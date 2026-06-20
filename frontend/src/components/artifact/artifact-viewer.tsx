"use client";

import { Artifact } from "@/types/artifact";

export default function ArtifactViewer({
  artifact
}: {
  artifact: Artifact
}) {

  return (
    <div className="space-y-6">

      <div className="border rounded-lg p-4">

        <h2 className="text-xl font-semibold">
          {artifact.file_name}
        </h2>

        <p className="text-sm text-gray-500">
          Status: {artifact.status}
        </p>

      </div>

      <div className="border rounded-lg p-4">

        <h3 className="font-semibold mb-3">
          Original SQL
        </h3>

        <pre className="overflow-auto text-sm whitespace-pre-wrap">
          {artifact.original_content}
        </pre>

      </div>

    </div>
  );
}