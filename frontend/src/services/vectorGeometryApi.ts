
import { api } from "./api";

export type VectorOperation =
  | "addition"
  | "subtraction"
  | "scalar"
  | "dot"
  | "cross"
  | "outer"
  | "magnitude"
  | "normalize"
  | "distance"
  | "angle"
  | "orthogonality"
  | "projection"
  | "span_membership"
  | "gram_schmidt";

export interface VectorGeometryRequest {
  operation: VectorOperation;
  a?: string[];
  b?: string[];
  scalar?: string;
  vectors?: string[][];
  target?: string[];
  normalize_basis?: boolean;
}

export interface VectorGeometryResponse {
  operation: VectorOperation;
  result: string | string[] | boolean;
  result_latex: string;
  verified: boolean;
  steps: {
    description: string;
    latex: string;
  }[];
}

export async function solveVectorGeometry(
  request: VectorGeometryRequest
): Promise<VectorGeometryResponse> {
  const response = await api.post<VectorGeometryResponse>(
    "/vector-geometry/solve",
    request
  );

  return response.data;
}
