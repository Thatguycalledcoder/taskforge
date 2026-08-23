from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    description: str
    status: str


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
