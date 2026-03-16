"use client";

import { useState } from "react";

import LaunchTracker from "../components/LaunchTracker";
import TenderScanner from "../components/TenderScanner";
import RegulationMonitor from "../components/RegulationMonitor";

export default function Home() {

  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [reports, setReports] = useState([]);

  const runAgent = async () => {

    const response = await fetch(
      "https://orbitscout-ai.onrender.com/query",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: query })
      }
    );

    const data = await response.json();

    setResult(data);
  };

  const loadReports = async () => {

    const response = await fetch(
      "https://orbitscout-ai.onrender.com/reports"
    );

    const data = await response.json();

    setReports(data);
  };


  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-950 to-black text-white px-10 py-12">

      {/* Header */}
      <div className="mb-10 text-center">

        <h1 className="text-4xl font-bold text-sky-400 mb-2">
          🚀 OrbitScout AI
        </h1>

        <p className="text-slate-400 text-lg">
          Autonomous Aerospace Intelligence Platform
        </p>

      </div>


      {/* Query Panel */}
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl mb-12">

        <h2 className="text-xl font-semibold mb-5 text-sky-300">
          Ask OrbitScout
        </h2>

        <input
          className="w-full p-4 rounded-lg bg-slate-800 border border-slate-700 focus:outline-none focus:border-sky-400 mb-5"
          placeholder="Example: Find aerospace tenders in India"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="flex gap-4">

          <button
            onClick={runAgent}
            className="bg-sky-500 hover:bg-sky-600 transition px-6 py-2 rounded-lg font-medium shadow"
          >
            Run Intelligence Agent
          </button>

          <button
            onClick={loadReports}
            className="bg-indigo-500 hover:bg-indigo-600 transition px-6 py-2 rounded-lg font-medium shadow"
          >
            Load Intelligence History
          </button>

        </div>

      </div>


      {/* Monitoring Panels */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
          <LaunchTracker />
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
          <TenderScanner />
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
          <RegulationMonitor />
        </div>

      </div>


      {/* Aerospace Intelligence Report */}
      {result && (

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl mb-12">

          <h2 className="text-2xl font-semibold mb-6 text-sky-400">
            🛰 Aerospace Intelligence Report
          </h2>

          {/* Query */}
          <div className="mb-6">
            <p className="text-sm text-slate-400">
              Query
            </p>
            <p className="text-white font-medium">
              {result.query}
            </p>
          </div>


          {/* Summary */}
          <div className="mb-6 bg-slate-950 p-5 rounded-lg border border-slate-800">

            <p className="text-sky-400 font-semibold mb-2">
              Intelligence Summary
            </p>

            <p className="text-slate-300 whitespace-pre-line">
              {result.intelligence_report?.summary}
            </p>

          </div>


          {/* Insights */}
          <div className="mb-8">

            <p className="text-sky-400 font-semibold mb-3">
              Key Insights
            </p>

            <ul className="space-y-2">

              {result.intelligence_report?.insights?.map((insight, i) => (

                <li key={i} className="text-slate-300">
                  • {insight}
                </li>

              ))}

            </ul>

          </div>


          {/* Intelligence Signal Cards */}
          <div className="grid md:grid-cols-3 gap-6">

            <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg">

              <p className="text-sky-400 font-semibold mb-2">
                NASA Signals
              </p>

              <p className="text-2xl font-bold text-white">
                {result.aerospace_intelligence?.nasa_updates?.length || 0}
              </p>

            </div>


            <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg">

              <p className="text-sky-400 font-semibold mb-2">
                ISRO Signals
              </p>

              <p className="text-2xl font-bold text-white">
                {result.aerospace_intelligence?.isro_updates?.length || 0}
              </p>

            </div>


            <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg">

              <p className="text-sky-400 font-semibold mb-2">
                SpaceX Signals
              </p>

              <p className="text-2xl font-bold text-white">
                {result.aerospace_intelligence?.spacex_launches?.length || 0}
              </p>

            </div>

          </div>

        </div>

      )}


      {/* Intelligence History */}
      {reports.length > 0 && (

        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl">

          <h2 className="text-xl font-semibold mb-6 text-sky-300">
            Intelligence History
          </h2>

          <div className="space-y-4">

            {reports.map((r, i) => (

              <div
                key={i}
                className="border border-slate-800 rounded-lg p-4 bg-slate-950"
              >

                <p className="text-sky-400 text-sm mb-1">
                  {r.timestamp}
                </p>

                <p className="text-slate-300 text-sm">
                  {r.summary}
                </p>

              </div>

            ))}

          </div>

        </div>

      )}

    </div>
  );
}
