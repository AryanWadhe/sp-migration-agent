export interface Artifact {
  artifact_id: number;
  project_id: number;
  file_name: string;
  artifact_type: string;
  status: string;
  original_content: string;
  file_size: number;
  content_hash: string;
  storage_path?: string;
  created_at: string;
  updated_at: string;
}