import GeneratedViewer
from "@/components/generated/generated-viewer";

import {
  getGeneratedArtifact
} from "@/services/generated-api";

export default async function GeneratedArtifactPage({
  params,
}: {
  params: Promise<{
    id: string;
  }>;
}) {

  const { id } = await params;

  const artifact =
    await getGeneratedArtifact(
      Number(id)
    );

  return (
    <main className="p-10">

      <GeneratedViewer
        artifact={artifact}
      />

    </main>
  );
}