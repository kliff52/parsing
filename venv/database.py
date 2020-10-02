from sqlalchemy import create_engine     ## Импорт движка
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload   # Потдягивать из других таблиц зависимости.

from models import BASE, Post, Tag, Writer


class GBBlogDB:
    def __init__(self, db_url):
        engine = create_engine(db_url, connect_args={'check_same_thread': False})
        BASE.metadata.create_all(engine)
        self.session_db = sessionmaker(bind=engine)  ## Получаем сесию от нашей БД

    def create_post(self, post_obj: Post, writer=None, tags=None):
        tags = tags if tags else []
        session = self.session_db()
        writer = self.__create_or_update(session, writer)
        #todo для студентов объясните почему именно такое решение в процедуре сохранения
        tags = [self.__create_or_update(session, tag) for tag in tags]
        post_obj.tags.extend(tags)
        post_obj.writer = writer
        try:
            session.commit()  # Пробуем закомитеть.
        except Exception as e:
            session.rollback()  # Если ошибка то откат
        finally:
            session.close() # При любом исходе закрываем сесию.

    def __create_or_update(self, session, model_obj):
        model_obj_result = session.query(model_obj.__class__).filter_by(url=model_obj.url).first() # Если такой есть то вернуть из базы повторившейся обьект
        if not model_obj_result:
            session.add(model_obj)
            try:
                session.commit()
            except Exception as e:
                session.rollback()
            finally:
                model_obj_result = model_obj
        return model_obj_result

    def save_post_from_dict(self, post: dict):
        tags = [Tag(*itm) for itm in post['tags']]
        writer = Writer(post['author_name'], post['author_url'])
        post = Post(post['title'], post['url'])
        self.create_post(post, writer, tags)


if __name__ == '__main__':
    db = GBBlogDB('sqlite:///gb_blog.db')
    print(1)