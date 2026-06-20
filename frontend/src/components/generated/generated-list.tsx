"use client";

import { useEffect, useState } from "react";

import {
  getGeneratedArtifacts,
  getGeneratedArtifact,
} from "@/services/generated-api";

import {
  GeneratedArtifact,
} from "@/types/generated-artifact";

import GeneratedViewer from "./generated-viewer";

export default function GeneratedList({
  projectId,
}: {
  projectId: number;
}) {
  const [items, setItems] =
    useState<GeneratedArtifact[]>([]);

  const [selected, setSelected] =
    useState<GeneratedArtifact | null>(
      null
    );

  useEffect(() => {
    async function load() {
      try {
        const data =
          await getGeneratedArtifacts(
            projectId
          );

        setItems(data);

        if (data.length > 0) {
          const firstArtifact =
            await getGeneratedArtifact(
              data[0]
                .generated_artifact_id
            );

          setSelected(firstArtifact);
        }
      } catch (error) {
        console.error(error);
      }
    }

    load();
  }, [projectId]);

  async function viewArtifact(
    generatedArtifactId: number
  ) {
    try {
      const artifact =
        await getGeneratedArtifact(
          generatedArtifactId
        );

      setSelected(artifact);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">
        Generated Models
      </h2>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-3">
          {items.map((item) => (
            <div
              key={
                item.generated_artifact_id
              }
              className="border rounded p-3"
            >
              <div className="font-medium">
                {item.model_name}
              </div>

              <div className="text-sm text-gray-500">
                Generated Artifact #
                {
                  item.generated_artifact_id
                }
              </div>

              <button
                className="mt-2 border px-3 py-1 rounded hover:bg-gray-100"
                onClick={() =>
                  viewArtifact(
                    item.generated_artifact_id
                  )
                }
              >
                View
              </button>
            </div>
          ))}
        </div>

        <div>
          {selected ? (
            <GeneratedViewer
              artifact={selected}
            />
          ) : (
            <div className="border rounded p-6 text-gray-500">
              Select a generated model
            </div>
          )}
        </div>
      </div>
    </div>
  );
}