import os, argparse
from xlrd import open_workbook
import re
import json


class ReadFromExcel(object):
    """
    Read data from Excel source and return a JSON representation suitable for
    passing to Django's serializers.deserialize()
    """
    def __init__(self, input, prefix='acad'):
        """ Create an xlrd Book object with the contents of our Excel input """
        self.wb = open_workbook(file_contents=input)
        self.prefix = prefix

    def json_from_sheets(self):
        data = []

        for sheet in self.wb.sheets():
            model = self.prefix + '.' + sheet.name.lower()

            """ Assume Excel input follows this format:
            field1 | field2 | field3
            -------|--------|-------
            value  | value  | value
            value  | value  | value
            """
            for row in range(1, sheet.nrows):

                dict = {}

                for column in range(0, sheet.ncols):
                    dict[str(sheet.cell_value(0, column))] = str(sheet.cell_value(row, column))

                """ Assume each sheet has an field name 'id' which corresponds
                to pk of model """
                pk = dict.pop('id')

                data.append({'fields': dict, 'pk': pk, 'model': model})

        jsondata = json.dumps(data, indent=2)
        return jsondata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infilename', help='Excel source file')
    args = parser.parse_args()

    with open(args.infilename, 'rb') as infile:
        excel = ReadFromExcel(infile.read())
        print excel.json_from_sheets()
