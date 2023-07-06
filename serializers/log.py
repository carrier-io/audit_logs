from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from ..models.logs import Log, RelatedEntity


class RelatedEntitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RelatedEntity
        fields = (
            'auditable_id',
            'auditable_type',
        )


class LogSchema(SQLAlchemyAutoSchema):
    related_entities = fields.Nested(RelatedEntitySchema, many=True)
    
    class Meta:
        model = Log


logs_schama = LogSchema(many=True)
log_schama = LogSchema()