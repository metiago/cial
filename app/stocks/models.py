from app import db


class MarketCap(db.Model):
    __tablename__ = 'market_caps'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<MarketCap(currency={self.currency}, value={self.value})>"


class PerformanceData(db.Model):
    __tablename__ = 'performance_data'

    id = db.Column(db.Integer, primary_key=True)
    five_days = db.Column(db.Float, nullable=False)
    one_month = db.Column(db.Float, nullable=False)
    three_months = db.Column(db.Float, nullable=False)
    year_to_date = db.Column(db.Float, nullable=False)
    one_year = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<PerformanceData(five_days={self.five_days}, one_month={self.one_month}, three_months={self.three_months}, year_to_date={self.year_to_date}, one_year={self.one_year})>"


class StockValues(db.Model):
    __tablename__ = 'stock_values'

    id = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<StockValues(open={self.open}, high={self.high}, low={self.low}, close={self.close})>"


class Competitor(db.Model):
    __tablename__ = 'competitors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    market_cap_id = db.Column(db.Integer, db.ForeignKey('market_caps.id'), nullable=False)
    stock_information_id = db.Column(db.Integer, db.ForeignKey('stock_information.id'), nullable=False)

    market_cap = db.relationship('MarketCap', backref='competitors')
    stock_information = db.relationship('StockInformation',
                                        backref='competitors_list',
                                        overlaps='stock_information_ref',
                                        viewonly=True)

    def __repr__(self):
        return f"<Competitor(name={self.name}, market_cap={self.market_cap})>"


class StockInformation(db.Model):
    __tablename__ = 'stock_information'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    purchased_amount = db.Column(db.Numeric(10, 2), nullable=False)
    purchased_status = db.Column(db.String(50), nullable=False)
    request_data = db.Column(db.Date, nullable=False)
    company_code = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    stock_values_id = db.Column(db.Integer, db.ForeignKey('stock_values.id'), nullable=False)
    performance_data_id = db.Column(db.Integer, db.ForeignKey('performance_data.id'), nullable=False)

    stock_values = db.relationship('StockValues', backref='stock_information')
    performance_data = db.relationship('PerformanceData', backref='stock_information')
    competitors = db.relationship('Competitor', backref='stock_information_ref', lazy=True)

    def __repr__(self):
        return f"<StockInformation(company_code={self.company_code}, company_name={self.company_name}, status={self.status})>"
