from pydantic import BaseModel, ConfigDict

class DeleteSchema(BaseModel):
    status_process: str = "Done"

    model_config = ConfigDict(from_attributes=True)