"use client";

import { GeneratedArtifact } from "@/types/generated-artifact";

import {
  getDownloadUrl,
} from "@/services/generated-api";

export default function GeneratedViewer({
  artifact,
}: {
  artifact: GeneratedArtifact;
}) {
  return (
    <div className="space-y-6">
      <div className="border rounded p-4">
        <h1 className="text-2xl font-bold">
          {artifact.model_name}
        </h1>

        <p className="text-sm text-gray-500">
          {artifact.artifact_type}
        </p>
      </div>

      <div className="border rounded p-4">
        <h2 className="font-semibold mb-4">
          Generated dbt Model
        </h2>

        <pre className="overflow-auto whitespace-pre-wrap text-sm">
          {artifact.content}
        </pre>
      </div>

      <a
        href={getDownloadUrl(
          artifact.generated_artifact_id
        )}
        target="_blank"
        rel="noopener noreferrer"
      >
        <button className="px-4 py-2 border rounded hover:bg-gray-100">
          Download SQL
        </button>
      </a>
    </div>
  );
}