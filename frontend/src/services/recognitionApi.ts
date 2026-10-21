
import { api } from "./api";

export type RecognitionMode = "text" | "formula";

export interface RecognitionResponse {
  mode: RecognitionMode;
  recognized_text: string;
  recognized_latex: string | null;
  requires_confirmation: boolean;
  warning: string;
}

export async function recognizeImage(
  file: File,
  mode: RecognitionMode
): Promise<RecognitionResponse> {
  const data = new FormData();

  data.append("file", file);
  data.append("mode", mode);

  const response = await api.post<RecognitionResponse>(
    "/recognition/recognize",
    data,
    {
      timeout: 120000,
    }
  );

  return response.data;
}
