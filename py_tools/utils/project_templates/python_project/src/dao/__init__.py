from src import settings
from src.dao.redis import RedisManager

from py_tools.connections.db.mysql import DBManager, SQLAlchemyManager


async def init_orm():
    """初始化mysql的ORM"""
    db_client = SQLAlchemyManager(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        db_name=settings.mysql_dbname,
    )
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)
    return db_client


async def init_redis():
    RedisManager.init_redis_client(
        async_client=True,
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=settings.redis_db,
    )
