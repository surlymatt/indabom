import json
import urllib

from .models import Part, Distributor, DistributorPart
from indabom.local_settings import OCTOPART_API_KEY

def match_part(part):
    # returns [{ seller: seller, }]
    query = [{'mpn': part.manufacturer_part_number}]

    url = 'https://octopart.com/api/v3/parts/match?queries=%s' \
        % urllib.quote(json.dumps(query))
    url += '&apikey=' + OCTOPART_API_KEY

    data = urllib.urlopen(url).read()
    response = json.loads(data)

    # need for each part: digi-key, mouser prices, moqs, lead times 
    DIGI_KEY_SELLER_ID = '459'
    MOUSER_SELLER_ID = '2401'

    dps = []
    
    # print mpn's
    for result in response['results']:
        for item in result['items']:
            for offer in item['offers']:
                if offer['seller']['id'] == DIGI_KEY_SELLER_ID or offer['seller']['id'] == MOUSER_SELLER_ID:
                    disty = Distributor.objects.filter(name=offer['seller']['name'])[0]
                    ltd = offer['factory_lead_days']
                    for price in offer['prices']['USD']:
                        moq = price[0]
                        price = price[1]
                        dps.append(DistributorPart(distributor=disty, part=part, minimum_order_quantity=moq, unit_cost=price, lead_time_days=ltd))

    return dps