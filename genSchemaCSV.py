# Name: genSchemaCSV.py
# Author: Rich Rose
# Description: Create a fake csv based on a JSON schema
# Lab: GSP291

from random import randint
from faker import Faker
import json
import sys
import argparse

fake = Faker()

# Name: getDatabaseSchema
# Description: Open the schema

def getDatabaseSchema(filename, schema_dict):
    with open(filename, 'r') as file:
        schema_dict = json.load(file)
    return schema_dict

# Name: getDataField
# Description: Create fake data

def getDataField(index):

    switcher={
        # Generate a fake string length 5 to 20 characters
        1: fake.pystr(min_chars=None, max_chars=randint(5,20)),
        # Generate a fake float length 5 with 2 decimal places
        2: fake.pyfloat(left_digits=5, right_digits=2, positive=False),
        # Generate a custom type - add your own definition :-)
        3: 'Custom TYPE'
    }

    return switcher.get(index, "Invalid index - update buildHeaderField")


# Name: setDataRow
# Description: Add some fake data based on the schema type

def setDataRow(schema_dict, csvRow):

    index = 0
    bound = len(schema_dict)-1
    customField = ""

    for schema in schema_dict:
        if index < bound:
            if schema['type'] == "STRING":
                customField = getDataField(1)
            elif schema['type'] == "FLOAT":
                customField = getDataField(2)

            csvRow = csvRow + str(customField) + ","
            index = index + 1
        else:
            if schema['type'] == "STRING":
                customField = getDataField(1)
            elif schema['type'] == "FLOAT":
                customField = getDataField(2)
                csvRow = csvRow + str(customField) + "\n"

    return csvRow


# Name: setHeaderRow
# Description: Use the schema to create a header row

def setHeaderRow(schema_dict, csvHeader):

    index = 0
    bound = len(schema_dict)-1

    for schema in schema_dict:
        if index < bound:

            csvHeader = csvHeader + schema['name'] + ","
            index = index + 1
        else:
            csvHeader = csvHeader + schema['name'] + "\n"

    return csvHeader


# Name: getCustomCSV
# Description: Take the schema and output psuedo csv data

def getCustomCSV(schema_dict, numRows):
    csvHeader   = ""
    csvRow      = ""
    index       = 0
    
    # Open file
    with open('test.csv', 'w') as csv_file:

        # Generate header for the file
        csvHeader = setHeaderRow(schema_dict, csvHeader)
        # print (csvHeader)
        csv_file.write(csvHeader)

        for index in range(int(numRows)):

            # Generate N rows for the file
            csvRow = setDataRow(schema_dict, csvRow)
            # print (csvRow)
            csv_file.write(csvRow)


# Name: getArguments
# Description: Process command line arguments

def getArguments():

    filename = ""
    numRows = 0

    # Consume schema
    parser=argparse.ArgumentParser(description='Schema command line executer')
    parser.add_argument('--schema', help='Add value1')
    parser.add_argument('--numRows',help='Add value2')

    args=parser.parse_args()

    # Ensure two arguments are supplied
    if (len(sys.argv) < 2):
        parser.print_help()
    else:
        # Map filename + numRow
        filename = args.schema
        numRows  = args.numRows

    # Return value
    return filename, int(numRows)


# Process the Dataschema and build a CSV
# Usage: app --schema file.json --numRows 10

if __name__ == '__main__':
    schema_dict = []
    filename    = ""
    numRows     = 0

    # Validate arguments
    filename, numRows=getArguments()

    # Only process information if data is required
    if numRows > 0:
      # Read in the JSON schema
      schema_dict = getDatabaseSchema(filename, schema_dict)

      # Build a CSV based on the schema
      getCustomCSV(schema_dict, numRows)
