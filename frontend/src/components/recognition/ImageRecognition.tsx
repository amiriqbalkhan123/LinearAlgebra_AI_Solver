
import { useEffect, useState } from "react";
import axios from "axios";
import {
  ImageUp,
  ScanText,
  CheckCircle2,
} from "lucide-react";

import MathDisplay from "../math/MathDisplay";

import {
  recognizeImage,
  type RecognitionMode,
  type RecognitionResponse,
} from "../../services/recognitionApi";


export default function ImageRecognition() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");

  const [mode, setMode] =
    useState<RecognitionMode>("formula");

  const [result, setResult] =
    useState<RecognitionResponse | null>(null);

  const [editedText, setEditedText] = useState("");
  const [confirmed, setConfirmed] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!file) {
      setPreview("");
      return;
    }

    const url = URL.createObjectURL(file);
    setPreview(url);

    return () => URL.revokeObjectURL(url);
  }, [file]);

  function selectFile(next: File | null) {
    setFile(next);
    setResult(null);
    setEditedText("");
    setConfirmed(false);
    setError("");
  }

  async function handleRecognize() {
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);
    setConfirmed(false);

    try {
      const response = await recognizeImage(file, mode);

      setResult(response);
      setEditedText(response.recognized_text);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;

        setError(
          typeof detail === "string"
            ? detail
            : "OCR processing failed."
        );
      } else {
        setError("Unexpected recognition error.");
      }
    } finally {
      setLoading(false);
    }
  }

  const inputClass =
    "w-full rounded-lg border border-zinc-700 bg-zinc-800 p-3";

  return (
    <section className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold">
          Image & Handwriting Recognition
        </h2>

        <p className="mt-2 text-sm text-zinc-400">
          Upload a mathematical question, recognize
          its content, and correct the transcription.
        </p>
      </header>

      <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
        <label className="block space-y-2">
          <span className="font-medium">
            Recognition Mode
          </span>

          <select
            value={mode}
            onChange={(event) => {
              setMode(event.target.value as RecognitionMode);
              setResult(null);
              setConfirmed(false);
              setError("");
            }}
            className={inputClass}
          >
            <option value="formula">
              Mathematical Formula (pix2tex)
            </option>
            <option value="text">
              Printed Question Text (Tesseract)
            </option>
          </select>
        </label>

        <label className="block space-y-2">
          <span className="font-medium">
            Upload Question Image
          </span>

          <div className="rounded-lg border border-dashed border-zinc-600 p-6 text-center">
            <ImageUp
              className="mx-auto mb-3 text-blue-400"
              size={32}
            />

            <input
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(event) =>
                selectFile(event.target.files?.[0] ?? null)
              }
              className="w-full text-sm text-zinc-300"
            />

            <p className="mt-3 text-xs text-zinc-500">
              PNG, JPEG or WEBP — maximum 5 MB.
              Crop the question before uploading
              for better recognition.
            </p>
          </div>
        </label>

        {preview && (
          <div className="rounded-lg bg-zinc-950 p-4">
            <h3 className="mb-3 font-medium">
              Original Image
            </h3>

            <img
              src={preview}
              alt="Uploaded mathematical question"
              className="mx-auto max-h-96 max-w-full object-contain"
            />
          </div>
        )}

        <button
          type="button"
          disabled={!file || loading}
          onClick={handleRecognize}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 p-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          <ScanText size={18} />
          {loading ? "Recognizing..." : "Recognize Question"}
        </button>
      </section>

      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-900 bg-red-950 p-4 text-red-300"
        >
          {error}
        </div>
      )}

      {result && (
        <section className="space-y-5 rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <h3 className="text-xl font-semibold">
            Recognition Results
          </h3>

          <p className="rounded-lg border border-amber-900 bg-amber-950 p-3 text-sm text-amber-200">
            {result.warning}
          </p>

          <label className="block space-y-2">
            <span className="font-medium">
              Correct the Recognized Content
            </span>

            <textarea
              rows={6}
              value={editedText}
              onChange={(event) => {
                setEditedText(event.target.value);
                setConfirmed(false);
              }}
              className={inputClass}
              spellCheck={false}
            />
          </label>

          {mode === "formula" && editedText.trim() && (
            <div className="rounded-lg bg-zinc-950 p-4">
              <h4 className="mb-3 font-medium">
                Mathematical Preview
              </h4>

              <MathDisplay latex={editedText} />
            </div>
          )}

          <button
            type="button"
            disabled={!editedText.trim()}
            onClick={() => setConfirmed(true)}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-green-700 p-3 font-semibold hover:bg-green-600 disabled:opacity-50"
          >
            <CheckCircle2 size={18} />
            Confirm Transcription
          </button>

          {confirmed && (
            <div
              role="status"
              className="rounded-lg border border-green-900 bg-green-950 p-4 text-sm text-green-300"
            >
              Transcription confirmed locally.
              The next phase will convert this
              content into a structured problem
              and send it to the mathematical solver.
            </div>
          )}
        </section>
      )}
    </section>
  );
}
