from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table           # Для промежуточной таблицы
)

BASE = declarative_base()

"""
one to many - один к многому
many to one - многое к одному
one to one - один к одному
many to many - многое к многому
"""

# tag_post = Table('tag_post', BASE.metadata,                              # Виртуальная таблица
#                  Column('post_id', Integer, ForeignKey('post.id')),
#                  Column('tag_id', Integer, ForeignKey('tag.id'))
#                  )


class Post(BASE):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)   ## не может быть null, уникальность false
    date = Column(String, nullable=False, unique=False)
    adres = Column(String, nullable=False, unique=False)
    city = Column(String, nullable=False, unique=False)
    pos_addres = Column(String, nullable=False, unique=False)
    telephone = Column(String, nullable=False, unique=False)
    kontakt_person = Column(String, nullable=False, unique=False)
    site = Column(String, nullable=False, unique=False)
    url = Column(String, nullable=False, unique=True)
    # writer_id = Column(Integer, ForeignKey('writer.id'), nullable=False)
    # writer = relationship("Writer", back_populates='post', lazy ='joined')  # Получаем обьект соединяем с врайтерами, lazy - не ленивая связь.
    # tags = relationship('Tag', secondary=tag_post, back_populates='posts')  # Указываем таблицу что являеться промежуточной для нашей связи.

    def __init__(self, name, date, adres, city, pos_addres, telephone, kontakt_person, site, url):
        # tags = tags if tags else []
        self.name = name
        self.date = date
        self.adres = adres
        self.city = city
        self.pos_addres = pos_addres
        self.telephone = telephone
        self.kontakt_person = kontakt_person
        self.site = site
        self.url = url
        # self.writer = writer
        # self.tags.extend(tags)   # Записывает список тегов


# class Writer(BASE):  # BASE - обьеденяет все таблицы в одну базу
#     __tablename__ = 'writer'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False, unique=False)
#     url = Column(String, nullable=False, unique=True)
#     post = relationship('Post', back_populates='writer')   #получаем обьект из БД. соединяем с таблицей постов
#
#     def __init__(self, name, url):
#         self.name = name
#         self.url = url
#
#     def __str__(self):
#         return self.name
#
#
# class Tag(BASE):
#     __tablename__ = 'tag'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     name = Column(String, nullable=False, unique=False)
#     url = Column(String, nullable=False, unique=True)
#     posts = relationship('Post', secondary=tag_post, back_populates='tags')
#
#     def __init__(self, name, url):
#         self.name = name.lower()
#         self.url = url