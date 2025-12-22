from typing import Generic, TypeVar
from uuid import UUID
from src.core.db import Queries


T = TypeVar("T")


class CrudRepository(Generic[T]):
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_by_id(self, id: UUID) -> T:
        return Queries.get_by_id(self.session, self.model, id)

    def create(self, entity: T):
        Queries.insert(self.session, entity)

    def delete(self, id: UUID):
        Queries.delete_by_id(self.session, self.model, id)
