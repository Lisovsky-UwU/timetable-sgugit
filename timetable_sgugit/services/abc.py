from typing import TypeVar
from typing import Generic
from typing import Optional
from typing import List
from typing import Iterable
from typing import Type
from functools import lru_cache
from sqlalchemy import Column
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query

from ..orm import session_factory
from ..exceptions import DataBaseException


T = TypeVar('T')

class BaseService(Generic[T]):

    def __init__(self, session: Optional[Session] = None, **kwargs):
        self.__session__ = session or session_factory(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

        if exc_type is not None:
            if issubclass(exc_type, ConnectionError):
                raise DataBaseException("Отсутствует соединение с базой данных")

    @property
    def session(self) -> Session:
        return self.__session__

    @property
    @lru_cache(maxsize=None)
    def model(self) -> Type[T]:
        for base in type(self).__orig_bases__:
            if hasattr(base, '__args__'):
                return base.__args__[0]

    @property
    def query(self) -> Query:
        return self.session.query(self.model)


    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()


    def get_all(self, get_deleted: bool = False, order_by: Optional[Column] = None) -> List[T]:
        query = self.query
        if order_by is not None:
            query = query.order_by(order_by)

        if not get_deleted and hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted == False)

        return query.all()


    def get_by_id(self, id: int) -> Optional[T]:
        return self.query.get(id)


    def get_filtered(
        self, 
        expression, 
        get_deleted: Optional[bool] = False, 
        order_by: Optional[Column] = None
    ) -> List[T]:
        query = self.query.filter(expression)

        if not get_deleted and hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted == False)

        if order_by is not None:
            query = query.order_by(order_by)

        return query.all()


    def get_filtered_first(
        self, 
        expression, 
        get_deleted: Optional[bool] = False
    ) -> Optional[T]:
        query = self.query.filter(expression)

        if not get_deleted and hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted == False)

        return query.first()


    def create(self, item: T, flush: bool = True) -> T:
        self.session.add(item)
        if flush:
            self.session.flush((item,))
            
        return item


    def create_for_iter(self, items: Iterable[T], flush: bool = True) -> List[T]:
        items = list(items)
        self.session.add_all(items)
        if flush:
            self.session.flush()
        
        return items


    def update(self, item: T, flush: bool = True) -> T:
        item = self.session.merge(item)
        if flush:
            self.session.flush((item,))

        return item
    

    def update_for_iter(self, items: Iterable[T], flush: bool = True) -> List[T]:
        for item in items:
            self.update(item, flush=False)
        if flush:
            self.session.flush()

        return list(items)


    def delete(self, item: T, flush: bool = False) -> None:
        if hasattr(self.model, 'deleted'):
            item.deleted = True
            self.update(item, flush=flush)
        else:
            self.session.delete(item)

        if flush:
            self.session.flush((item,))


    def delete_for_id_list(self, id_list: Iterable[int], flush: bool = True) -> None:
        delete_list = [ self.query.get(id) for id in id_list ]
        self.delete_for_list(delete_list, flush)


    def delete_for_list(self, delete_list: Iterable[T], flush: bool = True) -> None:
        for item in delete_list:
            self.delete(item)

        if flush:
            self.session.flush()
