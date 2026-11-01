from pydantic import BaseModel, ConfigDict


class CoreModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        populate_by_name=True,
        use_enum_values=True,
    )
