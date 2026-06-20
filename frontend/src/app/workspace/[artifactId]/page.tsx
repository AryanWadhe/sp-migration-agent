import MigrationWorkspace
from "@/components/workspace/migration-workspace";

import {
  getArtifact
} from "@/services/artifact-api";

import {
  getGeneratedArtifactByArtifactId
} from "@/services/generated-api";

export default async function WorkspacePage({
  params,
}: {
  params: Promise<{
    artifactId: string;
  }>;
}) {

  const { artifactId } =
    await params;

  const artifact =
    await getArtifact(
      Number(artifactId)
    );

  const generated =
    await getGeneratedArtifactByArtifactId(
      Number(artifactId)
    );

  return (
    <main className="p-8">

      <MigrationWorkspace
        artifact={artifact}
        generated={generated}
      />

    </main>
  );
}