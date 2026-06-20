import { api } from "./api";

import { Artifact } from "@/types/artifact";

export async function getArtifacts(
  projectId: number
): Promise<Artifact[]> {

  const response = await api.get(
    `/artifacts/project/${projectId}`
  );

  return response.data;
}

export async function getArtifact(
  artifactId: number
): Promise<Artifact> {

  const response = await api.get(
    `/artifacts/${artifactId}`
  );

  return response.data;
}