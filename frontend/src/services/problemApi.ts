
import { api } from "./api";

export type ProblemDomain =
  | "matrices"
  | "linear_systems"
  | "vector_spaces"
  | "vector_geometry"
  | "eigenanalysis"
  | "decompositions";

export interface UnifiedProblemRequest {
  domain: ProblemDomain;
  data: Record<string, unknown>;
}

export interface UnifiedProblemResponse {
  domain: ProblemDomain;
  status: "success";
  verified: boolean;
  result: Record<string, unknown>;
}

export async function solveUnifiedProblem(
  problem: UnifiedProblemRequest
): Promise<UnifiedProblemResponse> {
  const { data } = await api.post<UnifiedProblemResponse>(
    "/problems/solve",
    problem
  );

  return data;
}
