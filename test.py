#!/usr/bin/env python

import json
from utils import weekly_forecast_data
from datetime import datetime, date

# Get the current date and time
now = datetime.now()

# Get the weekly forecast data
data = weekly_forecast_data(now)
print(json.dumps(data, indent=4))
