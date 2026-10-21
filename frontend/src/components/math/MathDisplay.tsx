
import { useMemo } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

interface MathDisplayProps {
  latex: string;
  block?: boolean;
}

export default function MathDisplay({
  latex,
  block = true,
}: MathDisplayProps) {
  const html = useMemo(
    () =>
      katex.renderToString(latex, {
        displayMode: block,
        throwOnError: false,
        trust: false,
        strict: "warn",
      }),
    [latex, block]
  );

  return (
    <div
      className="overflow-x-auto py-2"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
