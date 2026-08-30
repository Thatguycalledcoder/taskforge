from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(max_length=255)
    status: str = Field(max_length=50)


class JobCreate(JobBase):
    user_id: int


class JobUpdate(BaseModel):
    title: str | None
    description: str | None
    status: str | None


class JobResponse(JobBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
