from datetime import datetime, date, time
from fastapi import FastAPI, Query, Header
from fastapi.responses import RedirectResponse, PlainTextResponse
from typing import Annotated
from pydantic import BaseModel
import starlette.status as status
from immanuel import charts
from immanuel.const import chart, names
from utils import retrograde_periods, weekly_forecast_data, yearly_forecast_data

tags_metadata = [
    {
        "name": "planetary_positions",
        "description": "Planetary positions for a given date and time",
    },
    {
        "name": "retrograde_calendar",
        "description": "Retrograde calendar for a given year",
    },
    {
        "name": "get_weekly_forecast_data",
        "description": "Get weekly forecast data - planet positions, major aspects, retrograde etc - for a given date",
    },
    {
        "name": "get_yearly_forecast_data",
        "description": "Get yearly forecast data - retrogrades, direct stations and ingresses represented as periods of time for each planet",
    },
]

app = FastAPI(
    title="Skylar May API",
    description="API for building astrological charts. Based on swisseph and immanuel.",
    version="0.0.1",
    license_info={"name": "MIT License", "identifier": "MIT"},
    openapi_tags=tags_metadata,
)


class PlanetDescription(BaseModel):
    name: str
    latitude: str
    longitude: str
    sign: str
    sign_longitude: str
    house: str
    speed: float
    distance: float
    movement: str


class PlanetPositionsResponse(BaseModel):
    success: int
    data: list[PlanetDescription]


class Period(BaseModel):
    start: date
    end: date


class PeriodsForPlanet(BaseModel):
    planet: str
    periods: list[Period]


class RetrogradeCalendarResponse(BaseModel):
    success: int
    data: list[PeriodsForPlanet]


@app.get("/")
def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.get("/planetary_positions", tags=["planetary_positions"])
def planetary_positions(
    year: Annotated[
        int,
        Query(
            title="Year",
            description="Year of birth (e.g. 1990)",
            examples=[1990],
        ),
    ],
    month: Annotated[
        int,
        Query(
            title="Month",
            description="Month of birth (e.g. 9)",
            examples=[9],
        ),
    ],
    day: Annotated[
        int,
        Query(
            title="Day",
            description="Birth day (e.g. 5)",
            examples=[5],
        ),
    ],
    lat: Annotated[
        float,
        Query(
            title="Latitude",
            description="Latitude of birth place (e.g. 40.7128)",
            examples=[55.3948],
        ),
    ],
    lon: Annotated[
        float,
        Query(
            title="Longitude",
            description="Longitude of birth place (e.g. 74.0060)",
            examples=[43.8399],
        ),
    ],
    hour: Annotated[
        int,
        Query(
            title="Hour",
            description="Hour of birth, if you know it (e.g. 12)",
            examples=[15],
        ),
    ] = 0,
    min: Annotated[
        int,
        Query(
            title="Minute",
            description="Minute of birth, if you know it (e.g. 01)",
            examples=[1],
        ),
    ] = 0,
    sec: Annotated[
        int,
        Query(
            title="Second",
            description="Second of birth, if you know it (e.g. 53)",
            examples=[53],
        ),
    ] = 0,
    x_token: Annotated[
        str | None,
        Header(
            title="X-Token",
            description="Your API key",
            examples=["3bbfdde8842a5c44a0323518eec97cbe"],
        ),
    ] = None,
) -> PlanetPositionsResponse:
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    natal_chart = charts.Natal(native)
    objects = []
    for obj in natal_chart.objects.values():
        if obj.type.index == chart.PLANET:
            objects.append(
                {
                    "name": obj.name,
                    "latitude": obj.latitude.formatted,
                    "longitude": obj.longitude.formatted,
                    "sign": obj.sign.name,
                    "sign_longitude": obj.sign_longitude.formatted,
                    "house": obj.house.name,
                    "speed": obj.speed,
                    "distance": obj.distance,
                    "movement": obj.movement.formatted,
                }
            )
    return {"success": 1, "data": objects}


@app.get("/retrograde_calendar", tags=["retrograde_calendar"])
def retrograde_calendar(
    n: Annotated[
        int,
        Query(
            title="N of months",
            description="Number of next months to show calendar for",
            examples=[12],
        ),
    ],
    lat: Annotated[
        float,
        Query(
            title="Latitude",
            description="Latitude of observer place",
            examples=[55.3948],
        ),
    ],
    lon: Annotated[
        float,
        Query(
            title="Longitude",
            description="Longitude of observer place",
            examples=[43.8399],
        ),
    ],
    x_token: Annotated[
        str | None,
        Header(
            title="X-Token",
            description="Your API key",
            examples=["3bbfdde8842a5c44a0323518eec97cbe"],
        ),
    ] = None,
) -> RetrogradeCalendarResponse:
    retro_table = retrograde_periods(n, lat, lon)
    response = []
    for obj, days in retro_table.items():
        asteroid = round(obj, -2) == chart.ASTEROID
        name = names.ASTEROIDS[obj] if asteroid else names.PLANETS[obj]
        response.append(
            {
                "planet": name,
                "periods": [{"start": x[0].date(), "end": x[1].date()} for x in days],
            }
        )
    return {"success": 1, "data": response}


@app.get("/natal.json")
def natal_text(
    year: Annotated[
        int,
        Query(
            title="Year",
            description="Year of birth (e.g. 1990)",
        ),
    ],
    month: Annotated[
        int,
        Query(
            title="Month",
            description="Month of birth (e.g. 9)",
        ),
    ],
    day: Annotated[
        int,
        Query(
            title="Day",
            description="Birth day (e.g. 5)",
        ),
    ],
    lat: Annotated[
        float,
        Query(
            title="Latitude",
            description="Latitude of birth place (e.g. 40.7128)",
        ),
    ],
    lon: Annotated[
        float,
        Query(
            title="Longitude",
            description="Longitude of birth place (e.g. 74.0060",
        ),
    ],
    hour: Annotated[
        int,
        Query(
            title="Hour",
            description="Hour of birth, if you know it (e.g. 12)",
        ),
    ] = 0,
    min: Annotated[
        int,
        Query(
            title="Minute",
            description="Minute of birth, if you know it (e.g. 01)",
        ),
    ] = 0,
    sec: Annotated[
        int,
        Query(
            title="Second",
            description="Second of birth, if you know it (e.g. 53)",
        ),
    ] = 0,
    x_token: Annotated[
        str | None,
        Header(
            title="X-Token",
            description="Your API key",
        ),
    ] = None,
):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    # return json.loads( json.dumps(charts.Natal(native), cls=ToJSON, indent=4) )
    return charts.Natal(native)


@app.get("/natal.txt")
def natal_text(
    year: Annotated[
        int,
        Query(
            title="Year",
            description="Year of birth (e.g. 1990)",
        ),
    ],
    month: Annotated[
        int,
        Query(
            title="Month",
            description="Month of birth (e.g. 9)",
        ),
    ],
    day: Annotated[
        int,
        Query(
            title="Day",
            description="Birth day (e.g. 5)",
        ),
    ],
    lat: Annotated[
        float,
        Query(
            title="Latitude",
            description="Latitude of birth place (e.g. 40.7128)",
        ),
    ],
    lon: Annotated[
        float,
        Query(
            title="Longitude",
            description="Longitude of birth place (e.g. 74.0060",
        ),
    ],
    hour: Annotated[
        int,
        Query(
            title="Hour",
            description="Hour of birth, if you know it (e.g. 12)",
        ),
    ] = 0,
    min: Annotated[
        int,
        Query(
            title="Minute",
            description="Minute of birth, if you know it (e.g. 01)",
        ),
    ] = 0,
    sec: Annotated[
        int,
        Query(
            title="Second",
            description="Second of birth, if you know it (e.g. 53)",
        ),
    ] = 0,
    x_token: Annotated[
        str | None,
        Header(
            title="X-Token",
            description="Your API key",
        ),
    ] = None,
):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    # return json.loads( json.dumps(charts.Natal(native), cls=ToJSON, indent=4) )
    natal = charts.Natal(native)
    objects = ""
    for object in natal.objects.values():
        objects += f"{object}\n"
    response = f"""
Daytime: {natal.diurnal}
Moon Phase: {natal.moon_phase}
{objects}
"""
    return PlainTextResponse(response)


@app.post("/transits")
def transits(year: int, month: int, day: int, hour: int, lat: float, lon: float):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    return charts.Transits(native)


@app.post("/progressions")
def progressions(year: int, month: int, day: int, hour: int, lat: float, lon: float):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    return charts.Progressed(native)


@app.post("/synastry")
def synastry(
    year: int,
    month: int,
    day: int,
    hour: int,
    lat: float,
    lon: float,
    year2: int,
    month2: int,
    day2: int,
    hour2: int,
    lat2: float,
    lon2: float,
):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    native2 = charts.Subject(datetime(year2, month2, day2, hour2, 0, 0), lat2, lon2)
    return charts.Synastry(native, native2)


@app.post("/composite")
def composite(
    year: int,
    month: int,
    day: int,
    hour: int,
    lat: float,
    lon: float,
    year2: int,
    month2: int,
    day2: int,
    hour2: int,
    lat2: float,
    lon2: float,
):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    native2 = charts.Subject(datetime(year2, month2, day2, hour2, 0, 0), lat2, lon2)
    return charts.Composite(native, native2)


@app.post("/solar_returns")
def solar_returns(year: int, month: int, day: int, hour: int, lat: float, lon: float):
    native = charts.Subject(datetime(year, month, day, hour, 0, 0), lat, lon)
    return charts.SolarReturns(native)


@app.get("/get_weekly_forecast_data", tags=["get_weekly_forecast_data"])
def get_weekly_forecast_data(
    start_date: Annotated[
        date,
        Query(
            title="Start date",
            description="Start date for the forecast",
            examples=[date.today()],
        ),
    ],
):
    datetime_obj = datetime.combine(start_date, time.min)
    wfd = weekly_forecast_data(datetime_obj)
    return {"success": 1, "data": wfd}


@app.get("/get_yearly_forecast_data", tags=["get_yearly_forecast_data"])
def get_yearly_forecast_data(
    start_date: Annotated[
        date,
        Query(
            title="Start date",
            description="Start date for the forecast",
            examples=[date.today()],
        ),
    ],
):
    datetime_obj = datetime.combine(start_date, time.min)
    yfd = yearly_forecast_data(datetime_obj)
    return {"success": 1, "data": yfd}
