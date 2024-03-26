from datetime import datetime, timedelta
from immanuel import charts
from immanuel.tools import calculate, date, ephemeris
from immanuel.const import chart, calc
from immanuel.setup import settings

planets = [
    chart.MERCURY,
    chart.VENUS,
    chart.MARS,
    chart.JUPITER,
    chart.SATURN,
    chart.URANUS,
    chart.NEPTUNE,
    chart.PLUTO,
]

planet_names = [
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
]

def retrograde_periods(n, lat, lon):
    retro_table = {obj: [] for obj in planets}

    coords = [lat, lon]

    # Get the current date and time
    now = datetime.now()
    end_date = now + timedelta(days=n * 30)

    start_day = datetime(now.year, now.month, now.day, 0, 0, 0, 0, None)
    end_day = datetime(end_date.year, end_date.month, end_date.day, 0, 0, 0, 0, None)

    buffer = {
        obj: {
            "start": None,
            "end": None,
            "current_direction": calc.DIRECT,
        }
        for obj in planets
    }

    current_day = start_day
    while current_day < end_day:
        day_jd = date.to_jd(current_day)
        objects = ephemeris.objects(
            tuple(planets),
            day_jd,
            *coords,
            chart.PLACIDUS,
            calc.DAY_NIGHT_FORMULA,
        ).values()
        for obj in list(objects):
            movement = calculate.object_movement(obj)
            if (
                movement == calc.RETROGRADE
                and buffer[obj["index"]]["current_direction"] == calc.DIRECT
            ):
                buffer[obj["index"]]["start"] = current_day
                buffer[obj["index"]]["current_direction"] = calc.RETROGRADE
            elif (
                movement == calc.DIRECT
                and buffer[obj["index"]]["current_direction"] == calc.RETROGRADE
            ):
                buffer[obj["index"]]["end"] = current_day
                buffer[obj["index"]]["current_direction"] = calc.DIRECT
                retro_table[obj["index"]].append(
                    (buffer[obj["index"]]["start"], buffer[obj["index"]]["end"])
                )
        current_day = current_day + timedelta(minutes=30)

    for obj in buffer:
        if (
            buffer[obj]["current_direction"] == calc.RETROGRADE
            and buffer[obj]["start"] != None
            and buffer[obj]["end"] == None
        ):
            retro_table[obj].append((buffer[obj]["start"], end_day))

    return retro_table


def weekly_forecast_data(start_date):
    settings.set({"objects": planets})

    # Preparing data for weekly forecast
    weekly_data = {}

    for i in range(7):  # for each day of week
        date = start_date + timedelta(days=i)

        native = charts.Subject(date_time=date, latitude=0.0, longitude=0.0)
        natal = charts.Natal(native)

        planet_positions = {}
        for object in natal.objects.values():
            planet_positions[object.name] = {
                "sign": object.sign.name,
                "house": object.house.number,
                "movement": object.movement.formatted,
            }

        planet_aspects = []
        aspects_set = set()
        for index, aspects in natal.aspects.items():
            for aspect in aspects.values():
                aspect_key = aspect._active_name + " " + aspect._passive_name
                if aspect_key not in aspects_set:
                    planet_aspects.append(
                        {
                            "active": aspect._active_name,
                            "passive": aspect._passive_name,
                            "aspect": aspect.aspect,
                            "type": aspect.type,
                        }
                    )
                    aspects_set.add(aspect_key)

        weekly_data[date.strftime("%Y-%m-%d")] = {
            "moon_phase": natal.moon_phase.formatted,
            "planets": planet_positions,
            "aspects": planet_aspects,
        }

    return weekly_data


def yearly_forecast_data(start_date):
    settings.set({"objects": planets})

    yearly_data = {}
    cursor = {}
    planet_positions = {}
    for object in planet_names:
        planet_positions[object] = {"sign": [], "movement": []}

    for i in range(365):  # for each day of week
        date = start_date + timedelta(days=i)

        native = charts.Subject(date_time=date, latitude=0.0, longitude=0.0)
        natal = charts.Natal(native)

        for object in natal.objects.values():
            if cursor.get(object.name) is None:
                cursor[object.name] = {}
                for key in ["sign", "movement"]:
                    attr = getattr(object, key)
                    cursor[object.name][key] = {
                        "value": attr.formatted if key == "movement" else attr.name,
                        "start": date,
                    }
            else:
                for key in ["sign", "movement"]:
                    attr = getattr(object, key)
                    value = attr.formatted if key == "movement" else attr.name
                    if cursor[object.name][key]["value"] != value:
                        period = f'{cursor[object.name][key]["start"].strftime("%Y-%m-%d")} - {(date - timedelta(days=1)).strftime("%Y-%m-%d")}'
                        planet_positions[object.name][key].append(
                            {
                                "period": period,
                                "value": cursor[object.name][key]["value"],
                            }
                        )
                        cursor[object.name][key] = {
                            "value": value,
                            "start": date,
                        }

    for object in planet_names:
        for key in ["sign", "movement"]:
            period = f'{cursor[object][key]["start"].strftime("%Y-%m-%d")} - {(start_date + timedelta(days=365)).strftime("%Y-%m-%d")}'
            planet_positions[object][key].append(
                {
                    "period": period,
                    "value": cursor[object][key]["value"],
                }
            )

    return planet_positions
