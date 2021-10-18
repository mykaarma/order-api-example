# .py
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

import sys #for exception handling

from optparse import OptionParser
from mkauth import username, password, customer_base_url, order_base_url
import kcustomercore, kordercore

customer_creds = {kcustomercore.KEY_USERNAME:username, kcustomercore.KEY_PASSWORD:password, kcustomercore.KEY_BASE_URL:customer_base_url}

order_creds = {kordercore.KEY_USERNAME:username, kordercore.KEY_PASSWORD:password, kordercore.KEY_BASE_URL:order_base_url}

import pprint


# Global, set to true by the parser if needed
DEBUG = False
SIMULATION = False

def prettyprint(message, width=280):
    '''pretty prints the text'''
    pprint.pprint(message,width = width)

def debug_print(message):
    '''Prints the message if the DEBUG flag is set'''
    if DEBUG:
        prettyprint(message)

def find_orders_with_customers(dept_uuid, filters):
    '''finds order with customers, based on the given filters'''
    try:
        orders = kordercore.get_orders(order_creds, dept_uuid, filters, DEBUG = DEBUG, SIMULATION = SIMULATION)
        debug_print(orders)
        for order in orders:
            #get the customer
            customer_uuid = order['customer']['uuid']
            customer_detail = kcustomercore.get_customer_by_uuid(customer_creds, dept_uuid, customer_uuid, DEBUG = DEBUG, SIMULATION = SIMULATION)
            order['customer']['detail'] = customer_detail
    except:
        debug_print("Got an exception %s during this request... skipping" % sys.exc_info()[0])
        debug_print("Details:")
        debug_print(sys.exc_info()[1])
        print(sys.exc_info()[1])
        orders = None
    return orders

def print_to_csv(orders, csv_file):
    '''prints the list of orders to a CSV'''
    # first, flatten each object
    from flatten_json import flatten
    dict_as_list = [flatten(o) for o in orders]
    debug_print(dict_as_list)

    # then, merge all keys into a master_keys list
    master_keys = dict()
    for d in dict_as_list:
        master_keys.update(d)
    column_names = [k for k in master_keys.keys()]
    debug_print(column_names)

    # write to CSV, set restval = '' for leaving fields blank when none exist
    import csv
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = column_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='')

        writer.writeheader()
        for d in dict_as_list:
            writer.writerow(d)
    # end of file writing
    debug_print("file %s written" % csv_file)

    
def main():
    global DEBUG #important, otherwise the global var DEBUG won't be set.
    global SIMULATION #important, otherwise the global var SIMULATION won't be set.
    
    usage = "usage: python3 %prog [-v|--verbose] [-s|--simulation] -p dept_uuid -d YYYY-MM-DD -t statuscode -f csvfile >> out.log"
    parser = OptionParser(usage)
    parser.add_option("-p", "--department", dest="dept_uuid",
                      help="the UUID of the department")
    parser.add_option("-d", "--date", dest="date",
                      help="the date of creation of the orders (YYYY-MM-DD)")
    parser.add_option("-t", "--statuscode", dest="statuscode",
                      help="the status code of the ROs that will extracted (O, P, or C)")
    parser.add_option("-f", "--csvfile", dest="csvfile",
                      help="the path of the CSV file where data will be dumped")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    parser.add_option("-s", "--simulation",
                      action="store_true", dest="simulation")
    (options, args) = parser.parse_args()
    DEBUG = options.verbose
    SIMULATION = options.simulation
    
    if options.dept_uuid == None:
        parser.error("missing dept_uuid")
    if options.date == None:
        parser.error("missing date (YYYY-MM-DD)")
    if options.statuscode == None:
        parser.error("missing statuscode")
    if options.csvfile == None:
        parser.error("missing csvfile")
    debug_print('# getting orders now')
    
    filters = {"orderStatus": options.statuscode, "orderType": "RO", "fromOrderDate":options.date, "toOrderDate": options.date}
    orders = find_orders_with_customers(options.dept_uuid,filters)
    debug_print(orders)
    print_to_csv(orders,options.csvfile)

if __name__ == "__main__":
    main()