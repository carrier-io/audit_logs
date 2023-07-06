from .mixins import TimestampModelMixin, CreateReadUpdateDeleteCountMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    String, 
    Column, 
    Integer,
    Text,
    JSON,
    ForeignKey,
)
from tools import db



class Log(CreateReadUpdateDeleteCountMixin, TimestampModelMixin, db.Base):
    __tablename__ = "audit__logs"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    
    auditable_id = Column(Integer, nullable=True)
    auditable_type = Column(String(150), nullable=True)

    user_email = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    changes = Column(JSON, nullable=True)
    related_entities = relationship('RelatedEntity', backref=backref("log"), lazy=True) 


class RelatedEntity(CreateReadUpdateDeleteCountMixin, db.Base):
    __tablename__ = "aduit__reltated_entities"

    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey(Log.id), nullable=True)
    auditable_id = Column(Integer, nullable=True)
    auditable_type = Column(String(150), nullable=True)
