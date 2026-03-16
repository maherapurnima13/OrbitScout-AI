export default function LaunchTracker() {

  const launches = [
    {
      mission: "Starlink Mission",
      rocket: "Falcon 9",
      agency: "SpaceX",
      date: "2026-04-10"
    },
    {
      mission: "Gaganyaan Test",
      rocket: "LVM3",
      agency: "ISRO",
      date: "2026-05-12"
    },
    {
      mission: "Artemis Support",
      rocket: "SLS",
      agency: "NASA",
      date: "2026-06-02"
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg">

      {/* Title */}
      <h2 className="text-lg font-semibold mb-5 text-sky-400">
        🚀 Satellite Launch Tracker
      </h2>

      <div className="space-y-4">

        {launches.map((launch, i) => (

          <div
            key={i}
            className="bg-slate-950 border border-slate-800 rounded-lg p-4 hover:border-sky-500 transition"
          >

            {/* Mission */}
            <p className="font-semibold text-white">
              {launch.mission}
            </p>

            {/* Rocket + Agency */}
            <p className="text-sm text-slate-400 mt-1">
              {launch.rocket} • {launch.agency}
            </p>

            {/* Date */}
            <div className="mt-2 inline-block text-xs bg-sky-500/20 text-sky-400 px-3 py-1 rounded-full">
              Launch Date: {launch.date}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}