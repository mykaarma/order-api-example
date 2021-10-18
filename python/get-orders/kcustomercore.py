# kcustomercore
'''
    This codebase contains exmaples and libraries to use the myKaarma order API.
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

def find_vehicle(vehicle_list, vin):
    """Finds a given vehicle in a list, if present"""
    for vehicle in vehicle_list:
        if vehicle['vin'] == vin:
            return vehicle
    return None


def add_customer(creds, dept_uid, customer, DEBUG = False, SIMULATION = False):
    """A simple method to add a new customer.

    This method will take the credentials (username, password, and base URL)
    the departmentUUID, and a DICT matching the customer object structure, and PUT it 
    in the API. An optional DEBUG boolean can be passed that will result in dumping of 
    the HTTP response on stdout. Another optional input SIMULATION, when set to true, will 
    lead to NO network traffic, just the dumping of the request.
    """

    url = "%s/department/%s/customer" % (creds[KEY_BASE_URL],dept_uid)
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a PUT request to %s with data %s" % (url, customer))
        return "SIMULATION MODE ON"
    else:
        r = requests.put(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]), json = customer)
        if DEBUG:
            print(r.json())
        get_url = "%s/department/%s/customer/%s" % (creds[KEY_BASE_URL],dept_uid,r.json()['customerUuid'])
        r = requests.get(get_url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]))
        if DEBUG:
            print(r.json())
        return r.json()["customerWithVehicles"]

def get_customer(creds, department_uuid, search_str, DEBUG = False, SIMULATION = False):
    """Gets the customer based on the provided search string"""
    url = "%s/department/%s/customer/list?searchTerm=%s&searchPreference=customer&maxResults=1" % (creds[KEY_BASE_URL], department_uuid, search_str)
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a GET request to %s" % (url))
        return "SIMULATION MODE ON"
    else:
        r = requests.get(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]))
        raw_response = r.json()
        if DEBUG:
            print(raw_response)
        if raw_response['matchingCount'] == 0:
            return None
        else:
            return raw_response['matchingCustomers'][0]

def get_customer_by_dms_id(creds, department_uuid, dms_id, DEBUG = False, SIMULATION = False):
    """Gets the customer based on the provided DMS ID"""
    url = "%s/department/%s/customer/list?searchTerm=%s&searchPreference=customer&maxResults=50" % (creds[KEY_BASE_URL], department_uuid, dms_id)
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a GET request to %s" % (url))
        return "SIMULATION MODE ON"
    else:
        r = requests.get(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]))
        raw_response = r.json()
        if DEBUG:
            print(raw_response)
        if raw_response['matchingCount'] == 0:
            return None
        else:
            for customer_obj in raw_response['matchingCustomers']:
                try:
                    if customer_obj['customer']['customerKey'] == dms_id:
                        if DEBUG:
                            print("found for %s!" % dms_id)
                        return customer_obj
                except:
                    continue
            # loop ended, not found.
            if DEBUG:
                print("NOTHING found for %s!" % dms_id)
            return None

def get_or_add(creds, dept_uuid, dms_id, first_name, last_name, phone_num, email, vin, DEBUG = False, SIMULATION = False):
    """NOT READY! A method to get a given customer, or add one if none exists"""
    customer_info = get_customer(creds, dept_uuid, dms_id, DEBUG, SIMULATION)
    print(customer_info)
    if customer_info == None:
        print ("Customer with DMS ID %s not found! Adding them now..." % dms_id)
        new_customer = {
            "customer": {
                "customerKey": dms_id,
                "firstName": first_name,
                "lastName": last_name,
                "emails": [
                {
                    "emailAddress": email,
                    "label": "B",
                    "okToEmail": True,
                    "isPreferred": True
                }
                ],
                "phoneNumbers": [
                {
                    "phoneNumber": phone_num,
                    "label": "cell",
                    "okToCall": True,
                    "okToText": True,
                    "isPreferred": True
                }
                ],
            },
            "vehicles": [
                {
                "vin": vin,
                "isValid": True
                }
            ],
            "validateVin": True
            }
        customer_info = add_customer(creds,dept_uuid, new_customer, DEBUG, SIMULATION)
        return (customer_info["customer"],customer_info["vehicles"][0]["vehicleUuid"])
    else:
        # customer returned. Check for vehicle
        v = find_vehicle(customer_info["vehicles"], vin)
        if v == None:
            print("NOT DOING ANYTHING ... HERE BE DRAGONS!!")
        else:
            return(customer_info["customer"],v["vehicleUuid"])

        
def get_customer_and_vehicle(creds, dept_uuid, dms_id, vin, DEBUG = False, SIMULATION = False):
    """A STRICT method to get a given customer and their vehicle"""
    customer_info = get_customer_by_dms_id(creds, dept_uuid, dms_id, DEBUG, SIMULATION)
    if DEBUG:
        print(customer_info)
    if customer_info == None:
        return (None, None)
    else:
        # customer returned. Check for vehicle
        v = find_vehicle(customer_info["vehicles"], vin)
        if v == None:
            print("No Vehicle found for VIN %s !!" % vin)
            return (None, None)
        else:
            return(customer_info["customer"],v["vehicleUuid"])    

def get_customer_by_uuid(creds, department_uuid, customer_uuid, DEBUG = False, SIMULATION = False):
    """Gets the customer based on the provided UUID"""
    url = "%s/department/%s/customer/%s?excludeVehicles=false" % (creds[KEY_BASE_URL], department_uuid, customer_uuid)
    
    if SIMULATION:
        print("\n\n[SIM MODE] I would like to make a GET request to %s" % (url))
        return "SIMULATION MODE ON"
    else:
        r = requests.get(url,auth=(creds[KEY_USERNAME],creds[KEY_PASSWORD]))
        raw_response = r.json()
        if DEBUG:
            print(raw_response)
        #TODO check the "error" object
        return raw_response['customerWithVehicles']

if __name__ == "__main__":
    print('Sorry, no direct usage available. Import and then call the methods.')