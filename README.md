This project is a web application that enables users to analyze stock market data and execute trades. 
It scrapes stock information from MarketWatch and utilizes the Polygon API for real-time data.
Users can view stock performance, apply various analytical tools, and buy stocks directly through the app. 
The application features secure user authentication, portfolio management, and a responsive design for an optimal 
user experience across devices.

### Prerequisites
1. Python 3.10+
2. Docker
3. Docker Compose
4. Postgres 13

### 1. Starting Postgres DB

```bash
docker-compose up --build
```

### 2. Init database:

```bash
# Creates a new migration repository
flask db init

# Autogenerate a new revision file
flask db migrate

# Upgrade to a later version
flask db upgrade
```

### 3. Set Up & Running

```bash
# Creates virtual env
python3 -m venv venv

# Activates virtual env
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Set flask environment variables linux
export FLASK_DEBUG=1
export FLASK_APP=run.py
export FLASK_CONFIG=development

# Set flask environment variables windows
set FLASK_DEBUG=1
set FLASK_APP=run.py
set FLASK_CONFIG=development

# Running dev server
flask run
```

### 4. Testing

```bash
pytest tests
```

### 5. Testing Endpoint

```bash
# GET BY STOCK SYMBOL AND DATE
curl http://localhost:5000/stocks/aapl/2023-04-20

# POST 
curl -X POST http://localhost:5000/stocks/AAPL \
-H "Content-Type: application/json" \
-d '{"amount": 5.33}'
```