from sqlalchemy.orm import Mapped, mapped_column

from py_tools.connections.db.mysql import BaseOrmTableWithTS


class UserTable(BaseOrmTableWithTS):
    """用户表"""

    __tablename__ = "user"
    username: Mapped[str] = mapped_column(comment="用户昵称")
    password: Mapped[str] = mapped_column(comment="用户密码")
    phone: Mapped[str] = mapped_column(comment="手机号")
    email: Mapped[str] = mapped_column(comment="邮箱")
