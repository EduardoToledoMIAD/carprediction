from marshmallow import Schema, fields, validate, ValidationError

class CarPredictionSchema(Schema):
    RDSpend = fields.Float(required=True)
    Administration = fields.Float(required=True)
    MarketingSpend = fields.Float(required=True)
    State = fields.Str(required=True)
    
class BatchSchema(Schema):
    batch = fields.List(fields.Nested(CarPredictionSchema))

