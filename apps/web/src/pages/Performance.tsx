import { useEffect, useState } from "react";
import { getMetrics, type Metrics } from "../lib/api";

const CARDS = ["AUROC", "AUPRC", "Sensitivity", "Specificity", "F1", "Accuracy"] as const;

export function Performance() {
  const [data, setData] = useState<Metrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getMetrics()
      .then(setData)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section>
      <p className="kicker">Held-out split</p>
      <h1 className="mt-3 font-serif text-3xl font-normal tracking-tight">Model performance</h1>
      <p className="mt-2 max-w-xl text-sm text-mute">
        Numbers appear only from evaluation artifacts. This foundation returns
        an empty contract on purpose.
      </p>

      <div className="mt-10 border border-line px-6 py-8">
        <p className="kicker">Status</p>
        <p className="mt-3 max-w-2xl font-serif text-2xl leading-snug">
          {error
            ? "API unreachable — start the backend to load the empty state."
            : data?.message ?? "Loading…"}
        </p>
      </div>

      <div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-3">
        {CARDS.map((label) => (
          <div key={label} className="border border-line px-4 py-5">
            <p className="kicker">{label}</p>
            <p className="mt-3 font-serif text-3xl text-stone">—</p>
          </div>
        ))}
      </div>
    </section>
  );
}
