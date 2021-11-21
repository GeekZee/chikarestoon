from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_async_engine(
    f"sqlite+aiosqlite:///{sqlite_file_name}", connect_args={"check_same_thread": False})


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
