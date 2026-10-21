
import { api } from "./api";
import type { MatrixData } from "./api";

export type SystemClassification =
  | "unique"
  | "infinite"
  | "no_solution";

export interface SystemStep {
  description: string;
  operation: string | null;
  latex: string;
}

export interface LinearSystemResponse {
  classification: SystemClassification;
  rank_a: number;
  rank_augmented: number;
  unknowns: number;
  equations: number;
  free_variables: string[];
  input_latex: string;
  rref_latex: string;
  solution_latex: string | null;
  solution: string[] | null;
  steps: SystemStep[];
  verified: boolean;
}

export async function solveLinearSystem(
  matrix: MatrixData,
  constants: string[]
): Promise<LinearSystemResponse> {
  const response = await api.post<LinearSystemResponse>(
    "/systems/solve",
    { matrix, constants }
  );

  return response.data;
}
