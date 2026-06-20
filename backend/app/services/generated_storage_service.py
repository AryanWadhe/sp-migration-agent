from pathlib import Path


class GeneratedStorageService:

    BASE_PATH = Path(
        "storage/generated"
    )

    @staticmethod
    def save_model(
        project_id: int,
        model_name: str,
        content: str
    ) -> str:

        folder = (
            GeneratedStorageService.BASE_PATH
            / f"project_{project_id}"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            folder
            / f"{model_name}.sql"
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(file_path)