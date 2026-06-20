import { api } from "./api";
import { GeneratedArtifact } from "@/types/generated-artifact";

export async function getGeneratedArtifacts(
  projectId: number
): Promise<GeneratedArtifact[]> {

  const response = await api.get(
    `/generated-artifacts/project/${projectId}`
  );

  return response.data;
}

export async function getGeneratedArtifact(
  generatedArtifactId: number
): Promise<GeneratedArtifact> {

  const response = await api.get(
    `/generated-artifacts/${generatedArtifactId}`
  );

  return response.data;
}

export function getDownloadUrl(
  generatedArtifactId: number
): string {

  return (
    `${process.env.NEXT_PUBLIC_API_URL}` +
    `/generated-artifacts/${generatedArtifactId}/download`
  );
}

export async function getGeneratedArtifactByArtifactId(
  artifactId: number
) {

  const response = await api.get(
    `/generated-artifacts/artifact/${artifactId}`
  );

  return response.data;
}


