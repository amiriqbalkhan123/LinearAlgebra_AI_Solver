
import type { MatrixResponse } from "../../services/api";
import MathDisplay from "../math/MathDisplay";

interface SolutionViewerProps {
  solution: MatrixResponse;
}

export default function SolutionViewer({
  solution,
}: SolutionViewerProps) {
  return (
    <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <h2 className="text-xl font-semibold">
        Mathematical Solution
      </h2>

      <div>
        <p className="mb-2 text-sm text-zinc-400">
          Input Matrix A
        </p>
        <MathDisplay latex={solution.input_latex} />
      </div>

      {solution.matrix_b_latex && (
        <div>
          <p className="mb-2 text-sm text-zinc-400">
            Input Matrix B
          </p>
          <MathDisplay latex={solution.matrix_b_latex} />
        </div>
      )}

      <div className="border-t border-zinc-800 pt-5">
        <p className="mb-3 text-sm text-zinc-400">
          {solution.operation.toUpperCase()} — Result
        </p>
        <div className="rounded-lg bg-zinc-950 p-4 text-green-400">
          <MathDisplay latex={solution.result_latex} />
        </div>
      </div>
    </section>
  );
}
