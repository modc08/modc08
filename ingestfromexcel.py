import os, argparse
from xlrd import open_workbook
import re

''' This is just a dummy function for testing purposes '''
def Source(**kwargs):
    for key, value in kwargs.iteritems():
        print '%s = %s' % (key, value)

def nomatch(**kwargs):
    print 'No match for sheet name'

switch = {
    # To create a Django object would use Source.objects.create
    'Source': Source,
}

class IngestFromExcel(object):
    def __init__(self, input):
        ''' Create an xlrd Book object with the contents of our Excel input '''
        self.wb = open_workbook(file_contents=input.read())

    def get_sheetnames(self):
        for sheet in self.wb.sheets():
            print sheet.name

    def create_from_sheets(self):
        for sheet in self.wb.sheets():
            ''' This dictionary will hold the element names and values read
            from the sheet '''
            dict = {}

            ''' Skip first row as this has column headers. Assume element name
            in column 1, value in column 3. '''
            for row in range(1, sheet.nrows):
                dict[str(sheet.cell_value(row,0))] = str(sheet.cell_value(row,2))

            ''' Each workbook may have multiple sheets of same category named
            Source1, Source2, ... Source11 etc. Strip any number of decimal
            digits from end of sheet name to get just the category name.
            '''
            category = re.sub('\d*$', '', sheet.name)

            ''' Look up our category name and pass dictionary as kwargs '''
            switch.get(category, nomatch)(**dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infilename', help='Excel source file')
    args = parser.parse_args()

    infile = open(args.infilename, 'rb')
    excel = IngestFromExcel(infile)
    excel.create_from_sheets()
