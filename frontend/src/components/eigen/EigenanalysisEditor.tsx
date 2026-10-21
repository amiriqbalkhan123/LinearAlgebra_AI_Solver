
import { useState } from "react";
import axios from "axios";
import { CheckCircle2, AlertCircle } from "lucide-react";

import MatrixEditor from "../math/MatrixEditor";
import MathDisplay from "../math/MathDisplay";

import type { MatrixData } from "../../services/api";

import {
  analyzeEigen,
  type EigenanalysisResponse,
} from "../../services/eigenanalysisApi";


export default function EigenanalysisEditor() {
  const [matrix, setMatrix] = useState<MatrixData>([
    ["4", "1"],
    ["0", "2"],
  ]);

  const [result, setResult] =
    useState<EigenanalysisResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSteps, setShowSteps] = useState(true);

  const rows = matrix.length;
  const cols = matrix[0].length;

  const validShape =
    rows === cols && rows <= 4;

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await analyzeEigen(matrix);
      setResult(response);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;

        setError(
          typeof detail === "string"
            ? detail
            : "Invalid matrix or backend unavailable."
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
          Eigenanalysis & Diagonalization
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Compute exact eigenvalues, eigenvectors,
          eigenspaces, multiplicities and diagonalization.
        </p>
      </header>

      <MatrixEditor
        name="A"
        matrix={matrix}
        onChange={(next) => {
          setMatrix(next);
          setResult(null);
          setError("");
        }}
      />

      {!validShape && (
        <div className="flex items-center gap-2 rounded-lg border border-amber-900 bg-amber-950 p-4 text-sm text-amber-300">
          <AlertCircle size={18} />
          Select a square matrix with dimensions
          between 1×1 and 4×4.
        </div>
      )}

      <button
        type="button"
        disabled={!validShape || loading}
        onClick={handleAnalyze}
        className="w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading
          ? "Analyzing..."
          : "Analyze Eigenvalues & Eigenvectors"}
      </button>

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
              Eigenanalysis Results
            </h3>

            {result.verified && (
              <span className="flex items-center gap-2 text-sm text-green-400">
                <CheckCircle2 size={18} />
                Verified
              </span>
            )}
          </div>

          <div className="rounded-lg bg-zinc-950 p-4">
            <h4 className="mb-3 font-medium">
              Characteristic Polynomial
            </h4>
            <MathDisplay
              latex={`p_A(\\lambda)=${result.characteristic_latex}`}
            />

            <p className="mt-3 text-sm text-zinc-400">
              Factored form
            </p>
            <MathDisplay
              latex={`p_A(\\lambda)=${result.factored_latex}`}
            />
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            {result.eigenvalues.map((item, index) => (
              <article
                key={index}
                className="space-y-4 rounded-lg border border-zinc-800 bg-zinc-950 p-4"
              >
                <h4 className="font-semibold">
                  Eigenvalue {index + 1}
                </h4>

                <MathDisplay
                  latex={`\\lambda=${item.value_latex}`}
                />

                <div className="grid grid-cols-2 gap-2 text-center">
                  <div className="rounded bg-zinc-900 p-3">
                    <p className="text-xs text-zinc-400">
                      Algebraic
                    </p>
                    <p className="text-xl font-semibold">
                      {item.algebraic_multiplicity}
                    </p>
                  </div>

                  <div className="rounded bg-zinc-900 p-3">
                    <p className="text-xs text-zinc-400">
                      Geometric
                    </p>
                    <p className="text-xl font-semibold">
                      {item.geometric_multiplicity}
                    </p>
                  </div>
                </div>

                <p className="text-sm text-zinc-400">
                  Eigenspace basis
                </p>

                {item.basis_latex.map((v, i) => (
                  <MathDisplay key={i} latex={v} />
                ))}
              </article>
            ))}
          </div>

          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4">
            <h4 className="mb-3 font-semibold">
              Diagonalization
            </h4>

            {result.diagonalizable ? (
              <div className="space-y-3">
                <p className="text-sm text-green-400">
                  This matrix is diagonalizable.
                </p>

                {result.P_latex && (
                  <MathDisplay
                    latex={`P=${result.P_latex}`}
                  />
                )}

                {result.D_latex && (
                  <MathDisplay
                    latex={`D=${result.D_latex}`}
                  />
                )}

                <MathDisplay latex="A=PDP^{-1}" />
              </div>
            ) : (
              <p className="text-sm text-amber-300">
                This matrix does not have enough
                linearly independent eigenvectors
                for diagonalization.
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-lg bg-zinc-950 p-4">
              <p className="mb-2 text-xs text-zinc-400">
                Trace
              </p>
              <MathDisplay latex={result.trace} />
            </div>

            <div className="rounded-lg bg-zinc-950 p-4">
              <p className="mb-2 text-xs text-zinc-400">
                Determinant
              </p>
              <MathDisplay latex={result.determinant} />
            </div>
          </div>

          <div className="border-t border-zinc-800 pt-5">
            <button
              type="button"
              onClick={() => setShowSteps((prev) => !prev)}
              aria-expanded={showSteps}
              className="w-full text-left text-lg font-semibold"
            >
              {showSteps ? "Hide" : "Show"}
              {" "}Step-by-Step Explanation
              {" "}({result.steps.length})
            </button>

            {showSteps && (
              <div className="mt-4 space-y-3">
                {result.steps.map((step, index) => (
                  <article
                    key={index}
                    className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                  >
                    <p className="mb-3 text-sm text-zinc-300">
                      <span className="mr-2 text-blue-400">
                        {index + 1}.
                      </span>
                      {step.description}
                    </p>

                    <MathDisplay latex={step.latex} />
                  </article>
                ))}
              </div>
            )}
          </div>
        </section>
      )}
    </section>
  );
}
