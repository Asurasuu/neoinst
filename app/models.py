from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Тута описываются модели данных (на их основе создаются таблицы)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String,)
    surname = Column(String,)
    about = Column(String,)
    phone = Column(String,)
    hashed_password = Column(String)

    # sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    # received_messages = relationship("Message", foreign_keys="[Message.recipient_id]", back_populates="recipient")

# Модель сообзений
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, )#ForeignKey("users.id"))
    recipient_id = Column(Integer,)# ForeignKey("users.id"))
    content = Column(String)

    # sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    # recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")