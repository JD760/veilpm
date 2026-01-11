from src.core.repositories.crud_repository import CrudRepository


class FolderRepository(CrudRepository):
    def __init__(self, session, model):
        super().__init__(session, model)
        self.session = session
