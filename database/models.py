from sqlalchemy import create_engine, Column, String, DateTime, Text, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# This code is used to create initial table

Base = declarative_base()


class UserContent(Base):
    __tablename__ = 'user_content'
    user_id = Column(String)
    prompt = Column(Text, nullable=False)
    paths_url = Column(Text, nullable=False)
    status = Column(String, default='Processing')
    generated_at = Column(DateTime)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'prompt', 'generated_at', name='user_content_pk'),
    )

class UserLogin(Base):
    __tablename__ = 'user_login'
    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'ai_content.db')
engine = create_engine(f'sqlite:///{db_path}')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
