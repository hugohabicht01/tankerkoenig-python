# Tankerkoenig-Python
Python wrapper for the creativecommons.tankerkoenig.de API

Note: The API is under Creative Commons (CC BY 4.0) license. It is used by many clients so please restrict API calls to the minimum.
Every request requires an API key that can be requested [here](https://creativecommons.tankerkoenig.de/#register)

## Examples
Finding petrol stations around a certain coordinate:
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

Accessing details of a station by its ID:
```python
import tankerkoenig

client = tankerkoenig.Client(api_key="00000000-0000-0000-0000-000000000002")

details = client.details(id="24a381e3-0d72-416d-bfd8-b2f65f6e5802")
print(details)
# Details_Model(
#     ok=True,
#     license='CC BY 4.0 -  https://creativecommons.tankerkoenig.de',
#     data='MTS-K',
#     status='ok',
#     station=Details_Station(
#         id='24a381e3-0d72-416d-bfd8-b2f65f6e5802',
#         name='Esso Tankstelle',
#         brand='ESSO',
#         street='HAUPTSTR. 7',
#         houseNumber=' ',
#         postCode=84152,
#         place='MENGKOFEN',
#         openingTimes=[
#             Details_OpeningTime(
#                 text='Mo-Fr',
#                 start='05:00:00',
#                 end='22:30:00',
#             ),
#             Details_OpeningTime(
#                 text='Samstag',
#                 start='07:00:00',
#                 end='22:30:00',
#             ),
#             Details_OpeningTime(
#                 text='Sonntag, Feiertag',
#                 start='08:00:00',
#                 end='22:30:00',
#             ),
#         ],
#         overrides=[],
#         wholeDay=False,
#         isOpen=True,
#         e5=1.009,
#         e10=1.009,
#         diesel=1.009,
#         lat=48.72210601,
#         lng=12.44438439,
#         state=None,
#     ),
# )
```