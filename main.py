# app/main.py
import os
import json
import numpy as np
import mysql.connector
from datetime import datetime
from fastapi import FastAPI, WebSocket, Request, BackgroundTasks, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
from dotenv import load_dotenv
from sqlalchemy import text

from app.db import SessionLocal
from app.models import Item, Event, Base
from app.recommender import get_model, best_matches

# ----------------------------
# Environment & App Setup
# ----------------------------
load_dotenv()

app = FastAPI(title="AI Travel Recommendation & Analytics API")
templates = Jinja2Templates(directory="app/templates")

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/recent")
async def recent_searches_page(request: Request):
    # ✅ Create a new DB connection
    conn = mysql.connector.connect(
        host="192.168.99.100",   # or "db" if using Docker
        user="root",
        password="example",
        database="mydb"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT query, timestamp FROM searches ORDER BY timestamp DESC LIMIT 20")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return templates.TemplateResponse("recent.html", {"request": request, "results": results})

# Static + Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ----------------------------
# Global Variables
# ----------------------------
connected = []  # WebSocket connections
MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
model = SentenceTransformer(MODEL_NAME)

# ----------------------------
# Database Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Helper: Load items + embeddings (NEW)
# ----------------------------
def load_items_memory(db: Session):
    """Load items and generate text embeddings for each."""
    items = db.query(Item).all()
    if not items:
        return [], [], np.zeros((0, 384), dtype=np.float32)

    texts = [
        f"{it.title}. {it.description or ''}. {it.location or ''}. {it.tags or ''}"
        for it in items
    ]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return items, texts, embeddings


# ----------------------------
# NEW: Recommender + Event Logging (Updated & Working)
# ----------------------------
@app.post("/api/recommend")
def recommend_and_log(payload: Dict, db: Session = Depends(get_db)):
    query = payload.get("query", "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query' in body")

    # --- Save query in searches table (for /recent page) ---
    try:
        conn = mysql.connector.connect(
            host="192.168.99.100",   # same as /recent route
            user="root",
            password="example",
            database="mydb"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO searches (query, timestamp) VALUES (%s, NOW())", (query,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Saved search query: {query}")
    except Exception as e:
        print(f"⚠️ Error saving search query: {e}")

    # Load items and precompute embeddings
    items, texts, embeddings = load_items_memory(db)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")

    # Compute query embedding
    query_emb = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)

    # Compute cosine similarity
    cosine_scores = np.dot(embeddings, query_emb)
    top_indices = np.argsort(-cosine_scores)[:3]  # top 3 results

    results = []
    for idx in top_indices:
        item = items[idx]
        score = float(cosine_scores[idx])
        image_url = item.image_url or "/static/images/placeholder.png"
        
        results.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "image_url": item.image_url,
            "location": item.location,
            "tags": item.tags,
            "score": round(score, 3)
        })

    # Log event
    best_match = results[0] if results else None
    event = Event(
        event_type="search",
        item_id=best_match["id"] if best_match else None,
        user_id=None,
        meta={
            "query": query,
            "similarity": float(best_match["score"]) if best_match else 0.0,
            "recommended_title": best_match["title"] if best_match else None
        }
    )
    db.add(event)
    db.commit()

    return {
        "query": query,
        "recommendations": [
            {
                "destination": r["title"],
                "description": r["description"],
                "image_url": r["image_url"],
                "location": r["location"],
                "tags": r["tags"],
                "score": r["score"]
            }
            for r in results
        ]
    }

# ----------------------------
# Event Tracking (Clicks, Views)
# ----------------------------
@app.post("/track")
async def track(event: dict, background: BackgroundTasks):
    session: Session = SessionLocal()
    try:
        ev = Event(
            event_type=event.get("event_type"),
            item_id=event.get("item_id"),
            user_id=event.get("user_id"),
            meta=event.get("meta")
        )
        session.add(ev)
        session.commit()
        background.add_task(trigger_publish_analytics_update)
        return {"status": "ok"}
    except Exception as e:
        session.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        session.close()

# ----------------------------
# Analytics Helpers
# ----------------------------
def get_aggregate_top(n=5):
    session: Session = SessionLocal()
    try:
        res = session.execute(
            "SELECT item_id, COUNT(*) as cnt FROM events WHERE event_type='click' AND item_id IS NOT NULL GROUP BY item_id ORDER BY cnt DESC LIMIT :n",
            {"n": n}
        ).fetchall()
        return [{"item_id": r[0], "count": int(r[1])} for r in res]
    finally:
        session.close()

from sqlalchemy import text  # ✅ add this import at the top

@app.get("/analytics/top-queries")
def analytics_top_queries(limit: int = 10):
    """
    Compatible with MariaDB 10.5 (no JSON_EXTRACT).
    Extracts query text from meta using string search.
    """
    session = SessionLocal()
    try:
        sql = text("""
        SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(meta, '"query": "', -1), '"', 1) AS query,
               COUNT(*) AS cnt
        FROM events
        WHERE event_type = 'search' AND meta LIKE '%"query":%'
        GROUP BY query
        ORDER BY cnt DESC
        LIMIT :limit
        """)  # ✅ wrap SQL in text()

        rows = session.execute(sql, {"limit": limit}).fetchall()
        result = [{"query": r[0] or "", "count": int(r[1])} for r in rows]
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        session.close()

async def publish_analytics_update():
    top = get_aggregate_top(10)
    data = {"type": "analytics_update", "top": top}
    living = []
    for ws in connected:
        try:
            await ws.send_json(data)
            living.append(ws)
        except Exception:
            pass
    connected[:] = living

def trigger_publish_analytics_update():
    import asyncio
    asyncio.create_task(publish_analytics_update())

# ----------------------------
# Analytics Endpoints
# ----------------------------
@app.get("/analytics/summary")
async def analytics_summary():
    top = get_aggregate_top(10)
    return {"top_clicks": top}

@app.get("/analytics/recent-searches")
def recent_searches(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(Event)
        .filter(Event.event_type == "search")
        .order_by(Event.created_at.desc())
        .limit(limit)
        .all()
    )
    result = []
    for r in rows:
        meta = r.meta or {}
        result.append({
            "id": r.id,
            "query": meta.get("query"),
            "similarity": meta.get("similarity"),
            "recommended": meta.get("recommended_title"),
            "when": r.created_at.isoformat() if hasattr(r, "created_at") else None
        })
    return result

# ----------------------------
# WebSocket for Live Analytics
# ----------------------------
@app.websocket("/ws/analytics")
async def websocket_analytics(ws: WebSocket):
    await ws.accept()
    connected.append(ws)
    try:
        await ws.send_json({"type": "welcome", "top": get_aggregate_top(10)})
        while True:
            _ = await ws.receive_text()
    except Exception:
        pass
    finally:
        try:
            connected.remove(ws)
        except:
            pass

# ----------------------------
# Routes for UI
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = "app/static/index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/search")
def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})
