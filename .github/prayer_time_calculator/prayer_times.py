import argparse
from dataclasses import dataclass
import datetime
from typing import Optional

from pyIslam.praytimes import (
    PrayerConf,
    Prayer,
    LIST_FAJR_ISHA_METHODS,
)
from pyIslam.hijri import HijriDate
from pyIslam.qiblah import Qiblah

NEWLINE = '\n'  # Can't use `\` with f-string


@dataclass
class PrayerTimeMetaData:
    date: datetime.date
    longitude: float
    latitude: float
    gmt_offset: float
    fajr_isha_method: int
    asr_fiqh: int

@dataclass
class PrayerWaqtTimes:
    meta: PrayerTimeMetaData

    fajr: datetime.datetime
    zuhr: datetime.datetime
    asr: datetime.datetime
    maghrib: datetime.datetime
    isha: datetime.datetime

    shurooq: datetime.datetime  # Sunrise


def calculate_prayer_times(
    longitude: float,
    latitude: float,
    gmt_offset: float,
    fajr_isha_method: int,
    asr_fiqh: int,
    prayer_date: Optional[datetime.date] = None,
    verbose: bool = False
) -> PrayerWaqtTimes:
    prayer_date = prayer_date or datetime.date.today()

    pconf = PrayerConf(longitude, latitude, gmt_offset, fajr_isha_method, asr_fiqh)

    meta = PrayerTimeMetaData(
        date=prayer_date,
        longitude=longitude,
        latitude=latitude,
        gmt_offset=gmt_offset,
        fajr_isha_method=fajr_isha_method,
        asr_fiqh=asr_fiqh
    )

    prayer_times = Prayer(pconf, prayer_date)

    return PrayerWaqtTimes(
        meta=meta,
        fajr=prayer_times.fajr_time(),
        zuhr=prayer_times.dohr_time(),
        asr=prayer_times.asr_time(),
        maghrib=prayer_times.maghreb_time(),
        isha=prayer_times.ishaa_time(),
        shurooq=prayer_times.sherook_time()
    )

if __name__ == "__main__":
    available_codes = "Available Fajr and Isha methods:\n"
    for method in LIST_FAJR_ISHA_METHODS:
        available_codes += f"  {method.id}) {' | '.join(method.organizations)}\n"
    available_codes += "\nAvailable Asr Fiqh methods:\n  1) Shafii, Maliki, Hambali\n  2) Hanafi"

    parser =  argparse.ArgumentParser(description="Calculate prayer times", epilog=available_codes,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--longitude", type=float, required=True, help="Longitude of the location")
    parser.add_argument("--latitude", type=float, required=True, help="Latitude of the location")
    parser.add_argument("--gmt-offset", type=float, required=True, help="GMT offset of the location. Only provide the number, not the GMT prefix. Ex: -5 for EST")
    parser.add_argument("--fajr-isha-method", type=int, required=True, help="Pass the ID (int) of the organization")
    parser.add_argument("--asr-fiqh", type=int, required=True, help="Pass the ID (int) of the organization")
    parser.add_argument("--prayer-date", help="Date for which you want to calculate the prayer times. Format: YYYY-MM-DD",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(), default=datetime.date.today())
    results = parser.parse_args()

    print(
        calculate_prayer_times(
            longitude=results.longitude,
            latitude=results.latitude,
            gmt_offset=results.gmt_offset,
            fajr_isha_method=results.fajr_isha_method,
            asr_fiqh=results.asr_fiqh,
            prayer_date=results.prayer_date,
            verbose=True
        )
    )
