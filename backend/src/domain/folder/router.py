from uuid import UUID
from fastapi import APIRouter

from .schema import Folder

router = APIRouter("/folders")


@router.get(
    "/{folder_id}",
)
def get_folder_route(
    folder_id: UUID,
) -> Folder:
    pass
