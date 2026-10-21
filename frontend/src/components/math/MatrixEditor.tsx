
import type { MatrixData } from "../../services/api";

interface MatrixEditorProps {
  name: string;
  matrix: MatrixData;
  onChange: (matrix: MatrixData) => void;
}

export default function MatrixEditor({
  name,
  matrix,
  onChange,
}: MatrixEditorProps) {
  const rows = matrix.length;
  const cols = matrix[0].length;

  function resizeMatrix(newRows: number, newCols: number) {
    const updated = Array.from(
      { length: newRows },
      (_, rowIndex) =>
        Array.from(
          { length: newCols },
          (_, colIndex) =>
            matrix[rowIndex]?.[colIndex] ?? "0"
        )
    );

    onChange(updated);
  }

  function updateCell(
    rowIndex: number,
    colIndex: number,
    value: string
  ) {
    const updated = matrix.map((row) => [...row]);
    updated[rowIndex][colIndex] = value;
    onChange(updated);
  }

  return (
    <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <h2 className="mb-4 text-lg font-semibold">
        Matrix {name}
      </h2>

      <div className="mb-5 flex flex-wrap gap-4">
        <label className="flex items-center gap-2 text-sm">
          Rows
          <select
            value={rows}
            onChange={(event) =>
              resizeMatrix(Number(event.target.value), cols)
            }
            className="rounded border border-zinc-700 bg-zinc-800 p-2"
          >
            {Array.from({ length: 10 }, (_, i) => i + 1).map(
              (n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              )
            )}
          </select>
        </label>

        <label className="flex items-center gap-2 text-sm">
          Columns
          <select
            value={cols}
            onChange={(event) =>
              resizeMatrix(rows, Number(event.target.value))
            }
            className="rounded border border-zinc-700 bg-zinc-800 p-2"
          >
            {Array.from({ length: 10 }, (_, i) => i + 1).map(
              (n) => (
                <option key={n} value={n}>
                  {n}
                </option>
              )
            )}
          </select>
        </label>
      </div>

      <div className="overflow-x-auto">
        <div className="inline-flex min-w-full items-stretch gap-2">
          <div className="w-1.5 rounded-l-lg border-l-2 border-y-2 border-zinc-400" />

          <div
            className="grid flex-1 gap-2"
            style={{
              gridTemplateColumns: `repeat(${cols}, minmax(72px, 1fr))`,
            }}
          >
            {matrix.map((row, rowIndex) =>
              row.map((value, colIndex) => (
                <input
                  key={`${rowIndex}-${colIndex}`}
                  aria-label={`${name} row ${rowIndex + 1} column ${colIndex + 1}`}
                  type="text"
                  inputMode="decimal"
                  value={value}
                  onChange={(event) =>
                    updateCell(
                      rowIndex,
                      colIndex,
                      event.target.value
                    )
                  }
                  className="w-full min-w-0 rounded-md border border-zinc-700 bg-zinc-800 p-2 text-center text-sm outline-none focus:border-blue-500"
                  placeholder="0"
                />
              ))
            )}
          </div>

          <div className="w-1.5 rounded-r-lg border-r-2 border-y-2 border-zinc-400" />
        </div>
      </div>

      <p className="mt-3 text-xs text-zinc-500">
        Supported values: 5, -3, 1/2, -7/4, 0.125
      </p>
    </section>
  );
}
