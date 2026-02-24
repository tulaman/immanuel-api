# Immanuel API

An astrological calculation REST API built with FastAPI and the [Immanuel](https://github.com/theriftlab/immanuel-python) Python library. Provides endpoints for natal charts, planetary positions, retrograde calendars, transits, progressions, synastry, composite charts, solar returns, and daily/weekly/yearly forecasting.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Astrology Engine**: [Immanuel](https://github.com/theriftlab/immanuel-python) (built on Swiss Ephemeris)
- **Python**: 3.10+

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/your-username/immanuel-api.git
cd immanuel-api
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Running with Docker

```bash
docker build -t immanuel-api .
docker run -p 8000:8000 immanuel-api
```

## API Endpoints

### Natal Charts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/natal.json` | Full natal chart as JSON |
| GET | `/natal.txt` | Natal chart as plain text |

**Parameters**: `year`, `month`, `day`, `lat`, `lon`, `hour` (opt), `min` (opt), `sec` (opt)

### Planetary Positions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/planetary_positions` | Planetary positions for a given date and location |

**Parameters**: `year`, `month`, `day`, `lat`, `lon`, `hour` (opt), `min` (opt), `sec` (opt)

**Response** includes for each planet: name, latitude, longitude, sign, sign longitude, house, speed, distance, and movement (direct/retrograde).

### Retrograde Calendar

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/retrograde_calendar` | Retrograde periods for the next N months |

**Parameters**: `n` (number of months), `lat`, `lon`

### Forecasting

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get_daily_forecast_data` | Daily planet positions, aspects, and moon phase |
| GET | `/get_weekly_forecast_data` | 7-day forecast data |
| GET | `/get_yearly_forecast_data` | 365-day planet movement periods |

**Parameters**: `start_date` (format: `YYYY-MM-DD`)

### Chart Comparisons & Returns

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transits` | Calculate transits for a birth chart |
| POST | `/progressions` | Calculate progressions for a birth chart |
| POST | `/synastry` | Compare two birth charts |
| POST | `/composite` | Generate composite chart from two charts |
| POST | `/solar_returns` | Calculate solar return for a given year |

**Transits/Progressions parameters**: `year`, `month`, `day`, `hour`, `lat`, `lon`

**Synastry/Composite parameters**: Two sets of `year`, `month`, `day`, `hour`, `lat`, `lon` (suffixed `_2` for the second person)

**Solar Returns parameters**: `year`, `month`, `day`, `hour`, `lat`, `lon`, `solar_return_year`

## Example Request

```bash
curl "http://localhost:8000/planetary_positions?year=1990&month=9&day=5&lat=55.3948&lon=43.8399"
```

## Planets Tracked

Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

## Project Structure

```
immanuel-api/
├── app.py              # FastAPI application and route definitions
├── utils.py            # Forecast calculation utilities
├── test_app.py         # Test suite
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── .env                # Environment variables (ephemeris path)
└── data/               # Swiss Ephemeris data files
```

## Testing

```bash
pytest test_app.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SE_EPHE_PATH` | `./data` | Path to Swiss Ephemeris data files |

## License

See repository for license details.
