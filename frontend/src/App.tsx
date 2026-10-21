
import { useState } from "react";
import axios from "axios";
import {
  Calculator,
  RotateCcw,
  Sigma,
} from "lucide-react";
import VectorGeometryEditor from "./components/vectors/VectorGeometryEditor";
import MatrixEditor from "./components/math/MatrixEditor";
import VectorSpacesEditor from "./components/vectors/VectorSpacesEditor";
import SolutionViewer from "./components/solutions/SolutionViewer";
import LinearSystemEditor from "./components/systems/LinearSystemEditor";
import EigenanalysisEditor from "./components/eigen/EigenanalysisEditor";
import {
  solveMatrix,
  type MatrixData,
  type MatrixOperation,
  type MatrixResponse,
} from "./services/api";

const operations: {
  value: MatrixOperation;
  label: string;
}[] = [
  { value: "addition", label: "Matrix Addition" },
  { value: "subtraction", label: "Matrix Subtraction" },
  { value: "multiplication", label: "Matrix Multiplication" },
  { value: "determinant", label: "Determinant" },
  { value: "inverse", label: "Matrix Inverse" },
  { value: "transpose", label: "Matrix Transpose" },
  { value: "rank", label: "Matrix Rank" },
  {
    value: "ref",
    label: "Row Echelon Form (REF)",
  },
  { value: "rref", label: "Reduced Row Echelon Form" },
];

const binaryOperations: MatrixOperation[] = [
  "addition",
  "subtraction",
  "multiplication",
];

function defaultMatrixA(): MatrixData {
  return [
    ["4", "1"],
    ["0", "2"],
  ];
}

function defaultMatrixB(): MatrixData {
  return [
    ["1", "2"],
    ["3", "4"],
  ];
}

export default function App() {
  const [activeTab, setActiveTab] = useState<
    "matrices" | "systems" | "vectors" | "geometry" | "eigen"
  >("matrices");
  const [matrixA, setMatrixA] =
    useState<MatrixData>(defaultMatrixA);

  const [matrixB, setMatrixB] =
    useState<MatrixData>(defaultMatrixB);

  const [operation, setOperation] =
    useState<MatrixOperation>("determinant");

  const [solution, setSolution] =
    useState<MatrixResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const requiresMatrixB =
    binaryOperations.includes(operation);

  function reset() {
    setMatrixA(defaultMatrixA());
    setMatrixB(defaultMatrixB());
    setOperation("determinant");
    setSolution(null);
    setError("");
  }

  async function handleSolve() {
    setLoading(true);
    setError("");
    setSolution(null);

    try {
      const result = await solveMatrix({
        matrix: matrixA,
        matrix_b: requiresMatrixB
          ? matrixB
          : undefined,
        operation,
      });

      setSolution(result);
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
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-5xl space-y-8 px-5 py-8">
        <header className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-800 pb-6">
          <div>
            <div className="flex items-center gap-3">
              <Sigma className="text-blue-400" size={32} />
              <h1 className="text-3xl font-bold">
                LinearAI
              </h1>
            </div>
            <p className="mt-2 text-zinc-400">
              Intelligent Linear Algebra Solver
            </p>
          </div>

          {activeTab === "matrices" && (
            <button
            type="button"
            onClick={reset}
            className="flex items-center gap-2 rounded-lg border border-zinc-700 px-4 py-2 hover:bg-zinc-800"
          >
            <RotateCcw size={16} />
            Reset
            </button>
          )}
        </header>

        <nav aria-label="Solver mode" className="flex flex-wrap gap-2 border-b border-zinc-800 pb-4">
          <button
            type="button"
            aria-pressed={activeTab === "matrices"}
            onClick={() => setActiveTab("matrices")}
            className={`rounded-lg px-4 py-2 ${
              activeTab === "matrices"
                ? "bg-blue-600 text-white"
                : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700"
            }`}
          >
            Matrix Calculator
          </button>
          <button
            type="button"
            aria-pressed={activeTab === "systems"}
            onClick={() => setActiveTab("systems")}
            className={`rounded-lg px-4 py-2 ${
              activeTab === "systems"
                ? "bg-blue-600 text-white"
                : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700"
            }`}
          >
            Linear Systems
          </button>
          
          <button
            type="button"
            aria-pressed={activeTab === "vectors"}
            onClick={() => setActiveTab("vectors")}
            className={`rounded-lg px-4 py-2 ${
              activeTab === "vectors"
                ? "bg-blue-600 text-white"
                : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700"
            }`}
          >
            Vector Spaces
          </button>

          
          <button
            type="button"
            aria-pressed={activeTab === "geometry"}
            onClick={() => setActiveTab("geometry")}
            className={`rounded-lg px-4 py-2 ${
              activeTab === "geometry"
                ? "bg-blue-600 text-white"
                : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700"
            }`}
          >
            Vector Geometry
          </button>

          
          <button
            type="button"
            aria-pressed={activeTab === "eigen"}
            onClick={() => setActiveTab("eigen")}
            className={`rounded-lg px-4 py-2 ${
              activeTab === "eigen"
                ? "bg-blue-600 text-white"
                : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700"
            }`}
          >
            Eigenanalysis
          </button>



        </nav>

        {activeTab === "matrices" && (
        <section className="space-y-5">
          <div>
            <h2 className="text-2xl font-semibold">
              Matrix Calculator
            </h2>
            <p className="mt-2 text-sm text-zinc-400">
              Enter your values, select an operation,
              and calculate exact results.
            </p>
          </div>

          <div className={`grid gap-5 ${requiresMatrixB ? "lg:grid-cols-2" : ""}`}>
            <MatrixEditor
              name="A"
              matrix={matrixA}
              onChange={(value) => {
                setMatrixA(value);
                setSolution(null);
              }}
            />

            {requiresMatrixB && (
              <MatrixEditor
                name="B"
                matrix={matrixB}
                onChange={(value) => {
                  setMatrixB(value);
                  setSolution(null);
                }}
              />
            )}
          </div>

          <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
            <label
              htmlFor="operation"
              className="mb-3 block font-medium"
            >
              Mathematical Operation
            </label>

            <select
              id="operation"
              value={operation}
              onChange={(event) => {
                setOperation(
                  event.target.value as MatrixOperation
                );
                setSolution(null);
                setError("");
              }}
              className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3"
            >
              {operations.map((item) => (
                <option
                  key={item.value}
                  value={item.value}
                >
                  {item.label}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={handleSolve}
              disabled={loading}
              className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 p-3 font-semibold transition-colors hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Calculator size={18} />
              {loading ? "Calculating..." : "Solve"}
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

          {solution && (
            <SolutionViewer solution={solution} />
          )}
        </section>
        )}

        {activeTab === "systems" && <LinearSystemEditor />}
        {activeTab === "vectors" && <VectorSpacesEditor />}
        {activeTab === "geometry" && <VectorGeometryEditor />}

        <footer className="border-t border-zinc-800 pt-5 text-center text-xs text-zinc-500">
          LinearAI — Powered by Python, FastAPI, and SymPy
        </footer>
      </div>
    </main>
  );
}
