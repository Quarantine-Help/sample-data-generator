import logging
import typing

import pycountry as pycountry
import requests
from django.conf import settings
from faker import Faker
from faker_e164.providers import E164Provider


class DataGenerator(object):
    type = None
    longitude = None
    latitude = None
    amount = None
    HERE_MAPS_BROWSE_API = "https://browse.search.hereapi.com/v1/browse"
    countries_alpha_maps: typing.Dict[str, str] = {}

    def __init__(self, type, latitude, longitude, amount=10):
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.amount = amount
        self.faker: Faker = Faker("en")
        self.faker.add_provider(E164Provider)
        self.countries_alpha_maps = {}

    def prettify_post_code(self, post_code=None):
        """
        So apparently postcode can have hiphens. We dont want that. can be
        DE-12354
        :return:
        """
        post_code = post_code.strip()
        if "-" not in post_code:
            return post_code

        post_code = post_code.split("-")[1].strip()
        post_code = post_code.replace(" ", "")
        if not post_code.isdigit():
            return "12644"

        return post_code

    def generate_dummy_participant_data(self, places_information: typing.List):
        """
        We need data of the format:
        {
              "user": {
                "firstName": "Patient First Test with 6",
                "lastName": "Patient last",
                "email": "patientssss2dsddgfg@patient.com",
                "password": "YEEHA"
              },
              "position": {
                "longitude": "2.7105760574340807",
                "latitude": "48.19827663849882"
              },
              "type": "AF",
              "firstLineOfAddress": "First Line of add",
              "secondLineOfAddress": "Second line",
              "placeId": "ChIJwyyKo7J3X0YRZ5XOMcLx3xo",
              "postCode": "12345",
              "city": "Berlin",
              "country": "DE",
              "crisis": 1,
              "phone": "+46761189391"
        }
        :param places_information:
        :return:
        """
        faked_data = []
        for place_information in places_information:
            address_information = place_information["address"]
            post_code = address_information.get("postalCode", None)
            if not post_code:
                logging.info(f"Skipping: {place_information} due to no post " f"code")
                continue

            fake_data = {"postCode": self.prettify_post_code(post_code)}
            user_data = {
                "firstName": self.faker.first_name(),
                "lastName": self.faker.first_name(),
                "email": self.faker.email(),
            }
            fake_data["user"] = user_data
            fake_data["position"] = {
                "longitude": place_information["position"]["lng"],
                "latitude": place_information["position"]["lat"],
            }
            fake_data["type"] = self.type
            if place_information["resultType"] == "houseNumber":
                fake_data["firstLineOfAddress"] = (
                    f"{address_information['street']}"
                    f" {address_information['houseNumber']}"
                )
            else:
                fake_data["firstLineOfAddress"] = address_information["street"]

            fake_data["placeId"] = place_information["id"]
            fake_data["secondLineOfAddress"] = address_information.get(
                "district", "-/-"
            )
            fake_data["phone"] = self.faker.e164(
                region_code="GB", valid=True, possible=True
            )
            fake_data["city"] = address_information["city"]
            fake_data["country"] = self.transform_to_alpha2(
                address_information["countryCode"]
            )
            fake_data["crisis"] = 1
            faked_data.append(fake_data)
        return faked_data

    def get_places_nearby(self):
        here_maps_result = requests.get(
            f"{self.HERE_MAPS_BROWSE_API}",
            params={
                "apiKey": settings.HERE_MAPS_API_KEY,
                "at": f"{self.latitude},{self.longitude}",
                "additionaldata": "Country2",
                "resultTypes": "street,houseNumber",
                "limit": self.amount,
                "in": f"circle:{self.latitude},{self.longitude};r=2500000",
            },
        )
        here_maps_result_decoded = here_maps_result.json()
        # Now we have like 10 results. Return them for future processing.
        return here_maps_result_decoded["items"]

    def generate_dummy_data(self):
        # First, we need to get amount places nearby
        places_nearby = self.get_places_nearby()
        return self.generate_dummy_participant_data(places_information=places_nearby)

    def transform_to_alpha2(self, alpha_three_code=None):
        alpha_three_code_from_cache = self.countries_alpha_maps.get(
            alpha_three_code, None
        )
        if alpha_three_code_from_cache:
            return alpha_three_code_from_cache
        # Else lookup from pycountries
        country_alpha_2 = pycountry.countries.get(alpha_3=alpha_three_code).alpha_2
        self.countries_alpha_maps.update({alpha_three_code: country_alpha_2})
        return country_alpha_2
