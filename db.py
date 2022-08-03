from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    'sqlite:///database.db',
    connect_args={
        "check_same_thread": False
    }
)


def get_session() -> Session:
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    return session()
