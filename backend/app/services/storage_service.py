from pathlib import Path


class StorageService:

    STORAGE_ROOT = Path("storage")

    @classmethod
    def get_project_folder(
        cls,
        project_id: int
    ) -> Path:

        folder = cls.STORAGE_ROOT / f"project_{project_id}"

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder

    @classmethod
    def save_sql_file(
        cls,
        project_id: int,
        file_name: str,
        content: str
    ) -> str:

        folder = cls.get_project_folder(
            project_id
        )

        file_path = folder / file_name

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(file_path)