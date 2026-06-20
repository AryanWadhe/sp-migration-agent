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

    <div className="grid grid-cols-2 gap-6">

      <div className="border rounded p-4">

        <h2 className="font-bold mb-4">
          Original SQL
        </h2>

        <pre>
          {artifact.original_content}
        </pre>

      </div>

      <div className="border rounded p-4">

        <h2 className="font-bold mb-4">
          Generated dbt
        </h2>

        <pre>
          {generated.content}
        </pre>

      </div>

    </div>

  );
}