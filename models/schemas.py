from marshmallow import Schema, fields, validate, ValidationError

class ProfitPredictionSchema(Schema):
    RDSpend = fields.Float(required=True)
    Administration = fields.Float(required=True)
    MarketingSpend = fields.Float(required=True)
    State = fields.Str(required=True)

class CarPredictionSchema(Schema):
    Year = fields.Int(required=True)
    Mileage= fields.Int(required=True)
    State = fields.Str(required=True)
    Make = fields.Str(required=True)
    Model = fields.Str(required=True)

class BatchSchema(Schema):
    batch = fields.List(fields.Nested(CarPredictionSchema))

class Batch1Schema(Schema):
    batch = fields.List(fields.Nested(ProfitPredictionSchema))
