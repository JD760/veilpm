from fastapi import APIRouter

VAULTS_TAG = "Vaults"

router = APIRouter(prefix="/vaults", tags=[VAULTS_TAG])


@router.get(
    "/",
    name="Get all vaults accessible to the user",
    description="Get all vaults owned by (or shared with) the user",
)
def get_all_user_vaults_route():
    pass


@router.post(
    "/",
    name="Create a new vault owned by user",
)
def create_new_user_vault_route():
    pass


@router.get(
    "/{vault_id}",
    name="Get the provided vault",
    description="Get the vault with provided ID if it exists\
        and the user is authorised to view it",
)
def get_vault_route():
    pass


@router.delete(
    "/{vault_id}",
    name="Delete the vault provided",
    description="Delete the vault provided if permitted to do so",
    status_code=204,
)
def delete_vault_route():
    pass
