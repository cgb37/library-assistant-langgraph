# Shared database service for the Quart app

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from shared.config_service import config_service

DATABASE_URL = config_service.get('DATABASE_URL')

# Convert sqlite:// to sqlite+aiosqlite:// for async support
if DATABASE_URL.startswith('sqlite://'):
    DATABASE_URL = DATABASE_URL.replace('sqlite://', 'sqlite+aiosqlite://')

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session