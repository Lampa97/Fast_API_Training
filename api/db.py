from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "urls.db"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables(run_engine=None):
    """Create the database and tables if they do not exist."""
    if run_engine is None:
        run_engine = engine
    SQLModel.metadata.create_all(run_engine)


def get_session(run_engine=None):
    """Get a database session."""
    if run_engine is None:
        run_engine = engine
    with Session(run_engine) as session:
        yield session
