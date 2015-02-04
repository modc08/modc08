from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
@stringfilter
def linkify_pubid(value):
    """ Catch http[s]:// urls and return hyperlinked form without doing anything
    else """
    if re.match('http[s]?:\/\/', value):
        return '<a href="%s">%s</a>' % (value, value)

    split = re.split(':', value, maxsplit=1)

    prefixes = {
        'doi': 'http://dx.doi.org/',
        'hdl': 'http://hdl.handle.net/',
        'pmid': 'http://www.ncbi.nlm.nih.gov/pubmed/'
    }
    try:
        prefix = prefixes[split[0]]
    except KeyError:
        """ If we didn't find a known pubid prefix, just return whatever value was passed """
        return value

    url = prefix + split[1]
    return '<a href="%s">%s</a>' % (url, url)
