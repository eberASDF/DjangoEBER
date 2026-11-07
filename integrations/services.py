import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.cache import cache
from requests import Session
from zeep import Client
from zeep.transports import Transport


SOAP_WSDL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
CHARACTERS = (
    ('Aang', 'Avatar: The Last Airbender'),
    ('Katara', 'Avatar: The Last Airbender'),
    ('Toph', 'Avatar: The Last Airbender'),
    ('Zuko', 'Avatar: The Last Airbender'),
    ('Korra', 'The Legend of Korra'),
    ('Bolin', 'The Legend of Korra'),
)


class ExternalServiceError(Exception):
    pass


def avatar_character_images():
    cached = cache.get('avatar_character_images_v1')
    if cached is not None:
        return cached
    scenes = []
    for name, series in CHARACTERS:
        url = f'https://last-airbender-api.fly.dev/api/v1/characters?{urlencode({"name": name})}'
        try:
            with urlopen(Request(url, headers={'Accept': 'application/json'}), timeout=12) as response:
                characters = json.load(response)
        except Exception as exc:
            raise ExternalServiceError('La API pública de Avatar no respondió en este momento.') from exc
        character = next((item for item in characters if item.get('name', '').casefold() == name.casefold()), None)
        if character and character.get('photoUrl'):
            scenes.append({
                'serie': series,
                'titulo': name,
                'imagen': character['photoUrl'],
                'descripcion': character.get('affiliation') or '',
            })
    if not scenes:
        raise ExternalServiceError('La API pública de Avatar no devolvió imágenes.')
    cache.set('avatar_character_images_v1', scenes, 3600)
    return scenes


def country_capital(country_code):
    session = Session()
    session.verify = True
    transport = Transport(session=session, timeout=8, operation_timeout=8)
    try:
        client = Client(wsdl=SOAP_WSDL, transport=transport)
        return str(client.service.CapitalCity(sCountryISOCode=country_code)).strip()
    except Exception as exc:
        raise ExternalServiceError('El servicio SOAP no respondió en este momento.') from exc
