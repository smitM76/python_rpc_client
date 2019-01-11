from sqlalchemy.orm import sessionmaker
from dataQueue import engine, User, config
import sqlalchemy.exc
import logging
import json
from logging import basicConfig
from logging.config import dictConfig

file = open('logging_config.ini', "r")
config = json.load(file)
dictConfig(config)


LOGGER = logging.getLogger(__name__)

"""
logging.basicConfig(filename='mainFile.log',
                    level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

"""

#LOGGER = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)


def display_data():
    session = Session()
    try:
        users = session.query(User).all()
    except NameError as e:
        LOGGER.error(e)
    else:
        user_list = []
        for user in users:
            values = {
                "id": user.id,
                "username": user.username,
                "comment": user.comment
            }
            user_list.append(values)
            # print(user_list)
        session.close()
    # print(user_list)
    return user_list


def insert_data(uname, comment):
    session = Session()
    user = User()
    user.username = uname
    user.comment = comment
    try:
        session.add(user)
        session.commit()
        LOGGER.info('Record Created Successfully')
        return 'Record Created Successfully'

    except sqlalchemy.exc.IntegrityError as e:
        LOGGER.error(e)
        return("username already exists!")
    session.close()


def update_data(uid, u_name, u_comment):
    session = Session()
    u_id = '{}'.format(uid)
    try:
        if u_name is None and u_comment is None:
            return 'Required minimum one optional argument [--username][--comment]'
        elif u_name is None:
            x = session.query(User).filter(User.id == u_id).first()
            x.comment = u_comment
            session.commit()
            LOGGER.info('comment updated to : {} '.format(u_comment))
            return 'comment updated to : {} '.format(u_comment)
        elif u_comment is None:
            x = session.query(User).filter(User.id == u_id).first()
            x.username = u_name
            session.commit()
            session.close()
            logger.info('username updated to : {}'.format(u_name))
            return 'username updated to : {}'.format(u_name)
        else:
            x = session.query(User).filter(User.id == u_id).first()
            x.username = u_name
            x.comment = u_comment
            session.commit()
            session.close()
            logger.info('updated username => {} and comment => {}'.format(
                u_name, u_comment))
            return 'updated username => {} and comment => {}'.format(u_name, u_comment)
    except sqlalchemy.exc.IntegrityError as e:
        logger.error(e)
        return 'username must be unique'
    return 'Updated'


def delete_data(uid):
    session = Session()
    u_id = '{}'.format(uid)
    x = session.query(User).filter(User.id == u_id). \
        delete(synchronize_session=False)
    session.commit()
    session.close()
    return 'Deleted data for ID : {} '.format(u_id)
