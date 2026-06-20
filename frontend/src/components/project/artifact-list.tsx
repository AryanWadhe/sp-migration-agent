"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { Artifact } from "@/types/artifact";
import { getArtifacts } from "@/services/artifact-api";

export default function ArtifactList({
  projectId,
}: {
  projectId: number;
}) {
  const [artifacts, setArtifacts] =
    useState<Artifact[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    async function loadArtifacts() {
      try {
        const data =
          await getArtifacts(projectId);

        setArtifacts(data);
      } finally {
        setLoading(false);
      }
    }

    loadArtifacts();
  }, [projectId]);

  if (loading) {
    return <p>Loading artifacts...</p>;
  }

  return (
    <div className="space-y-3">
      <h2 className="text-xl font-semibold">
        Artifacts
      </h2>

      {artifacts.map((artifact) => (
        <Link
          key={artifact.artifact_id}
          href={`/workspace/${artifact.artifact_id}`}
        >
          <div className="border rounded p-3 hover:bg-gray-50 cursor-pointer transition">
            <div className="font-medium">
              {artifact.file_name}
            </div>

            <div className="text-sm text-gray-500">
              {artifact.status}
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}