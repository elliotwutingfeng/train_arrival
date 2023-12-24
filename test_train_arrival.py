import json
import unittest

from train_arrival import (
    get_all_station_names,
    get_all_train_arrival_time,
    get_train_arrival_time_by_id,
)


class TestTrainArrival(unittest.TestCase):
    @staticmethod
    def _verify_arrival_time_response(
        arrival_time_response, expected_station_name, expected_station_code=None
    ):
        assert "results" in arrival_time_response
        results = arrival_time_response["results"]
        assert isinstance(results, list)
        if not results:
            return
        assert all(isinstance(result, dict) for result in results)

        station_names = set(result.get("mrt", "") for result in results) - set([""])
        station_codes = set(result.get("code", "") for result in results) - set([""])
        assert len(station_codes) == 1
        assert expected_station_code is None or expected_station_code in station_codes
        assert len(station_names) == 1
        assert expected_station_name in station_names

    def test_get_all_station_names(self):
        assert len(get_all_station_names()) >= 166

    def test_get_train_arrival_time_by_id(self):
        test_cases = (
            ("Raffles Place", "EW14,NS26"),
            ("Farrer Road", "CC20"),
            ("Not A Real Station", ""),
        )
        for test_case in test_cases:
            expected_station_name, expected_station_code = test_case[0], test_case[1]
            res = get_train_arrival_time_by_id(expected_station_name)
            arrival_time_response = json.loads(res)  # type: dict
            if expected_station_name == "Not A Real Station":
                assert arrival_time_response.get("results", None) == []
                continue
            TestTrainArrival._verify_arrival_time_response(
                arrival_time_response, expected_station_name, expected_station_code
            )

    def test_get_all_train_arrival_time(self):
        limit = 5
        res = get_all_train_arrival_time(limit)
        arrival_time_responses = json.loads(res)
        assert len(arrival_time_responses) == limit
        for station_name, arrival_time_response in arrival_time_responses.items():
            TestTrainArrival._verify_arrival_time_response(
                arrival_time_response, station_name
            )


if __name__ == "__main__":
    unittest.main()
