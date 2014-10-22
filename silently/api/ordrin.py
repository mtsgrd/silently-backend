# -*- coding: utf-8 -*-

from flask import request
from ..core import cache, ordrin_api
from flask_socketio import emit

@cache.memoize(timeout='86400')
def get_restaurants(address):
    """Retrieves a restaurant list from ordrin.

    This function should be cached once it's clear if the address fields
    are necessary input.

    Args:
        zip_code (int): The current zip code of the user.
    """
    data = ordrin_api.delivery_list('ASAP', address['number'] + ' ' + address['street'],
            address['city'], address['zip'])
    restaurants = []
    for entry in data:
        restaurant = {'name': entry['na'],
                      'id': entry['id'],
                      'address': entry['addr'],
                      'location': [float(entry['latitude']),
                                   float(entry['longitude'])],
                      'phone': entry['cs_phone'],
                      'partner': entry['rds_info']['name'],
                      'allows_asap': entry['allow_asap'] == 'yes',
                      'delivery_time': entry['del'],
                      'minimum_order': entry['mino'],
                      'taking_orders': entry['is_delivering'] == True}
        restaurants.append(restaurant)
    return restaurants

@cache.memoize(timeout='86400')
def get_details(restaurant_id):
    """Retrieves a restaurant list from ordrin.

    The JSON response from the ordr.in API is a bit of a mess so we clean up
    the response.

    Most notably, the restaurant id returned in the lists are integers
    whereas the detail endpoint expects and returns them as strings.

    Args:
        zip_code (int): The current zip code of the user.
    """
    restaurant_id = str(restaurant_id)
    details = ordrin_api.restaurant_details(restaurant_id)

    menu = {'categories': []}
    for category in details['menu']:
        category_dict  = {'name': category['name'],
                          'items': []}
        menu['categories'].append(category_dict)
        for item in category['children']:
            item_dict = {'item_id': item['id'],
                         'name': item['name'],
                         'price': item['price'],
                         'choices': []}
            category_dict['items'].append(item_dict)
            for choice in item.get('children', []):
                choice_dict = {'choice_id': choice['id'],
                               'name': choice['name'],
                               'price': choice['price'],
                               'options': []}
                item_dict['choices'].append(choice_dict)
                for option in choice.get('children', []):
                    option_id = option['id']
                    option_name = option['name']
                    option_price = option['price']
                    option_dict = {'option_id': option['id'],
                                   'name': option['name'],
                                   'price': option['price']}
                    choice_dict['options'].append(option_dict)

    clean_info = {'id': int(details['restaurant_id']),
                  'menu' : menu}
    return clean_info
