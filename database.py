# from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Sequence
# from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import sessionmaker, relationship

# import logging
# import env_file

# logging.basicConfig(level=logging.INFO)

# token = env_file.get()

# Base = declarative_base()


# class MemberProfile(Base):
#     __tablename__ = "member_profile"

#     id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
#     member_id = Column("member_id", BigInteger, unique=True)
#     username = Column("username", String)


# engine = create_engine(token["DATABASE_URL"])
# Base.metadata.create_all(bind=engine)


# Session = sessionmaker(bind=engine)

# session = Session()

# def add_creds(member):
#     session.add(member)
#     session.commit()
#     session.close()


# def get_creds(member_id):
#     member = session.query(MemberProfile).filter_by(member_id=member_id).first()
#     if member is not None:
#         username = member.username
#     else:
#         username = None
#     return username


# member = MemberProfile(member_id=id, username=username)
