from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

import logging
import env_file

logging.basicConfig(level=logging.INFO)

token = env_file.get()

Base = declarative_base()


class RconCreds(Base):
    __tablename__ = "rconcreds"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    member_id = Column("member_id", BigInteger, unique=True)
    host = Column("host", String)
    port = Column("port", Integer)
    password = Column("password", String)


engine = create_engine(token["DATABASE_URL"])
Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)

session = Session()

# creds = RconCreds(
#     member_id=id,
#     host="host",
#     port=port,
#     password="password,
# )


def add_creds(creds):
    session.add(creds)
    session.commit()
    session.close()


def get_creds(member_id):
    creds = session.query(RconCreds).filter_by(member_id=member_id).first()
    if creds is not None:
        host = creds.host
        port = creds.port
        password = creds.password
    else:
        host, port, password = (None, None, None)
    return host, port, password
