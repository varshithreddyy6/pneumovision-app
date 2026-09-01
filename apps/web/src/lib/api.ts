/** Thin client. Empty VITE_API_URL = same origin (Vite proxies /health and /v1). */

export const API_URL = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export type Health = {
  status: string;
  service: string;
  version: string;
  model_loaded: boolean;
  note: string;
};

export type AnalyzeResult = {
  status: string;
  label: string | null;
  probability_pneumonia: number | null;
  probability_normal: number | null;
  threshold: number;
  uncertain: boolean;
  review_recommended: boolean;
  confidence_band: string | null;
  message: string;
  filename: string | null;
  heatmap_data_url: string | null;
  overlay_data_url: string | null;
  untrained: boolean;
  disclaimer: string;
};

export type Metrics = {
  available: boolean;
  message: string;
  metrics: Record<string, number> | null;
};

function readErrorMessage(detail: unknown, status: number): string {
  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }
  if (detail !== null && typeof detail === "object" && "message" in detail) {
    const value = (detail as { message?: unknown }).message;
    if (typeof value === "string" && value.trim()) {
      return value;
    }
  }
  return `Upload failed (${status})`;
}

export async function getHealth(): Promise<Health> {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error(`Health check failed (${res.status})`);
  return res.json();
}

export async function getMetrics(): Promise<Metrics> {
  const res = await fetch(`${API_URL}/v1/metrics`);
  if (!res.ok) throw new Error(`Metrics request failed (${res.status})`);
  return res.json();
}

export async function postAnalyze(file: File): Promise<AnalyzeResult> {
  const body = new FormData();
  body.append("file", file);
  const res = await fetch(`${API_URL}/v1/analyze`, { method: "POST", body });
  const text = await res.text();
  let parsed: unknown = {};
  try {
    parsed = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(text.slice(0, 400) || `Upload failed (${res.status})`);
  }
  if (!res.ok) {
    const detail =
      parsed !== null && typeof parsed === "object" && "detail" in parsed
        ? (parsed as { detail?: unknown }).detail
        : undefined;
    throw new Error(readErrorMessage(detail, res.status));
  }
  return parsed as AnalyzeResult;
}
