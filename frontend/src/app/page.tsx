"use client";

import { useEffect, useState } from "react";

interface HealthStatus {
  status: string;
  service: string;
  version: string;
  environment: string;
}

export default function HomePage() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

    fetch(`${apiUrl}/health`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        return response.json() as Promise<HealthStatus>;
      })
      .then(setHealth)
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Failed to reach API");
      });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6">
      <div className="w-full max-w-2xl rounded-xl border border-pyrocast-border bg-pyrocast-surface p-10 shadow-2xl">
        <div className="mb-6 flex items-center gap-3">
          <div className="h-3 w-3 rounded-full bg-pyrocast-accent animate-pulse" />
          <p className="font-mono text-xs uppercase tracking-widest text-pyrocast-muted">
            Phase 1 — Foundation
          </p>
        </div>

        <h1 className="mb-2 text-4xl font-bold tracking-tight text-white">PyroCast</h1>
        <p className="mb-8 text-lg text-gray-400">
          Enterprise wildfire spread prediction platform
        </p>

        <div className="rounded-lg border border-pyrocast-border bg-pyrocast-bg p-6">
          <h2 className="mb-4 font-mono text-sm uppercase tracking-wide text-pyrocast-accent">
            API Status
          </h2>

          {health && (
            <dl className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt className="text-pyrocast-muted">Status</dt>
                <dd className="font-medium text-pyrocast-success">{health.status}</dd>
              </div>
              <div>
                <dt className="text-pyrocast-muted">Service</dt>
                <dd className="font-medium">{health.service}</dd>
              </div>
              <div>
                <dt className="text-pyrocast-muted">Version</dt>
                <dd className="font-medium">{health.version}</dd>
              </div>
              <div>
                <dt className="text-pyrocast-muted">Environment</dt>
                <dd className="font-medium">{health.environment}</dd>
              </div>
            </dl>
          )}

          {error && (
            <p className="text-sm text-pyrocast-danger">
              Backend unreachable: {error}. Start the API with{" "}
              <code className="rounded bg-pyrocast-border px-1.5 py-0.5 font-mono text-xs">
                make api
              </code>
            </p>
          )}

          {!health && !error && (
            <p className="text-sm text-pyrocast-muted">Connecting to backend...</p>
          )}
        </div>
      </div>
    </main>
  );
}
