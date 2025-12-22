from uuid import UUID
from fastapi import APIRouter

from .schema import Folder

router = APIRouter("/folders")


@router.get("/{folder_id}", name="Retrieve a folder by UUID")
def get_folder_route(
    folder_id: UUID,
) -> Folder:
    pass


@router.post("/", name="Create a new folder")
def create_folder_route() -> Folder:
    pass


@router.delete(
    "/{folder_id}",
    name="Delete a folder",
)
def delete_folder_route(
    folder_id: UUID,
):
    pass
