## Pydantic v1 vs Pydantic v2

- `.dict()` function is now renamed to `.model_dump()`

- `schema_extra` function within a Config class is now renamed to `json_schema_extra`

- `Optional` variables need a `=None` example: id: Optional[int] = None