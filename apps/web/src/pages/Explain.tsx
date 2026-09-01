export function Explain() {
  const steps = [
    "Forward the chest X-ray through DenseNet121.",
    "Take the pneumonia logit as the target score.",
    "Weight the last convolutional map (denseblock4) by its gradients.",
    "ReLU, upsample, overlay. That is attribution — not a lesion outline.",
  ];

  return (
    <section className="max-w-2xl">
      <p className="kicker">Attribution</p>
      <h1 className="mt-3 font-serif text-3xl font-normal tracking-tight">Grad-CAM</h1>
      <p className="mt-4 leading-relaxed text-mute">
        Heatmaps will live here once inference is connected. The copy below is
        the contract the UI will keep: Grad-CAM answers which regions the
        network used, not where disease is.
      </p>
      <ol className="mt-10 space-y-6">
        {steps.map((step, i) => (
          <li key={step} className="flex gap-5">
            <span className="kicker mt-1 w-8 shrink-0">{String(i + 1).padStart(2, "0")}</span>
            <p className="font-serif text-xl leading-snug">{step}</p>
          </li>
        ))}
      </ol>
      <hr className="rule my-12" />
      <p className="text-sm leading-relaxed text-mute">
        If a future overlay lights up a corner marker or a shoulder, treat it as
        a shortcut — a debugging signal, not pathology.
      </p>
    </section>
  );
}
