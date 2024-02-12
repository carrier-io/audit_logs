from tools import db


def init_db():
    from ..models.logs import Log, RelatedEntity

    db.get_shared_metadata().create_all(bind=db.engine)

