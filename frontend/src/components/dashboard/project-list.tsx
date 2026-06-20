"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { getProjects } from "@/services/project-api";
import { Project } from "@/types/project";

export default function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  if (loading) {
    return <p>Loading projects...</p>;
  }

  return (
    <div className="space-y-4">
      {projects.map((project) => (
        <Link
          href={`/projects/${project.project_id}`}
          key={project.project_id}
        >
          <div className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <h2 className="font-semibold">
              {project.name}
            </h2>

            <p className="text-sm text-gray-500">
              {project.description}
            </p>
          </div>
        </Link>
      ))}
    </div>
  );
}