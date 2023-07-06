from tools import db


def init_db():
    from plugins.audit_logs import models
    db.Base.metadata.create_all(bind=db.engine)

