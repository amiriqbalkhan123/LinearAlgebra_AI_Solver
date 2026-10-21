
import { useState } from "react";
import axios from "axios";
import { CheckCircle2 } from "lucide-react";

import MatrixEditor from "../math/MatrixEditor";
import MathDisplay from "../math/MathDisplay";
import type { MatrixData } from "../../services/api";

import {
  solveVectorSpace,
  type VectorSpaceOperation,
  type VectorSpaceResponse,
} from "../../services/vectorSpacesApi";

const operations: {
  value: VectorSpaceOperation;
  label: string;
}[] = [
  { value: "column_space", label: "Column Space" },
  { value: "row_space", label: "Row Space" },
  { value: "null_space", label: "Null Space" },
  { value: "left_null_space", label: "Left Null Space" },
  { value: "rank_nullity", label: "Rank–Nullity Theorem" },
  { value: "independence", label: "Linear Independence" },
];

export default function VectorSpacesEditor() {
  const [matrix, setMatrix] = useState<MatrixData>([
    ["1", "2", "3"],
    ["2", "4", "6"],
  ]);

  const [operation, setOperation] =
    useState<VectorSpaceOperation>("null_space");

  const [result, setResult] =
    useState<VectorSpaceResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSolve() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const answer = await solveVectorSpace(
        matrix,
        operation
      );
      setResult(answer);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        setError(
          typeof detail === "string"
            ? detail
            : "Invalid matrix or server unavailable."
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
          Vector Spaces & Fundamental Subspaces
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Calculate exact bases, dimensions, pivots,
          null spaces and linear independence.
        </p>
      </div>

      <MatrixEditor
        name="A"
        matrix={matrix}
        onChange={(next) => {
          setMatrix(next);
          setResult(null);
          setError("");
        }}
      />

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
        <label
          htmlFor="space-operation"
          className="mb-3 block font-medium"
        >
          Vector Space Operation
        </label>

        <select
          id="space-operation"
          value={operation}
          onChange={(event) => {
            setOperation(
              event.target.value as VectorSpaceOperation
            );
            setResult(null);
          }}
          className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3"
        >
          {operations.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={handleSolve}
          disabled={loading}
          className="mt-5 w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          {loading ? "Calculating..." : "Solve Vector Space"}
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
        <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-xl font-semibold">
              {result.name}
            </h3>

            {result.verified && (
              <span className="flex items-center gap-2 text-sm text-green-400">
                <CheckCircle2 size={18} />
                Verified
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              ["Rank", result.rank],
              ["Nullity", result.nullity],
              ["Dimension", result.dimension ?? "—"],
            ].map(([label, value]) => (
              <div
                key={label}
                className="rounded-lg bg-zinc-950 p-4"
              >
                <p className="text-xs text-zinc-400">
                  {label}
                </p>
                <p className="mt-1 text-xl font-semibold">
                  {value}
                </p>
              </div>
            ))}
          </div>

          <div className="rounded-lg bg-zinc-950 p-4">
            <p className="mb-3 text-sm text-zinc-400">
              Reduced Row Echelon Form
            </p>
            <MathDisplay latex={result.rref_latex} />
          </div>

          {result.operation === "independence" && (
            <p className="rounded-lg bg-zinc-950 p-4">
              {result.is_independent
                ? "The matrix columns are linearly independent."
                : "The matrix columns are linearly dependent."}
            </p>
          )}

          {result.operation === "rank_nullity" && (
            <div className="rounded-lg bg-zinc-950 p-4">
              <MathDisplay
                latex={`\\operatorname{rank}(A)+\\operatorname{nullity}(A)=${result.rank}+${result.nullity}=${matrix[0].length}`}
              />
            </div>
          )}

          {result.dimension !== null &&
            result.operation !== "independence" && (
              <div className="rounded-lg border border-green-900 bg-zinc-950 p-4">
                <h4 className="mb-3 font-semibold text-green-400">
                  Basis Vectors
                </h4>

                {result.basis_latex.length > 0 ? (
                  <div className="space-y-3">
                    {result.basis_latex.map((vector, i) => (
                      <MathDisplay key={i} latex={vector} />
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-zinc-400">
                    Empty basis — zero-dimensional subspace.
                  </p>
                )}
              </div>
            )}

          <div className="space-y-3">
            <h4 className="text-lg font-semibold">
              Step-by-Step Calculation
            </h4>

            {result.steps.map((step, index) => (
              <article
                key={index}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
              >
                <p className="mb-3 text-sm text-zinc-300">
                  <span className="mr-2 font-semibold text-blue-400">
                    {index + 1}.
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
