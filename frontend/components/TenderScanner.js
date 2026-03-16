export default function TenderScanner() {

  const tenders = [
    {
      title: "Drone Surveillance System",
      agency: "Indian Defence",
      budget: "₹8 Cr"
    },
    {
      title: "Satellite Communication System",
      agency: "ISRO Procurement",
      budget: "₹9 Cr"
    },
    {
      title: "Aerospace Composite Manufacturing",
      agency: "DRDO",
      budget: "₹7 Cr"
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-lg">

      {/* Title */}
      <h2 className="text-lg font-semibold mb-5 text-sky-400">
        🚀 Aerospace Tender Intelligence
      </h2>

      <div className="space-y-4">

        {tenders.map((tender, i) => (

          <div
            key={i}
            className="bg-slate-950 border border-slate-800 rounded-lg p-4 hover:border-sky-500 transition"
          >

            {/* Tender Title */}
            <p className="font-semibold text-white">
              {tender.title}
            </p>

            {/* Agency */}
            <p className="text-sm text-slate-400 mt-1">
              {tender.agency}
            </p>

            {/* Budget Badge */}
            <div className="mt-2 inline-block text-xs bg-sky-500/20 text-sky-400 px-3 py-1 rounded-full">
              Budget: {tender.budget}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}