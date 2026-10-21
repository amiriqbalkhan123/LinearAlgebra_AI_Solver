
import { api, type MatrixData } from "./api";

export interface EigenvalueData {
  value: string;
  value_latex: string;
  algebraic_multiplicity: number;
  geometric_multiplicity: number;
  basis: string[][];
  basis_latex: string[];
  verified: boolean;
}

export interface EigenStep {
  description: string;
  latex: string;
}

export interface EigenanalysisResponse {
  input_latex: string;
  characteristic_polynomial: string;
  characteristic_latex: string;
  factored_latex: string;
  eigenvalues: EigenvalueData[];
  diagonalizable: boolean;
  P_latex: string | null;
  D_latex: string | null;
  trace: string;
  determinant: string;
  steps: EigenStep[];
  verified: boolean;
}

export async function analyzeEigen(
  matrix: MatrixData
): Promise<EigenanalysisResponse> {
  const response = await api.post<EigenanalysisResponse>(
    "/eigenanalysis/analyze",
    { matrix }
  );

  return response.data;
}
