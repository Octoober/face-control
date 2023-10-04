from typing import Optional, Union

from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session


class DatabaseConnection:
    # ! TODO: refactoring
    _instance: Optional["DatabaseConnection"] = None
    _engine: Engine
    _sessionmaker: sessionmaker
    _session: Optional[Session] = None

    def __new__(cls, url: Union[str, URL]) -> Optional["DatabaseConnection"]:
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._engine = create_engine(url)
            cls._instance._sessionmaker = sessionmaker(bind=cls._instance._engine)
        return cls._instance

    def __enter__(self) -> "DatabaseConnection":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_session()

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = self._sessionmaker()
        return self._session

    def close_session(self) -> None:
        if self._session:
            self._session.close()
            self._session = None
