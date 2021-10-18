# kordercore
'''
    This codebase contains exmaples and libraries to use the myKaarma order API
    Copyright (C) 2021 myKaarma

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
'''

import requests

#Keys in the "creds" dict.
KEY_USERNAME = 'username'
KEY_PASSWORD = 'password'
KEY_BASE_URL = 'base_url' #kept so this code can be used in dev and QA as well, not just prod.


def get_orders(creds, department_uuid, filters, DEBUG = False, SIMULATION = False):
    """Gets the orders based on the provided filters"""
    url = "%s/department/%s/order/specificSearch" % (creds[KEY_BASE_URL], department_uuid)
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a POST request to %s with data %s" % (url, filters))
        return "SIMULATION MODE ON"
    else:
        r = requests.post(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]),json=filters)
        raw_response = r.json()
        if DEBUG:
            print(raw_response)
        #TODO check for errors
        return raw_response['orders']


if __name__ == "__main__":
    print('Sorry, no direct usage available. Import and then call the methods.')