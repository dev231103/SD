import os
from datetime import datetime, timedelta
import pandas as pd
import sqlite3 as sq
import uuid
from pytz import timezone

# Configuration
Base = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'
Company = '01-Vermeulen'
active_timezones = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Kolkata']
numUnits = 24 * 7  # Generate one week of hourly timestamps for testing

# SQLite setup
sDataBaseDir = os.path.join(Base, Company, '03-Process', 'SQLite')
os.makedirs(sDataBaseDir, exist_ok=True)
conn1 = sq.connect(os.path.join(sDataBaseDir, 'Hillman.db'))

# Generate hourly timestamps
base = datetime(2018, 1, 1, 0, 0, 0)
date_list = [base - timedelta(hours=x) for x in range(numUnits)]

# Create DataFrame with timezone-aware UTC timestamps
TimeFrame = pd.DataFrame({
    'IDNumber': [str(uuid.uuid4()) for _ in date_list],
    'ZoneBaseKey': 'UTC',
    'nDateTimeValue': pd.to_datetime(date_list).tz_localize('UTC'),
    'DateTimeKey': [dt.strftime("%Y-%m-%d-%H-%M-%S") for dt in date_list],
    'DateTimeValue': [dt.strftime("%Y-%m-%d %H:%M:%S") for dt in date_list]
})

# Store initial data in SQLite
TimeHub = TimeFrame[['IDNumber', 'ZoneBaseKey', 'DateTimeKey', 'DateTimeValue']]
TimeHub.to_sql('Process-Time', conn1, if_exists="replace", index=False)

# Process each time zone
for zone in active_timezones:
    print(f"Processing time zone: {zone}")
    TimeFrame['ZoneDateTime'] = TimeFrame['nDateTimeValue'].dt.tz_convert(zone).dt.strftime("%Y-%m-%d %H:%M:%S")
    TimeFrame['Zone'] = zone
    TimeFrame['IDZoneNumber'] = [str(uuid.uuid4()) for _ in range(len(TimeFrame))]

    # Save to SQLite
    sZone = zone.replace('/', '-').replace(' ', '')
    TimeZoneFrame = TimeFrame[['IDZoneNumber', 'ZoneBaseKey', 'DateTimeKey', 'DateTimeValue', 'Zone', 'ZoneDateTime']]
    TimeZoneFrame.to_sql(f'Process-Time-{sZone}', conn1, if_exists="replace", index=False)

print("Processing completed successfully!")
