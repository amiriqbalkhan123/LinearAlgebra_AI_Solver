
import axios from "axios";

export type MatrixOperation =
  | "addition"
  | "subtraction"
  | "multiplication"
  | "determinant"
  | "inverse"
  | "transpose"
  | "rank"
  | "ref"
  | "rref";

export type MatrixData = string[][];

export interface MatrixRequest {
  matrix: MatrixData;
  matrix_b?: MatrixData;
  operation: MatrixOperation;
}


export interface SolutionStep {
  description: string;
  operation: string | null;
  latex: string;
}

export interface MatrixResponse {
  operation: MatrixOperation;
  input_latex: string;
  matrix_b_latex: string | null;
  result: string;
  result_latex: string;
  steps: SolutionStep[];
  verified: boolean;
}


export const api = axios.create({
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
