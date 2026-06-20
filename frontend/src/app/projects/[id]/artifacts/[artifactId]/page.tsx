import ArtifactViewer from "@/components/artifact/artifact-viewer";

import {
  getArtifact
} from "@/services/artifact-api";

export default async function ArtifactPage({
  params
}: {
  params: Promise<{
    id: string;
    artifactId: string;
  }>;
}) {

  const {
    artifactId
  } = await params;

  const artifact =
    await getArtifact(
      Number(artifactId)
    );

  return (
    <main className="p-10">

      <ArtifactViewer
        artifact={artifact}
      />

    </main>
  );
}