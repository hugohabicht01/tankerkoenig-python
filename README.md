# Tankerkoenig-Python
Python wrapper for the creativecommons.tankerkoenig.de API

Note: The API is under Creative Commons (CC BY 4.0) license. It is used by many clients so please restrict API calls to the minimum.
Every request requires an API key that can be requested [here](https://creativecommons.tankerkoenig.de/#register)

## Example
```python
import tankerkoenig

client = tankerkoenig.Client(api_key="00000000-0000-0000-0000-000000000002")

petrol_stations = client.list(
    lat=50.114634,
    lng=8.687657,
    rad=2,
    petrol_type=tankerkoenig.Petrol.DIESEL,
    sort=tankerkoenig.SortingMethod.DISTANCE,
)
print(petrol_stations)
```
