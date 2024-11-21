from marshmallow import fields

from app import db, ma


class BaseSchema(ma.Schema):
    class Meta:
        sqla_session = db.session


class MarketCapSchemaSchema(BaseSchema):
    currency = fields.String(required=True)
    value = fields.Float(required=True)


class CompetitorSchemaSchema(BaseSchema):
    name = fields.String(required=True)
    market_cap = fields.Nested(MarketCapSchemaSchema, required=True)


class PerformanceDataSchemaSchema(BaseSchema):
    five_days = fields.Float(required=True)
    one_month = fields.Float(required=True)
    three_months = fields.Float(required=True)
    year_to_date = fields.Float(required=True)
    one_year = fields.Float(required=True)


class StockValuesSchemaSchema(BaseSchema):
    open = fields.Float(required=True)
    high = fields.Float(required=True)
    low = fields.Float(required=True)
    close = fields.Float(required=True)


class StockInformationSchemaSchema(BaseSchema):
    status = fields.String(required=True)
    purchased_amount = fields.Integer(required=True)
    purchased_status = fields.String(required=True)
    request_data = fields.Date(required=True)
    company_code = fields.String(required=True)
    company_name = fields.String(required=True)
    stock_values = fields.Nested(StockValuesSchemaSchema, required=True)
    performance_data = fields.Nested(PerformanceDataSchemaSchema, required=True)
    competitors = fields.List(fields.Nested(CompetitorSchemaSchema), required=True)
