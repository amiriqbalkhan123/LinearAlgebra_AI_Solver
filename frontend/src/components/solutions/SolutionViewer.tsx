
import { useState } from "react";
import {
  CheckCircle2,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

import type { MatrixResponse } from "../../services/api";
import MathDisplay from "../math/MathDisplay";

interface SolutionViewerProps {
  solution: MatrixResponse;
}

export default function SolutionViewer({
  solution,
}: SolutionViewerProps) {
  const [showSteps, setShowSteps] = useState(true);

  return (
    <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold">
          Mathematical Solution
        </h2>

        {solution.verified && (
          <span className="flex items-center gap-2 rounded-full bg-green-950 px-3 py-1 text-sm text-green-400">
            <CheckCircle2 size={16} />
            Verified
          </span>
        )}
      </div>

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

      <div className="rounded-lg border border-green-900 bg-zinc-950 p-4">
        <h3 className="mb-3 font-semibold text-green-400">
          Final Answer
        </h3>
        <MathDisplay latex={solution.result_latex} />
      </div>

      {solution.steps.length > 0 && (
        <div className="border-t border-zinc-800 pt-5">
          <button
            type="button"
            onClick={() => setShowSteps((prev) => !prev)}
            aria-expanded={showSteps}
            className="flex w-full items-center justify-between text-left"
          >
            <h3 className="text-lg font-semibold">
              Step-by-Step Solution
              <span className="ml-2 text-sm font-normal text-zinc-500">
                ({solution.steps.length} steps)
              </span>
            </h3>

            {showSteps ? (
              <ChevronUp size={20} />
            ) : (
              <ChevronDown size={20} />
            )}
          </button>

          {showSteps && (
            <div className="mt-5 space-y-4">
              {solution.steps.map((step, index) => (
                <article
                  key={index}
                  className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                >
                  <div className="mb-3 flex items-start gap-3">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-900 text-xs font-semibold text-blue-200">
                      {index + 1}
                    </span>

                    <p className="pt-1 text-sm text-zinc-200">
                      {step.description}
                    </p>
                  </div>

                  <div className="overflow-x-auto rounded-md bg-zinc-900 p-3">
                    <MathDisplay latex={step.latex} />
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
