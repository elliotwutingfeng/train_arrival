import json
import logging
import sys
import time
from contextlib import closing
from typing import Any

try:
    import urllib.parse as parse
    import urllib.request as request
except ImportError:
    import urllib as parse
    import urllib2 as request

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

REFERER = "http://journey.smrt.com.sg/journey/station_info/"  # Credits: https://github.com/cheeaun/railrouter-sg


def _is_str_or_unicode(s):
    # type: (Any) -> bool
    """Check if `s` is str type in both Python 2 and 3, else if it is
    unicode type in Python 2.

    Args:
        s (Any): Argument to be checked.

    Returns:
        bool: True if `s` is str or unicode type.
    """
    if isinstance(s, str):
        return True
    is_python2 = sys.version_info[0] == 2
    return is_python2 and type(s).__name__ == "unicode"


def _get(url, params=None):
    # type: (str, dict[str, str] | None) ->  str
    """Make a GET request to `url` with optional query parameters `params`.

    Return the body as a string if it is a valid JSON string, otherwise {}.

    Args:
        url (str): Target URL.
        params (dict[str, str], optional): Optional query parameters. Defaults to None.

    Returns:
        str: GET request body.
    """
    if params:
        r = request.Request(url + "?" + parse.urlencode(params))
    else:
        r = request.Request(url)
    r.add_header("Referer", REFERER)

    try:
        with closing(request.urlopen(r, timeout=60)) as f:
            status_code = f.status if hasattr(f, "status") else f.getcode()
            if status_code == 200:
                data = f.read().decode("utf-8")
                _ = json.loads(data)  # Validate JSON string.
                return data
            logger.error(status_code)
            return "{}"
    except Exception as e:
        logger.error(e)
        return "{}"


def get_all_station_info():
    # type: () -> str
    """Get all train station information from SMRT API.

    Returns:
        str: Train station information as JSON string.
    """
    return _get("https://connect.smrt.wwprojects.com/smrt/api/stations")


def get_all_station_names():
    # type: () -> list[str]
    """Get all train station names from SMRT API.

    Returns:
        list[str]: List of train station names in ascending alphabetical order.
    """
    all_stations_info = json.loads(get_all_station_info())  # type: dict
    if not isinstance(all_stations_info, dict):
        all_stations_info = {}
    station_names = set()

    for station_info in all_stations_info.get("results", []):
        if isinstance(station_info, dict) and "name" in station_info:
            station_name = station_info[
                "name"
            ]  # Use station name to get its arrival timings
            if _is_str_or_unicode(station_name) and station_name:
                station_names.add(station_name)
    return sorted(station_names)


def get_train_arrival_time_by_id(station_name):
    # type: (str) -> str
    """Get train arrival times for a given train station as a JSON string.

    Args:
        station_name (str): Name of train station (e.g. City Hall, Eunos etc.)

    Returns:
        str: Train arrival times as a JSON string. If no relevant data is available, return {"results": []}.
    """
    params = {"station": station_name}

    max_attempts = 3

    for attempt in range(max_attempts):
        if attempt:
            time.sleep(
                2 ** (attempt - 1)
            )  # Sleep with exponential backoff for rate-limiting.
        data = _get(
            "https://connectv3.smrt.wwprojects.com/smrt/api/train_arrival_time_by_id",
            params,
        )
        d = json.loads(data)
        if not d.get("results", []):
            continue
        mrt_names = set(result.get("mrt", "") for result in d["results"]) - set([""])
        if (
            len(mrt_names) != 1 or station_name not in mrt_names
        ):  # Ensure that the 'mrt' field matches station name.
            continue
        return data  # Output guaranteed to be valid JSON.
    return '{"results": []}'


def get_all_train_arrival_time(limit=None):
    # type: (int | None) -> str
    """Get train arrival times for all train stations as a JSON string.

    Warning: Estimated execution time is at least 5 minutes.

    Args:
        limit (int | None, optional): Limit search results to
        first N station names in ascending alphabetical order.
        Has no effect if `limit` is not a positive integer or is
        larger than total number of station names. Defaults to None.

    Returns:
        str: Train arrival times for all train stations in
        ascending alphabetical order as a JSON string.
    """
    station_names = get_all_station_names()
    limit = (
        min(limit, len(station_names))
        if isinstance(limit, int) and (0 < limit <= len(station_names))
        else len(station_names)
    )

    results = {
        station_name: json.loads(get_train_arrival_time_by_id(station_name))
        for station_name in station_names[:limit]
    }

    return json.dumps(results)
