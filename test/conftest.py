import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from webapp import create_app
from webapp.models import Base, User, Role, Permission, GroupPermission


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    # seeded data
    session.add_all(
        [
            Role(name="Admin"),
            Role(name="Editer"),
            Permission(name="Create"),
            Permission(name="Edit"),
            GroupPermission(role_id=1, permission_id=1),
            GroupPermission(role_id=1, permission_id=2),
            GroupPermission(role_id=2, permission_id=2),
        ]
    )
    session.commit()

    yield session

    session.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
