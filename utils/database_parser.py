import re


def parse_database(dburl):
    """
    Parses the database.

    :param dburl: The url of the Postgres database.
    :return: Tuple (user_name, user_password, db_host, db_port, db_name)
    """
    m = re.search('postgres://([\w]*):([\w]*)@([^\s]*):([0-9]*)/([\w]*)', dburl)
    return m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)

