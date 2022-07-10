from sqlalchemy import Column, String, Integer, Boolean
from data_base.dbcore import Base


class Category(Base):
    """Категории товаров"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return self.name

