from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import uuid
import os

# ---- DB CONFIG ----
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./data/sessions.db"
)

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine)


# ---- MODELS ----
class ChatSession(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


# ---- INIT DB ----
def init_db():
    Base.metadata.create_all(engine)


# ---- SESSION FUNCTIONS ----
def create_session(name: str | None = None):
    db = SessionLocal()

    count = db.query(ChatSession).count()
    if name is None:
        name = f"Chat {count + 1}"

    session_id = str(uuid.uuid4())

    session = ChatSession(
        id=session_id,
        name=name,
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
    )

    db.add(session)
    db.commit()
    db.close()

    return session_id


def delete_session(session_id):
    db = SessionLocal()

    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()

    db.close()


def update_last_active(session_id):
    db = SessionLocal()

    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        session.last_active = datetime.utcnow()
        db.commit()

    db.close()


# ---- MESSAGE FUNCTIONS ----
def save_message(session_id, role, content):
    db = SessionLocal()

    msg = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.utcnow(),
    )

    db.add(msg)

    # update last active
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        session.last_active = datetime.utcnow()

    db.commit()
    db.close()


def load_messages(session_id):
    db = SessionLocal()

    msgs = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .all()
    )

    db.close()

    return [
        {"role": m.role, "content": m.content}
        for m in msgs
    ]


def delete_messages_by_session(session_id):
    db = SessionLocal()

    db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).delete()

    db.commit()
    db.close()


# ---- LIST SESSIONS ----
def list_sessions():
    db = SessionLocal()

    sessions = (
        db.query(ChatSession)
        .order_by(ChatSession.last_active.desc())
        .all()
    )

    db.close()

    return [
        {
            "id": s.id,
            "name": s.name,
            "created_at": s.created_at,
            "last_active": s.last_active,
        }
        for s in sessions
    ]