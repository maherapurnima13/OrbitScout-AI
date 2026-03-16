export default function RegulationMonitor() {

  const regulations = [
    {
      authority: "DGCA India",
      update: "New drone airspace rules announced",
      date: "2026-03-20"
    },
    {
      authority: "FAA",
      update: "Urban air mobility framework update",
      date: "2026-03-22"
    },
    {
      authority: "EASA",
      update: "Satellite communication regulations revised",
      date: "2026-03-25"
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg">

      {/* Title */}
      <h2 className="text-lg font-semibold mb-5 text-sky-400">
        🚀 Aviation Regulation Monitor
      </h2>

      <div className="space-y-4">

        {regulations.map((reg, i) => (

          <div
            key={i}
            className="bg-slate-950 border border-slate-800 rounded-lg p-4 hover:border-sky-500 transition"
          >

            {/* Authority */}
            <p className="font-semibold text-white">
              {reg.authority}
            </p>

            {/* Update */}
            <p className="text-sm text-slate-400 mt-1">
              {reg.update}
            </p>

            {/* Date Badge */}
            <div className="mt-2 inline-block text-xs bg-sky-500/20 text-sky-400 px-3 py-1 rounded-full">
              {reg.date}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}