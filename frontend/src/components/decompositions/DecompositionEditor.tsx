
import { useState } from "react";
import axios from "axios";
import { CheckCircle2 } from "lucide-react";

import MatrixEditor from "../math/MatrixEditor";
import MathDisplay from "../math/MathDisplay";

import type { MatrixData } from "../../services/api";

import {
  analyzeDecomposition,
  type DecompositionOperation,
  type DecompositionResponse,
} from "../../services/decompositionApi";

const operations: {
  value: DecompositionOperation;
  label: string;
}[] = [
  { value: "lu", label: "LU Decomposition" },
  { value: "qr", label: "QR Decomposition" },
  { value: "svd", label: "Singular Value Decomposition" },
  { value: "pseudoinverse", label: "Pseudoinverse" },
  { value: "least_squares", label: "Least Squares" },
  { value: "spectral", label: "Spectral Decomposition" },
  { value: "positive_definite", label: "Positive Definiteness" },
];

export default function DecompositionEditor() {
  const [matrix, setMatrix] = useState<MatrixData>([
    ["2", "1"],
    ["4", "3"],
  ]);

  const [operation, setOperation] =
    useState<DecompositionOperation>("lu");

  const [constants, setConstants] = useState<string[]>([
    "5", "11",
  ]);

  const [result, setResult] =
    useState<DecompositionResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const squareOnly = [
    "spectral",
    "positive_definite",
  ].includes(operation);

  const limit = operation === "svd" ? 10 : 6;

  const validShape =
    matrix.length <= limit &&
    matrix[0].length <= limit &&
    (!squareOnly || matrix.length === matrix[0].length);

  function updateMatrix(next: MatrixData) {
    setMatrix(next);
    setConstants((prev) =>
      Array.from(
        { length: next.length },
        (_, i) => prev[i] ?? "0"
      )
    );
    setResult(null);
    setError("");
  }

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await analyzeDecomposition({
        matrix,
        operation,
        ...(operation === "least_squares"
          ? { constants }
          : {}),
      });

      setResult(response);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        setError(
          typeof detail === "string"
            ? detail
            : "Invalid input or backend unavailable."
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
      <header>
        <h2 className="text-2xl font-semibold">
          Matrix Decompositions
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Exact and numerical factorization,
          pseudoinverse, least squares and spectral analysis.
        </p>
      </header>

      <MatrixEditor
        name="A"
        matrix={matrix}
        onChange={updateMatrix}
      />

      <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
        <label className="block space-y-2">
          <span className="font-medium">
            Mathematical Operation
          </span>

          <select
            value={operation}
            onChange={(event) => {
              setOperation(
                event.target.value as DecompositionOperation
              );
              setResult(null);
              setError("");
            }}
            className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3"
          >
            {operations.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        {operation === "least_squares" && (
          <div className="space-y-3">
            <h3 className="font-medium">
              Constants Vector b
            </h3>

            {constants.map((value, i) => (
              <label
                key={i}
                className="flex items-center gap-3"
              >
                <span className="w-8 text-sm text-zinc-400">
                  b{i + 1}
                </span>

                <input
                  type="text"
                  value={value}
                  onChange={(event) => {
                    const updated = [...constants];
                    updated[i] = event.target.value;
                    setConstants(updated);
                    setResult(null);
                  }}
                  className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 text-center"
                />
              </label>
            ))}
          </div>
        )}

        {!validShape && (
          <p className="text-sm text-amber-300">
            Select a compatible matrix, up to {limit}×{limit}.
            {squareOnly && " A square matrix is required."}
          </p>
        )}

        <button
          type="button"
          disabled={loading || !validShape}
          onClick={handleAnalyze}
          className="w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          {loading ? "Calculating..." : "Analyze Matrix"}
        </button>
      </section>

      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-900 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      {result && (
        <section className="space-y-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-xl font-semibold">
              Decomposition Results
            </h3>

            {result.verified && (
              <span className="flex items-center gap-2 text-sm text-green-400">
                <CheckCircle2 size={18} />
                Verified
              </span>
            )}
          </div>

          <p className="text-sm text-zinc-400">
            Computation mode:{" "}
            <strong className="text-white">
              {result.mode === "exact"
                ? "Exact symbolic"
                : "Numerical approximation"}
            </strong>
          </p>

          <div className="rounded-lg bg-zinc-950 p-4">
            <h4 className="mb-3 font-semibold">
              Input Matrix
            </h4>
            <MathDisplay latex={result.input_latex} />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {result.factors.map((factor, i) => (
              <article
                key={i}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
              >
                <h4 className="mb-3 font-semibold text-blue-400">
                  {factor.name}
                </h4>
                <MathDisplay latex={factor.latex} />
              </article>
            ))}
          </div>

          {result.metrics.length > 0 && (
            <div className="rounded-lg bg-zinc-950 p-4">
              <h4 className="mb-3 font-semibold">
                Mathematical Properties
              </h4>

              <div className="space-y-3">
                {result.metrics.map((item, i) => (
                  <div
                    key={i}
                    className="border-b border-zinc-800 pb-3 last:border-0"
                  >
                    <p className="text-xs text-zinc-400">
                      {item.name}
                    </p>
                    <p className="mt-1 break-words font-mono text-sm">
                      {item.value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-3">
            <h4 className="text-lg font-semibold">
              Mathematical Procedure
            </h4>

            {result.steps.map((step, i) => (
              <article
                key={i}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
              >
                <p className="mb-3 text-sm text-zinc-300">
                  <span className="mr-2 text-blue-400">
                    {i + 1}.
                  </span>
                  {step.description}
                </p>
                <MathDisplay latex={step.latex} />
              </article>
            ))}
          </div>
        </section>
      )}
    </section>
  );
}
