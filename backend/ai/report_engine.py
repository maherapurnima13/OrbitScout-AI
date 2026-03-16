def generate_intelligence_report(data):

    nasa = data.get("nasa_updates", [])
    isro = data.get("isro_updates", [])
    spacex = data.get("spacex_launches", [])

    report = {}

    report["summary"] = f"""
OrbitScout Aerospace Intelligence Report

NASA updates detected: {len(nasa)}
ISRO mission updates: {len(isro)}
SpaceX launch updates: {len(spacex)}

Total aerospace intelligence signals detected: {len(nasa) + len(isro) + len(spacex)}
"""

    report["insights"] = []

    if len(spacex) > 0:
        report["insights"].append(
            "Commercial launch activity increasing — potential satellite deployment opportunities."
        )

    if len(isro) > 0:
        report["insights"].append(
            "Indian space missions showing activity — potential collaboration or procurement opportunities."
        )

    if len(nasa) > 0:
        report["insights"].append(
            "NASA program updates detected — potential aerospace research opportunities."
        )

    return report