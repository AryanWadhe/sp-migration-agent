import { api } from "./api";
import { Project } from "@/types/project";

export async function getProjects(): Promise<Project[]> {
  const response = await api.get("/projects");
  return response.data;
}