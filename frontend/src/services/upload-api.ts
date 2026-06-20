import { api } from "./api";

export async function uploadAndGenerate(
  projectId: number,
  artifactType: string,
  file: File
) {

  const formData = new FormData();

  formData.append(
    "project_id",
    projectId.toString()
  );

  formData.append(
    "artifact_type",
    artifactType
  );

  formData.append(
    "file",
    file
  );

  const response =
    await api.post(
      "/artifacts/upload-and-generate",
      formData
    );

  return response.data;
}