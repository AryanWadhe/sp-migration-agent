from pydantic import BaseModel


class JoinCondition(BaseModel):
    join_type: str
    left_table: str | None = None
    left_column: str | None = None
    right_table: str | None = None
    right_column: str | None = None
    condition: str | None = None


class ParserResult(BaseModel):

    source_tables: list[str] = []
    target_tables: list[str] = []

    views: list[str] = []
    functions: list[str] = []

    joins: list[JoinCondition] = []

    filters: list[str] = []

    aggregations: list[dict] = []