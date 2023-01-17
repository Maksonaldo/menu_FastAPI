from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapper
import uuid
metadata = MetaData()

menu = Table(
    "menu",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("title", String,  nullable=True),
    Column("description", String,  nullable=True),
    Column("submenus_count",  Integer,  nullable=True, default=0),
    Column("dishes_count", Integer,  nullable=True, default=0),
)


class Menu:
    def __init__(self, id, title, description, submenus_count, dishes_count):
        self.id = id
        self.title = title
        self.description = description
        self.submenus_count = submenus_count
        self.dishes_count = dishes_count


submenu = Table(
    "submenu",
    metadata,
    Column("id", String, primary_key=True, default=uuid.uuid4),
    Column("title", String, nullable=True),
    Column("description", String, nullable=True),
    Column("dishes_count", Integer, nullable=True, default=0),
    Column("menu_id", String, ForeignKey("menu.id"), nullable=True)
)


class Submenu:
    def __init__(self, id, title, description, dishes_count, menu_id):
        self.id = id
        self.title = title
        self.description = description
        self.dishes_count = dishes_count
        self.menu_id = menu_id


dish = Table(
    "dish",
    metadata,
    Column("id",  String, primary_key=True, default=uuid.uuid4),
    Column("title", String, nullable=True),
    Column("description", String, nullable=True),
    Column("price", String, nullable=True),
    Column("submenu_id",  String, ForeignKey("submenu.id"), nullable=True)
)


class Dish:
    def __init__(self, id, title, description, price, submenu_id):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.submenu_id = submenu_id


mapper(Menu, menu)
mapper(Submenu, submenu)
mapper(Dish, dish)
