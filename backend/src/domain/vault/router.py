from typing import Annotated
from fastapi import APIRouter, Depends, Path
from uuid import UUID
from src.core.security import oauth2_scheme
from src.core.db import get_session
from .schema import Vault, CreateVault, VaultUser
from src.domain.user.schema import User, UserID
from src.domain.user.service import user_service
from .service import vault_service
from src.interfaces.db_session import DBSession

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
    session: DBSession = Depends(get_session),
) -> list[Vault]:
    user: User = user_service.get_user_from_token(session, token)
    vaults: list[Vault] = vault_service.get_vaults_by_user(session, user.id)
    if shared:
        vaults += vault_service.get_shared_vaults(session, user.id)
    return vaults


@router.get(
    "/shared",
    name="Get all vaults shared with the user",
    description="Get all vaults or shared with the user",
    response_model=list[Vault],
)
def get_shared_user_vaults_route(
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
) -> list[Vault]:
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.get_shared_vaults(session, user.id)


@router.post(
    "/",
    name="Create a new vault owned by user",
    response_model=Vault,
    status_code=201,
)
def create_new_user_vault_route(
    body: CreateVault,
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
) -> Vault:
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.create_vault(session, body, user.id)


@router.post(
    "/{vault_id}/shares/", name="Grant a user access to the vault", status_code=200
)
def share_vault_with_user_route(
    body: UserID,
    vault_id=Annotated[UUID, Path(title="ID of the current dataset")],
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
) -> VaultUser:
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.share_vault_with_user(session, vault_id, user, body.user_id)


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
    session: DBSession = Depends(get_session),
) -> Vault:
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.get_vault_by_id(session, vault_id, user.id)


@router.delete(
    "/{vault_id}",
    name="Delete the vault provided",
    description="Delete the vault provided if permitted to do so",
    status_code=204,
)
def delete_vault_route(
    vault_id: UUID,
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
):
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.delete_vault(session, vault_id, user.id)
