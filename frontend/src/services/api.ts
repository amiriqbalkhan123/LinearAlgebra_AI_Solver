
import axios from "axios";

export type MatrixOperation =
  | "determinant"
  | "rank"
  | "rref"
  | "transpose";

export interface MatrixRequest {
  matrix: number[][];
  operation: MatrixOperation;
}

export interface MatrixResponse {
  operation: MatrixOperation;
  input_latex: string;
  result: string;
  result_latex: string;
}

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 30000,
});

export async function solveMatrix(
  request: MatrixRequest
): Promise<MatrixResponse> {
  const response = await api.post<MatrixResponse>(
    "/solve/matrix",
    request
  );

  return response.data;
}
