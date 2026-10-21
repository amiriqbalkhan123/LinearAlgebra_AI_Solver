
import { useState } from "react";
import {
  solveMatrix,
  type MatrixOperation,
  type MatrixResponse,
} from "./services/api";

const operations: MatrixOperation[] = [
  "determinant",
  "rank",
  "rref",
  "transpose",
];

export default function App() {
  const [matrix, setMatrix] = useState<number[][]>([
    [4, 1],
    [0, 2],
  ]);

  const [operation, setOperation] =
    useState<MatrixOperation>("determinant");

  const [result, setResult] =
    useState<MatrixResponse | null>(null);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateCell(
    row: number,
    col: number,
    value: number
  ) {
    setMatrix((previous) =>
      previous.map((items, rowIndex) =>
        items.map((item, colIndex) =>
          rowIndex === row && colIndex === col
            ? value
            : item
        )
      )
    );
    setResult(null);
  }

  async function handleSolve() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const answer = await solveMatrix({
        matrix,
        operation,
      });
      setResult(answer);
    } catch {
      setError("Unable to solve. Check the matrix and API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 p-6 text-white">
      <div className="mx-auto max-w-3xl space-y-8">
        <header className="border-b border-zinc-800 pb-6">
          <h1 className="text-4xl font-bold">
            LinearAI
          </h1>
          <p className="mt-2 text-zinc-400">
            Intelligent Linear Algebra Solver
          </p>
        </header>

        <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <h2 className="mb-4 text-xl font-semibold">
            Matrix Input
          </h2>

          <div className="grid grid-cols-2 gap-3">
            {matrix.map((row, rowIndex) =>
              row.map((value, colIndex) => (
                <input
                  key={`${rowIndex}-${colIndex}`}
                  type="number"
                  value={value}
                  onChange={(event) =>
                    updateCell(
                      rowIndex,
                      colIndex,
                      Number(event.target.value)
                    )
                  }
                  className="w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3 text-center"
                />
              ))
            )}
          </div>

          <label
            htmlFor="operation"
            className="mt-6 block text-sm text-zinc-300"
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
              setResult(null);
            }}
            className="mt-2 w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3"
          >
            {operations.map((item) => (
              <option key={item} value={item}>
                {item.toUpperCase()}
              </option>
            ))}
          </select>

          <button
            type="button"
            onClick={handleSolve}
            disabled={loading}
            className="mt-6 w-full rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
          >
            {loading ? "Solving..." : "Solve Matrix"}
          </button>
        </section>

        {error && (
          <p role="alert" className="text-red-400">
            {error}
          </p>
        )}

        {result && (
          <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="mb-3 text-xl font-semibold">
              Solution
            </h2>
            <p className="break-all font-mono text-green-400">
              {result.result}
            </p>
          </section>
        )}
      </div>
    </main>
  );
}
