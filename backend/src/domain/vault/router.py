from typing import Annotated
from fastapi import APIRouter, Depends, Path
from uuid import UUID
from src.core.security import oauth2_scheme
from src.domain.user.service import get_user_service, UserService
from .schema import Vault, CreateVault, VaultUser
from src.domain.user.schema import User, UserID
from .service import get_vault_service, VaultService

VAULTS_TAG = "Vaults"
router = APIRouter(prefix="/vaults", tags=[VAULTS_TAG])


@router.get(
    "/",
    name="Get all vaults accessible to the user",
    description="Get all vaults owned by (or shared with) the user",
    response_model=list[Vault],
)
def get_all_user_vaults_route(
    shared: bool = True,
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
) -> list[Vault]:
    user: User = user_service.get_user_from_token(token)
    vaults: list[Vault] = vault_service.get_vaults_by_user(user.id)
    if shared:
        vaults += vault_service.get_shared_vaults(user.id)
    return vaults


@router.get(
    "/shared",
    name="Get all vaults shared with the user",
    description="Get all vaults or shared with the user",
    response_model=list[Vault],
)
def get_shared_user_vaults_route(
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
) -> list[Vault]:
    user: User = user_service.get_user_from_token(token)
    return vault_service.get_shared_vaults(user.id)


@router.get(
    "/{vault_id}",
    name="Get the provided vault",
    description="Get the vault with provided ID if it exists\
        and the user is authorised to view it",
    response_model=Vault,
)
def get_vault_route(
    vault_id: UUID,
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
) -> Vault:
    user: User = user_service.get_user_from_token(token)
    return vault_service.get_vault_by_id(vault_id, user.id)


@router.get("/{vault_id}/folders", name="Get all folders in a vault")
def get_vault_folders_route(
    vault_id: UUID,
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
):
    user: User = user_service.get_user_from_token(token)
    return vault_service.get_vault_folders(vault_id, user.id)


@router.post(
    "/",
    name="Create a new vault owned by user",
    response_model=Vault,
    status_code=201,
)
def create_new_user_vault_route(
    body: CreateVault,
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
) -> Vault:
    user: User = user_service.get_user_from_token(token)
    return vault_service.create_vault(body, user.id)


@router.post(
    "/{vault_id}/shares/",
    name="Grant a user access to the vault",
    status_code=200,
)
def share_vault_with_user_route(
    body: UserID,
    vault_id=Annotated[UUID, Path(title="ID of the current vault")],
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
) -> VaultUser:
    user: User = user_service.get_user_from_token(token)
    return vault_service.share_vault_with_user(
        vault_id,
        user,
        body.user_id,
    )


@router.post("/{vault_id}/folders")
def add_folder_to_vault():
    pass


@router.delete(
    "/{vault_id}/shares/{user_id}",
    name="Remove a user from a vault share",
    status_code=204,
)
def unshare_vault_with_user_route(
    vault_id=Annotated[UUID, Path(title="ID of the vault")],
    user_id=Annotated[UUID, Path(title="ID of the user")],
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
):
    auth_user: User = user_service.get_user_from_token(token)
    return vault_service.unshare_vault_with_user(
        vault_id,
        auth_user,
        user_id,
    )


@router.delete(
    "/{vault_id}",
    name="Delete the vault provided",
    description="Delete the vault provided if permitted to do so",
    status_code=204,
)
def delete_vault_route(
    vault_id: UUID,
    token: str = Depends(oauth2_scheme),
    vault_service: VaultService = Depends(get_vault_service),
    user_service: UserService = Depends(get_user_service),
):
    user: User = user_service.get_user_from_token(token)
    return vault_service.delete_vault(vault_id, user.id)


@router.delete("/{vault_id}/folders/{folder_id}")
def delete_folder_from_vault():
    pass
