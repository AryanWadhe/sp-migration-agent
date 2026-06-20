import ArtifactList from "@/components/project/artifact-list";
import UploadForm from "@/components/upload/upload-form";
import GeneratedList from "@/components/generated/generated-list";

export default async function ProjectPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <main className="max-w-5xl mx-auto p-10">
      <h1 className="text-3xl font-bold">Project {id}</h1>

      <UploadForm projectId={Number(id)} />

      <div className="mt-8">
        <ArtifactList projectId={Number(id)} />
      </div>

      <div className="mt-8">
        <GeneratedList projectId={Number(id)} />
      </div>
    </main>
  );
}
