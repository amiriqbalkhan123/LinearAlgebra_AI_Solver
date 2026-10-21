
import { useState } from "react";
import axios from "axios";

import MatrixEditor from "../math/MatrixEditor";
import SystemSolution from "./SystemSolution";

import type { MatrixData } from "../../services/api";
import {
  solveLinearSystem,
  type LinearSystemResponse,
} from "../../services/systemsApi";

export default function LinearSystemEditor() {
  const [matrix, setMatrix] = useState<MatrixData>([
    ["2", "1"],
    ["1", "-1"],
  ]);

  const [constants, setConstants] = useState<string[]>([
    "5",
    "1",
  ]);

  const [solution, setSolution] =
    useState<LinearSystemResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateMatrix(next: MatrixData) {
    setMatrix(next);

    setConstants((current) =>
      Array.from(
        { length: next.length },
        (_, index) => current[index] ?? "0"
      )
    );

    setSolution(null);
    setError("");
  }

  function updateConstant(index: number, value: string) {
    setConstants((previous) =>
      previous.map((item, i) =>
        i === index ? value : item
      )
    );

    setSolution(null);
    setError("");
  }

  async function handleSolve() {
    setLoading(true);
    setError("");
    setSolution(null);

    try {
      const result = await solveLinearSystem(
        matrix,
        constants
      );
      setSolution(result);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        setError(
          typeof detail === "string"
            ? detail
            : "Invalid system input."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">
          Linear Systems of Equations
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Solve Ax = b using exact Gauss–Jordan elimination.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[2fr_1fr]">
        <MatrixEditor
          name="A — Coefficients"
          matrix={matrix}
          onChange={updateMatrix}
        />

        <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <h3 className="mb-4 text-lg font-semibold">
            Vector b — Constants
          </h3>

          <div className="space-y-2">
            {constants.map((value, index) => (
              <label
                key={index}
                className="flex items-center gap-3"
              >
                <span className="w-8 text-sm text-zinc-400">
                  b{index + 1}
                </span>

                <input
                  type="text"
                  value={value}
                  onChange={(event) =>
                    updateConstant(
                      index,
                      event.target.value
                    )
                  }
                  className="w-full min-w-0 rounded-lg border border-zinc-700 bg-zinc-800 p-3 text-center"
                />
              </label>
            ))}
          </div>

          <p className="mt-4 text-xs text-zinc-500">
            Enter 0 for homogeneous systems.
          </p>
        </section>
      </div>

      <button
        type="button"
        onClick={handleSolve}
        disabled={loading}
        className="w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
      >
        {loading ? "Solving..." : "Solve Linear System"}
      </button>

      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-900 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      {solution && <SystemSolution solution={solution} />}
    </section>
  );
}
