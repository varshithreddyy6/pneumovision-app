import { FormEvent, useRef, useState } from "react";
import { postAnalyze, type AnalyzeResult } from "../lib/api";

export function Analyze() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);

  function onPick(next: File | null) {
    setResult(null);
    setError(null);
    if (preview) URL.revokeObjectURL(preview);
    setFile(next);
    setPreview(next ? URL.createObjectURL(next) : null);
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!file) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await postAnalyze(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setBusy(false);
    }
  }

  const pct = (n: number | null) =>
    n == null || Number.isNaN(n) ? "—" : `${(n * 100).toFixed(1)}%`;

  return (
    <section>
      <p className="kicker">Workstation</p>
      <h1 className="mt-3 font-serif text-3xl font-normal tracking-tight">X-ray analysis</h1>
      <p className="mt-2 max-w-xl text-sm text-mute">
        Upload a frontal chest radiograph. ID cards and snapshots are not X-rays
        and will produce meaningless scores. This is not a diagnosis.
      </p>

      <div className="mt-10 grid gap-10 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <p className="kicker mb-3">Viewer</p>
          <div className="flex min-h-[420px] items-center justify-center border border-line bg-[#111]">
            {preview ? (
              <img
                src={preview}
                alt="Selected radiograph preview"
                className="max-h-[420px] w-full object-contain"
              />
            ) : (
              <p className="px-8 text-center text-[0.72rem] uppercase tracking-label text-stone">
                No image loaded
              </p>
            )}
          </div>
        </div>

        <aside>
          <p className="kicker mb-3">AI analysis</p>
          <div className="border border-line bg-white/40 p-6">
            <form onSubmit={onSubmit} className="space-y-5">
              <input
                ref={inputRef}
                type="file"
                accept="image/png,image/jpeg"
                className="hidden"
                onChange={(e) => onPick(e.target.files?.[0] ?? null)}
              />
              <button
                type="button"
                onClick={() => inputRef.current?.click()}
                className="w-full border border-ink bg-transparent px-4 py-3 text-[0.72rem] uppercase tracking-label"
              >
                {file ? "Replace image" : "Choose JPEG or PNG"}
              </button>
              <p className="truncate text-xs text-mute">{file ? file.name : "No file selected"}</p>
              <button
                type="submit"
                disabled={!file || busy}
                className="w-full border border-ink bg-ink px-4 py-3 text-[0.72rem] uppercase tracking-label text-paper disabled:opacity-40"
              >
                {busy ? "Running model…" : "Run analysis"}
              </button>
            </form>

            <hr className="rule my-6" />

            {error && <p className="text-sm text-ink">{error}</p>}

            {!result && !error && (
              <div className="space-y-4">
                <p className="font-serif text-2xl text-stone">—</p>
                <p className="text-sm text-mute">Waiting for an image.</p>
                <div className="grid grid-cols-2 gap-3">
                  <Stat label="P(pneumonia)" value="—" />
                  <Stat label="P(normal)" value="—" />
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-4">
                {result.uncertain && (
                  <p className="text-sm text-mute">
                    Near the decision threshold — human review recommended.
                  </p>
                )}
                <p
                  className={
                    result.label === "PNEUMONIA"
                      ? "font-serif text-3xl text-[#9A1B1B]"
                      : "font-serif text-3xl"
                  }
                >
                  {result.label ?? "—"}
                </p>
                <p className="text-sm leading-relaxed text-mute">{result.message}</p>
                <p className="text-[0.7rem] uppercase tracking-label text-stone">
                  {result.confidence_band}
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <Stat label="P(pneumonia)" value={pct(result.probability_pneumonia)} />
                  <Stat label="P(normal)" value={pct(result.probability_normal)} />
                </div>
              </div>
            )}
          </div>
        </aside>
      </div>

      <div className="mt-12 grid gap-6 md:grid-cols-3">
        <Panel title="Original" src={preview} />
        <Panel title="Heatmap" src={result?.heatmap_data_url ?? null} />
        <Panel title="Overlay" src={result?.overlay_data_url ?? null} />
      </div>
      <p className="mt-4 max-w-2xl text-xs leading-relaxed text-mute">
        Grad-CAM highlights regions the network used. It does not prove that the
        highlighted area is medically a consolidation or any other pathology.
      </p>
    </section>
  );
}

function Panel({ title, src }: { title: string; src: string | null }) {
  return (
    <figure>
      <p className="kicker mb-3">{title}</p>
      {src ? (
        <img src={src} alt={title} className="h-40 w-full border border-line object-contain bg-[#111]" />
      ) : (
        <div className="flex h-40 items-center justify-center border border-dashed border-line">
          <span className="text-[0.68rem] uppercase tracking-label text-stone">Not computed</span>
        </div>
      )}
    </figure>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="border border-line px-3 py-3">
      <p className="kicker">{label}</p>
      <p className="mt-2 font-serif text-xl">{value}</p>
    </div>
  );
}
