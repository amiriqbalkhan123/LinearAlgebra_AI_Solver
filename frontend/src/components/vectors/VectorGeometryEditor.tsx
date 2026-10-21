
import { useState } from "react";
import axios from "axios";
import { CheckCircle2 } from "lucide-react";

import MathDisplay from "../math/MathDisplay";

import {
  solveVectorGeometry,
  type VectorOperation,
  type VectorGeometryResponse,
} from "../../services/vectorGeometryApi";

const operations: { value: VectorOperation; label: string }[] = [
  { value: "addition", label: "Vector Addition" },
  { value: "subtraction", label: "Vector Subtraction" },
  { value: "scalar", label: "Scalar Multiplication" },
  { value: "dot", label: "Dot Product" },
  { value: "cross", label: "Cross Product (3D)" },
  { value: "outer", label: "Outer Product" },
  { value: "magnitude", label: "Magnitude / Norm" },
  { value: "normalize", label: "Normalization" },
  { value: "distance", label: "Distance" },
  { value: "angle", label: "Angle (Radians)" },
  { value: "orthogonality", label: "Orthogonality Test" },
  { value: "projection", label: "Projection of A onto B" },
  { value: "span_membership", label: "Span Membership" },
  { value: "gram_schmidt", label: "Gram–Schmidt" },
];

const binary: VectorOperation[] = [
  "addition", "subtraction", "dot", "cross",
  "outer", "distance", "angle",
  "orthogonality", "projection",
];

function parseVector(text: string): string[] {
  return text.split(",").map((part) => part.trim());
}

function parseVectors(text: string): string[][] {
  return text
    .split("\n")
    .filter((line) => line.trim())
    .map(parseVector);
}

export default function VectorGeometryEditor() {
  const [operation, setOperation] =
    useState<VectorOperation>("dot");

  const [a, setA] = useState("1, 2, 3");
  const [b, setB] = useState("4, 5, 6");
  const [scalar, setScalar] = useState("2");

  const [vectors, setVectors] = useState(
    "1, 0, 1\n1, 1, 0"
  );

  const [target, setTarget] = useState("2, 1, 1");
  const [normalizeBasis, setNormalizeBasis] = useState(true);

  const [result, setResult] =
    useState<VectorGeometryResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const usesVectorSet = [
    "span_membership", "gram_schmidt",
  ].includes(operation);

  async function handleSolve() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const request = usesVectorSet
        ? {
            operation,
            vectors: parseVectors(vectors),
            ...(operation === "span_membership"
              ? { target: parseVector(target) }
              : { normalize_basis: normalizeBasis }),
          }
        : {
            operation,
            a: parseVector(a),
            ...(binary.includes(operation)
              ? { b: parseVector(b) }
              : {}),
            ...(operation === "scalar" ? { scalar } : {}),
          };

      const answer = await solveVectorGeometry(request);
      setResult(answer);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        setError(
          typeof detail === "string"
            ? detail
            : "Invalid mathematical input."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  }

  const fieldClass =
    "w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 outline-none focus:border-blue-500";

  return (
    <section className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold">
          Vector Operations & Geometry
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Exact arithmetic, vector geometry, projections,
          span and orthogonalization.
        </p>
      </header>

      <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
        <label className="block space-y-2">
          <span className="font-medium">
            Mathematical Operation
          </span>
          <select
            value={operation}
            onChange={(event) => {
              setOperation(event.target.value as VectorOperation);
              setResult(null);
              setError("");
            }}
            className={fieldClass}
          >
            {operations.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        {!usesVectorSet ? (
          <>
            <label className="block space-y-2">
              <span>Vector A</span>
              <input
                className={fieldClass}
                value={a}
                onChange={(e) => setA(e.target.value)}
                placeholder="1, 2, 3"
              />
            </label>

            {binary.includes(operation) && (
              <label className="block space-y-2">
                <span>Vector B</span>
                <input
                  className={fieldClass}
                  value={b}
                  onChange={(e) => setB(e.target.value)}
                  placeholder="4, 5, 6"
                />
              </label>
            )}

            {operation === "scalar" && (
              <label className="block space-y-2">
                <span>Scalar</span>
                <input
                  className={fieldClass}
                  value={scalar}
                  onChange={(e) => setScalar(e.target.value)}
                />
              </label>
            )}
          </>
        ) : (
          <>
            <label className="block space-y-2">
              <span>Vectors — One per line</span>
              <textarea
                rows={5}
                className={fieldClass}
                value={vectors}
                onChange={(e) => setVectors(e.target.value)}
              />
            </label>

            {operation === "span_membership" && (
              <label className="block space-y-2">
                <span>Target Vector</span>
                <input
                  className={fieldClass}
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                />
              </label>
            )}

            {operation === "gram_schmidt" && (
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={normalizeBasis}
                  onChange={(e) =>
                    setNormalizeBasis(e.target.checked)
                  }
                />
                Return orthonormal basis
              </label>
            )}
          </>
        )}

        <p className="text-xs text-zinc-500">
          Separate coordinates with commas. Fractions such as
          1/2, -3/4 and exact decimals are supported.
        </p>

        <button
          type="button"
          onClick={handleSolve}
          disabled={loading}
          className="w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          {loading ? "Calculating..." : "Solve Vector Problem"}
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
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold">
              Solution
            </h3>
            {result.verified && (
              <span className="flex items-center gap-2 text-sm text-green-400">
                <CheckCircle2 size={18} />
                Verified
              </span>
            )}
          </div>

          <div className="rounded-lg border border-green-900 bg-zinc-950 p-4">
            <h4 className="mb-3 font-semibold text-green-400">
              Final Answer
            </h4>
            <MathDisplay latex={result.result_latex} />
          </div>

          <h4 className="text-lg font-semibold">
            Mathematical Steps
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
        </section>
      )}
    </section>
  );
}
