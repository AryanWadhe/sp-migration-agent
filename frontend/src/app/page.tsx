import ProjectList from "@/components/dashboard/project-list";

export default function HomePage() {
  return (
    <main className="p-10">
      <h1 className="text-4xl font-bold">
        Migration Copilot
      </h1>

      <p className="mt-2 text-gray-500">
        Stored Procedure → dbt Migration Platform
      </p>

      <div className="mt-8">
        <ProjectList />
      </div>
    </main>
  );
}