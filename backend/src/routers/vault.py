from datetime import datetime
from http import HTTPStatus
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dbutil import get_session
from src.dependency_util import get_settings, get_user_from_token
from src.database.vault import (
    DbVault,
    delete_vault,
    get_vaults_by_user,
    create_vault,
    get_vault_by_id,
)
from src.models.user import User
from src.models.vault import CreateVault, Vault
from src.security import PasswordHandler
from src.settings import Settings
from .auth import oauth2_scheme


VAULTS_TAG = "Vaults"
router = APIRouter(prefix="/vaults", tags=[VAULTS_TAG])


@router.get(
    "/",
    name="Get all vaults accessible to the user",
    description="Get all vaults owned by (or shared with) the user",
)
def get_all_user_vaults_route(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):
    user: User = get_user_from_token(settings, session, token)
    return get_vaults_by_user(session, user.id)


@router.post(
    "/",
    name="Create a new vault owned by user",
    response_model=Vault,
)
def create_new_user_vault_route(
    body: CreateVault,
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
) -> Vault:
    user: User = get_user_from_token(settings, session, token)
    password_handler = PasswordHandler(settings)
    vault: DbVault = DbVault(
        id=uuid4(),
        owner=user.id,
        name=body.name,
        description=body.description,
        creation_date=datetime.now(),
        passphrase_hash=password_handler.hash(body.passphrase),
    )
    create_vault(session, vault)
    return Vault.model_validate(vault)


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
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):
    user: User = get_user_from_token(settings, session, token)
    vault: Vault = Vault.model_validate(get_vault_by_id(session, vault_id))

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
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):
    user: User = get_user_from_token(settings, session, token)
    db_vault = get_vault_by_id(session, vault_id)
    if not db_vault:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Vault {vault_id} does not exist")
    vault: Vault = Vault.model_validate(db_vault)

    if vault.owner != user.id:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "Only the owner may delete a vault"
        )
    delete_vault()
