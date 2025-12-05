from datetime import datetime
from http import HTTPStatus
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.core.config import Settings
from src.core.security import PasswordHandler, oauth2_scheme
from src.core.dependencies import get_settings
from src.core.db import get_session
from .models import DbVault
from .schema import Vault, CreateVault
from src.domain.user.schema import User
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
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
    session: DBSession = Depends(get_session),
) -> list[Vault]:
    user: User = user_service.get_user_from_token(session, token)
    return vault_service.get_vaults_by_user(session, user.id)


@router.post(
    "/", name="Create a new vault owned by user", response_model=Vault, status_code=201
)
def create_new_user_vault_route(
    body: CreateVault,
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
) -> Vault:
    user: User = user_service.get_user_from_token(session, token)
    db_vault: DbVault = DbVault(
        id=uuid4(),
        owner=user.id,
        name=body.name,
        description=body.description,
        creation_date=datetime.now(),
        passphrase_hash=PasswordHandler.hash(body.passphrase),
    )
    vault_service.create_vault(session, db_vault)
    vault = Vault.model_validate(db_vault)
    return vault


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
    db_vault = vault_service.get_vault_by_id(session, vault_id)

    if not db_vault:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Vault not found")
    vault: Vault = Vault.model_validate(db_vault)
    if vault.owner != user.id:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            "Only the owner may access a vault",
        )
    return vault


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
    db_vault = vault_service.get_vault_by_id(session, vault_id)
    if not db_vault:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Vault {vault_id} does not exist",
        )
    vault: Vault = Vault.model_validate(db_vault)
    if vault.owner != user.id:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "Only the owner may delete a vault"
        )
    vault_service.delete_vault(session, vault.id)
