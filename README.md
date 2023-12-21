<div align="center">

  <h3 align="center">Train Arrival</h3>
  <img src="images/train.svg" alt="Train" width="200" height="200">

  <p align="center">
    Extract train arrival information from the SMRT <a href="https://trainarrivalweb.smrt.com.sg">Train Arrival Information</a> API.
  </p>

  <p align="center">
    <strong>Output format:</strong> JSON string
  </p>

  <p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"/></a>
  </p>

  <p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-GREEN?style=for-the-badge" alt="MIT license"/></a>
  <a href="https://coveralls.io/github/elliotwutingfeng/train_arrival?branch=main"><img src="https://img.shields.io/coverallsCoverage/github/elliotwutingfeng/train_arrival?logo=coveralls&style=for-the-badge" alt="Coveralls"/></a>
  <img src='https://coveralls.io/repos/github/elliotwutingfeng/train_arrival/badge.svg?branch=main' alt='' width="0" height="0" />
  </p>

</div>

**Disclaimer:** This project is not sponsored, endorsed, or otherwise affiliated with SMRT Corporation.

## Requirements

Python 2.7 or 3

## Usage

```python
get_all_station_info()
"""
'{"count": 166, "next": null, "previous": null, "results": [{"name": "Admiralty", "code": "NS10", ...'
"""

get_all_station_names()
"""
['Admiralty',
 'Aljunied',
 'Ang Mo Kio',
 'Bakau',
 ...
]
"""

get_train_arrival_time_by_id("Paya Lebar")
"""
'{"results":[{"status":1,"platform_ID":"CPYL_A","code":"CC9,EW8","next_train_arr":"7","mrt":"Paya Lebar", ...'
"""

get_all_train_arrival_time()
"""
'{"Admiralty": {"results": [{"status": 1, "platform_ID": "ADM_A", "code": "NS10", "next_train_arr": "6", ...'
"""
```

## Warning

- This API appears not to be intended by SMRT for public use. You are solely [responsible](LICENSE) for your use of this application.

## Credits

- [RailRouter SG](https://github.com/cheeaun/railrouter-sg) for information on accessing the SMRT API.
- Logo modified from public domain vector at [svgrepo.com](https://www.svgrepo.com/svg/63666/singapore-metro-logo).
