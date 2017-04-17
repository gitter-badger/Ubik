import re


def parse_database(dburl):
    m = re.search('postgres://([\w]*):([\w]*)@([^\s]*):([0-9]*)/([\w]*)', dburl)
    return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)

