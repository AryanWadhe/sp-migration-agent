
from app.repositories.artifact_repository import (
    ArtifactRepository
)

from app.services.migration_context_service import (
    MigrationContextService
)

from app.services.dbt_generation_service import (
    DBTGenerationService
)

from app.services.generated_artifact_service import (
    GeneratedArtifactService
)
from app.services.generated_storage_service import (
    GeneratedStorageService
)


class ArtifactDBTGenerationService:

    @staticmethod
    def generate(
        db,
        artifact_id: int
    ):

        artifact = (
            ArtifactRepository.get_by_id(
                db,
                artifact_id
            )
        )

        if not artifact:
            raise ValueError(
                "Artifact not found"
            )
            
        print("=" * 80)
        print("ARTIFACT CONTENT")
        print("=" * 80)
        print(artifact.original_content)

        print("=" * 80)
        print("MIGRATION CONTEXT")
        print("=" * 80)

        context = (
            MigrationContextService.build_context(
                artifact.original_content
            )
        )
        # ArtifactDBTGenerationService.generate()
        # print(context)

        generated_result = (
            DBTGenerationService.generate(
                context
            )
        )
        model_name = ( generated_result["target_model"])
        
        project_id = artifact.project_id

        storage_path = (
            GeneratedStorageService.save_model(
                project_id=project_id,
                model_name=model_name,
                content=generated_result[
                    "dbt_sql"
                ]
            )
        )
        print("GENERATED RESULT")
        print(generated_result)

        generated_artifact = (
            GeneratedArtifactService.create_dbt_model(
                db=db,
                artifact_id=artifact_id,
                model_name=model_name,
                storage_path=storage_path,
                dbt_sql=generated_result[
                    "dbt_sql"
                ]
)
        )

        return {
            "generated_artifact_id":
                generated_artifact.generated_artifact_id,

            "target_model":
                generated_result["target_model"],

            "dbt_sql":
                generated_result["dbt_sql"]
        }