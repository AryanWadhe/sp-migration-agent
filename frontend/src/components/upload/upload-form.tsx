"use client";

import { useState } from "react";

import {
  uploadAndGenerate
} from "@/services/upload-api";

export default function UploadForm({
  projectId
}: {
  projectId: number;
}) {

  const [file, setFile] =
    useState<File | null>(null);

  const [loading, setLoading] =
    useState(false);

  async function handleUpload() {

    if (!file) return;

    setLoading(true);

    try {

      const result =
        await uploadAndGenerate(
          projectId,
          "stored_procedure",
          file
        );

      alert(
        `Generated ${result.target_model}`
      );

      window.location.reload();

    } finally {

      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">

      <input
        type="file"
        accept=".sql"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] ?? null
          )
        }
      />

      <button
        onClick={handleUpload}
        disabled={loading}
        className="border px-4 py-2 rounded"
      >
        {loading
          ? "Generating..."
          : "Upload & Generate"}
      </button>

    </div>
  );
}