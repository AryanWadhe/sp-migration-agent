"use client";

import { Artifact }
from "@/types/artifact";

import { GeneratedArtifact }
from "@/types/generated-artifact";

export default function MigrationWorkspace({
  artifact,
  generated,
}: {
  artifact: Artifact;
  generated: GeneratedArtifact;
}) {

  return (

    <div className="space-y-6">

      <h1 className="text-3xl font-bold">
        Migration Workspace
      </h1>

      <div className="grid grid-cols-2 gap-6">

        <div className="border rounded-lg p-4">

          <h2 className="font-semibold mb-4">
            Original SQL
          </h2>

          <pre className="overflow-auto whitespace-pre-wrap text-sm">
            {artifact.original_content}
          </pre>

        </div>

        <div className="border rounded-lg p-4">

          <h2 className="font-semibold mb-4">
            Generated dbt
          </h2>

          <pre className="overflow-auto whitespace-pre-wrap text-sm">
            {generated.content}
          </pre>

        </div>

      </div>

    </div>
  );
}