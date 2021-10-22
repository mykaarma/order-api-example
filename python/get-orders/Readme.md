# Get information about ROs of a given department
This program takes the following inputs: 
- the UUID of the department
- the date the ROs were opened
- the status code of the ROs we are looking for
- the CSV file name where the data will be dumped


# Dependencies
- python3
- optparse
- pprint
- requests
- csv
- flatten_json

# Scopes Needed
- `customer.search`, at the department level
- `order.standard.fetch`, at the department level 
- `order.specific.search`, at the department level

# Authentication
- save creds in mkauth.py (created by making a copy of mkauth.py.sample). Do NOT commit this file.

# How to run
```
python3 [-v|--verbose] [-s|--simulation] -p dept_uuid -d YYYY-MM-DD -t statuscode -f csvfile >> out.log
```

e.g. for all pre-invoiced (status 'P') ROs of dept abcd1234 opened on date 2021-10-14 to a file called data-2021-10-14.csv, use
```
 python get-orders.py -p abcd1234 -d 2021-10-14 -t P -f data-2021-10-14.csv  -v > out.log
```

# Python beginner tips
- use pip to install dependencies
```
example:
pip install requests flatten_json
```
