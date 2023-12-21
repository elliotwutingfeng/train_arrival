import json

from train_arrival import (
    get_all_station_names,
    get_all_train_arrival_time,
    get_train_arrival_time_by_id,
)


def _verify_arrival_time_response(d):
    assert "results" in d
    assert isinstance(d["results"], list)
    assert d["results"]
    first_result = d["results"][0]
    assert isinstance(first_result, dict)


def test_get_all_station_names():
    assert len(get_all_station_names()) >= 166


def test_get_train_arrival_time_by_id():
    test_cases = (("Raffles Place", "EW14,NS26"), ("Farrer Road", "CC20"))
    for test_case in test_cases:
        expected_station_name, expected_station_code = test_case[0], test_case[1]
        res = get_train_arrival_time_by_id(expected_station_name)
        arrival_time_response = json.loads(res)
        _verify_arrival_time_response(arrival_time_response)
        first_result = arrival_time_response["results"][0]
        assert first_result.get("code", "") == expected_station_code
        assert first_result.get("mrt", expected_station_name)


def test_get_all_train_arrival_time():
    res = get_all_train_arrival_time(3)
    arrival_time_responses = json.loads(res)
    assert len(arrival_time_responses) == 3
    for station_name, arrival_time_response in arrival_time_responses.items():
        _verify_arrival_time_response(arrival_time_response)
        first_result = arrival_time_response["results"][0]
        assert first_result.get("mrt", station_name)
