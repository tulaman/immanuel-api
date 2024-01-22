from datetime import datetime
import json
from fastapi import FastAPI, Query, Header
from fastapi.responses import RedirectResponse, PlainTextResponse
from typing import Annotated
from pydantic import BaseModel
import starlette.status as status
from immanuel import charts
from immanuel.const import chart
from immanuel.classes.serialize import ToJSON

tags_metadata = [
    {
        "name": "planetary_positions",
        "description": "Planetary positions for a given date and time",
    }
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
            description="Longitude of birth place (e.g. 74.0060",
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
