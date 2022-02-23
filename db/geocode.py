from __future__ import annotations
from argparse import ArgumentError
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

opencageKey="06fee6e0f0fd4b82972c28992c487837"
geocoder=OpenCageGeocode(opencageKey)

def add_post(link, description, author, latitude=None, longitude=None, location=None):
    #if given both coordinates and a text location (address) not going to check they are in the same place

    assert ((longitude!=None and latitude!=None) or location!=None), "Incorrect location Data given"

    if (longitude==None and latitude==None ) and location!=None:
        pass #forward geocoding

    elif (location==None) and (longitude!=None and latitude!=None):
        pass


def forward_geocode(location):
    try:
        results=geocoder.forward_geocode(location,language='en',limit=1, annotations=1)
        if results and len(results):
            return (results[0]['geometry']['lat'],results[0]['geometry']['lng'])
    except RateLimitExceededError as err:
        print(err)
    except InvalidInputError as err:
        print(err)


def reverse_geocode(latitude, longitude):
    try:
        results=geocoder.reverse_geocode(latitude,longitude,language='en',limit=1, annotations=1)
        if results and len(results):
            return (results[0]['formatted'])
    except RateLimitExceededError as err:
        print(err)
    except InvalidInputError as err:
        print(err)
