
import { api, type MatrixData } from "./api";

export type VectorSpaceOperation =
  | "column_space"
  | "row_space"
  | "null_space"
  | "left_null_space"
  | "rank_nullity"
  | "independence";

export interface VectorSpaceStep {
  description: string;
  latex: string;
}

export interface VectorSpaceResponse {
  operation: VectorSpaceOperation;
  name: string;
  input_latex: string;
  rref_latex: string;
  pivot_columns: number[];
  rank: number;
  nullity: number;
  dimension: number | null;
  ambient_dimension: number | null;
  basis: string[][];
  basis_latex: string[];
  is_independent: boolean | null;
  steps: VectorSpaceStep[];
  verified: boolean;
}

export async function solveVectorSpace(
  matrix: MatrixData,
  operation: VectorSpaceOperation
): Promise<VectorSpaceResponse> {
  const { data } = await api.post<VectorSpaceResponse>(
    "/vector-spaces/solve",
    { matrix, operation }
  );

  return data;
}
