
import { CheckCircle2 } from "lucide-react";

import MathDisplay from "../math/MathDisplay";

import type {
  LinearSystemResponse,
} from "../../services/systemsApi";

interface Props {
  solution: LinearSystemResponse;
}

const labels = {
  unique: "Unique Solution",
  infinite: "Infinitely Many Solutions",
  no_solution: "No Solution — Inconsistent",
};

export default function SystemSolution({ solution }: Props) {
  const variables = Array.from(
    { length: solution.unknowns },
    (_, i) => `x_{${i + 1}}`
  );

  const vectorLatex =
    "\\begin{bmatrix}" +
    variables.join("\\\\") +
    "\\end{bmatrix}";

  return (
    <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold">
          {labels[solution.classification]}
        </h2>

        {solution.verified && (
          <span className="flex items-center gap-2 text-sm text-green-400">
            <CheckCircle2 size={18} />
            Verified
          </span>
        )}
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        {[
          ["Equations", solution.equations],
          ["Unknowns", solution.unknowns],
          ["Rank(A)", solution.rank_a],
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
        <h3 className="mb-3 font-medium">
          Augmented Matrix
        </h3>
        <MathDisplay latex={solution.input_latex} />
      </div>

      <div className="rounded-lg bg-zinc-950 p-4">
        <h3 className="mb-3 font-medium">
          Reduced Row Echelon Form
        </h3>
        <MathDisplay latex={solution.rref_latex} />
      </div>

      <div className="rounded-lg border border-green-900 bg-zinc-950 p-4">
        <h3 className="mb-3 font-semibold text-green-400">
          Final Result
        </h3>

        {solution.solution_latex ? (
          <MathDisplay
            latex={`${vectorLatex}=${solution.solution_latex}`}
          />
        ) : (
          <MathDisplay latex="\\varnothing" />
        )}

        {solution.free_variables.length > 0 && (
          <p className="mt-3 text-sm text-zinc-400">
            Free variables:{" "}
            {solution.free_variables.join(", ")}
            {" — parameters are arbitrary real numbers."}
          </p>
        )}
      </div>

      <div className="space-y-3">
        <h3 className="text-lg font-semibold">
          Step-by-Step Solution
        </h3>

        {solution.steps.map((step, index) => (
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
  );
}
