from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from db_config import db_type, db_user, db_password, db_host, db_name
from messages import SEX

Base = declarative_base()
engine_db = f'{db_type}://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(engine_db, client_encoding = 'utf8')
Session = sessionmaker(bind = engine)
session = Session()


class HornyUser(Base):
    __tablename__ = 'horny_user'
    id = Column(Integer, primary_key=True)
    h_user_vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    age_from = Column(Integer, nullable=True)
    age_to = Column(Integer, nullable=True)
    country = Column(Integer, nullable=True)
    city = Column(Integer, nullable=True)
    sex = Column(Integer, nullable=True)


class DatingUser(Base):
    __tablename__ = 'dating_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    d_user_vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    vk_link = Column(String)
    h_user_id = Column(Integer, ForeignKey('horny_user.id', ondelete='CASCADE'))


class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link_photo = Column(String)
    count_likes = Column(Integer)
    d_user_id = Column(Integer, ForeignKey('dating_user.id', ondelete='CASCADE'))


class BlackList(Base):
    __tablename__ = 'black_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    d_user_vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    vk_link = Column(String)
    h_user_id = Column(Integer, ForeignKey('horny_user.id', ondelete='CASCADE'))


class DB:
    def __init__(self):
        pass

    def reg_new_user(self, user_data):
        try:
            h_user = HornyUser(**user_data)
            session.add(h_user)
            session.commit()
            return True
        except (IntegrityError, InvalidRequestError) as e:
            return False


    def add_date_to_favorites(self, d_user_vk_id, first_name, last_name, vk_link, h_user_id):
        try:
            d_user = DatingUser(
                d_user_vk_id = d_user_vk_id,
                first_name = first_name,
                last_name = last_name,
                vk_link = vk_link,
                h_user_id = h_user_id
            )
            session.add(d_user)
            session.commit()
            return True
        except (IntegrityError, InvalidRequestError):
            return False


    def add_photos(self, link_photo, count_likes, d_user_id):
        try:
            new_photos = Photos(link_photo = link_photo, count_likes = count_likes, d_user_id = d_user_id)
            session.add(new_photos)
            session.commit()
            return True
        except (IntegrityError, InvalidRequestError):
            return False


    def add_to_black_list(self, d_user_vk_id, first_name, last_name, vk_link, h_user_id):
        try:
            d_user = BlackList(
                d_user_vk_id = d_user_vk_id,
                first_name = first_name,
                last_name = last_name,
                vk_link = vk_link,
                h_user_id = h_user_id
            )
            session.add(d_user)
            session.commit()
            return True
        except (IntegrityError, InvalidRequestError):
            return False


    def delete_db_blacklist(self, vk_id):
        current_user = session.query(BlackList).filter_by(d_user_vk_id = vk_id).first()
        session.delete(current_user)
        session.commit()


    def delete_db_favorites(self, vk_id):
        current_user = session.query(DatingUser).filter_by(d_user_vk_id = vk_id).first()
        session.delete(current_user)
        session.commit()


    def check_db_h_user(self, vk_id):
        h_user_db_query = session.query(HornyUser).filter_by(h_user_vk_id = vk_id).first()
        h_user_db_id = h_user_db_query.id if h_user_db_query else None
        return h_user_db_id


    def check_db_d_user(self, vk_id):
        d_user_db_id = session.query(DatingUser).filter_by(d_user_vk_id = vk_id).first()
        return d_user_db_id


    def check_db_d_bl_user(self, vk_id):
        d_user_bl_db_id = session.query(BlackList).filter_by(d_user_vk_id = vk_id).first()
        return d_user_bl_db_id


    def check_db_black_list(self, vk_id):
        current_user = session.query(HornyUser).filter_by(h_user_vk_id = vk_id).first()
        found_black_list_users = session.query(BlackList).filter_by(h_user_id = current_user.id).all()
        return found_black_list_users


    def check_db_favorites(self, vk_id):
        current_user = session.query(HornyUser).filter_by(h_user_vk_id = vk_id).first()
        found_favorite_list_users = session.query(DatingUser).filter_by(h_user_id = current_user.id).all()
        return found_favorite_list_users


if __name__ == '__main__':
    Base.metadata.create_all(engine)
