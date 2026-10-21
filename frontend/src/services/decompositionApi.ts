
import { api, type MatrixData } from "./api";

export type DecompositionOperation =
  | "lu"
  | "qr"
  | "svd"
  | "pseudoinverse"
  | "least_squares"
  | "spectral"
  | "positive_definite";

export interface DecompositionRequest {
  matrix: MatrixData;
  operation: DecompositionOperation;
  constants?: string[];
}

export interface DecompositionResponse {
  operation: DecompositionOperation;
  mode: "exact" | "numerical";
  input_latex: string;
  factors: {
    name: string;
    latex: string;
  }[];
  metrics: {
    name: string;
    value: string;
  }[];
  steps: {
    description: string;
    latex: string;
  }[];
  verified: boolean;
}

export async function analyzeDecomposition(
  request: DecompositionRequest
): Promise<DecompositionResponse> {
  const { data } = await api.post<DecompositionResponse>(
    "/decompositions/analyze",
    request
  );

  return data;
}
