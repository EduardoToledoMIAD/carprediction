from marshmallow import Schema, fields, validate, ValidationError



class CarPredictionSchema(Schema):
    Year = fields.Int(required=True)
    Mileage= fields.Int(required=True)
    State = fields.Str(required=True)
    Make = fields.Str(required=True)
    Model = fields.Str(required=True)

class BatchSchema(Schema):
    batch = fields.List(fields.Nested(CarPredictionSchema))

