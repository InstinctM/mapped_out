from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

opencageKey="06fee6e0f0fd4b82972c28992c487837"
geocoder=OpenCageGeocode(opencageKey)

latitude=53.46719182070933
longitude=-2.2341700730222045
try:
    results=geocoder.reverse_geocode(latitude,longitude,language='en')
    if results and len(results):
        print(results[0]['formatted'])
except RateLimitExceededError as err:
    print(err)
except InvalidInputError as err:
    print(err)
