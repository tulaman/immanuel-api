from datetime import datetime, timedelta
from immanuel.tools import calculate, convert, date, ephemeris
from immanuel.const import chart, calc

planets = [
    chart.MERCURY,
    chart.VENUS,
    chart.MARS,
    chart.JUPITER,
    chart.SATURN,
    chart.URANUS,
    chart.NEPTUNE,
    chart.PLUTO,
    chart.CHIRON,
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
