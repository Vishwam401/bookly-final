from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=True)

# ✅ correct async session maker
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)

# ✅ dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# ✅ init DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)