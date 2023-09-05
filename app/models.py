from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('true'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))