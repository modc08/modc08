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
        self.wb = open_workbook(file_contents=input.read())

        self.prefix = prefix

    def json_from_sheets(self):
        data = []

        for sheet in self.wb.sheets():
            dict = {}

            """ Assume we should skip the first row as it contains column
            headers, and that element names are in column 1 and values in
            column 3. """
            for row in range(1, sheet.nrows):
                dict[str(sheet.cell_value(row, 0))] = str(sheet.cell_value(row, 2))

            """ Assume each sheet has an element name 'id' which corresponds to
            pk of model """
            pk = dict.pop('id')

            """ Each workbook may have multiple sheets of same category named
            Source1, Source2, ... Source11 etc. Strip any number of decimal
            digits from end of sheet name to get just the category name. """
            category = re.sub('\d*$', '', sheet.name)
            model = self.prefix + '.' + category.lower()

            data.append({'fields': dict, 'pk': pk, 'model': model})

        jsondata = json.dumps(data, indent=2)
        return jsondata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infilename', help='Excel source file')
    args = parser.parse_args()

    with open(args.infilename, 'rb') as infile:
        excel = ReadFromExcel(infile)
        print excel.json_from_sheets()
