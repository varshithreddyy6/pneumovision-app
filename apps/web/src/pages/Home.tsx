import { Link } from "react-router-dom";

export function Home() {
  return (
    <section>
      <p className="kicker">Chest X-ray · research screen</p>
      <h1 className="mt-4 max-w-3xl font-serif text-4xl font-normal leading-[1.15] tracking-tight text-ink md:text-5xl">
        A quiet workstation for pneumonia screening research.
      </h1>
      <p className="mt-6 max-w-xl text-[1.05rem] leading-relaxed text-mute">
        DenseNet121, patient-level splits, Grad-CAM, and an uncertainty band —
        presented as a product UI, not a notebook. This repository is the
        foundation: layout, API contract, and empty states. Inference is not
        wired yet.
      </p>

      <div className="mt-10 flex flex-wrap items-center gap-6">
        <Link
          to="/analyze"
          className="border border-ink bg-ink px-6 py-3 text-[0.72rem] uppercase tracking-label text-paper no-underline"
        >
          Open workstation
        </Link>
        <Link
          to="/about"
          className="text-[0.72rem] uppercase tracking-label text-ink no-underline"
        >
          About &amp; contact
        </Link>
      </div>

      <hr className="rule my-16" />

      <div className="grid gap-12 md:grid-cols-3">
        {[
          {
            k: "01",
            t: "Architecture",
            d: "React UI talks to a FastAPI contract. PyTorch stays off the browser.",
          },
          {
            k: "02",
            t: "Honesty",
            d: "No fabricated metrics. Performance stays empty until a real evaluation exists.",
          },
          {
            k: "03",
            t: "Restraint",
            d: "Paper surface, one ink color, serif titles. The radiograph will be the hero.",
          },
        ].map((item) => (
          <article key={item.k}>
            <p className="kicker">{item.k}</p>
            <h2 className="mt-3 font-serif text-2xl font-normal">{item.t}</h2>
            <p className="mt-3 text-sm leading-relaxed text-mute">{item.d}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
