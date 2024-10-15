#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys
import time

import MySQLdb

from config.common import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

logging.basicConfig(level=logging.INFO)


def mysql_is_ready(retries=5, delay=5):
    for attempt in range(retries):
        try:
            logging.info(f"Trying connect to MySQL ({attempt + 1}/{retries})...")
            db = MySQLdb.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASS,
                db=DB_NAME,
                port=int(DB_PORT),
            )
            db.close()
            logging.info("MySQL is ready 🔥")
            return
        except MySQLdb.OperationalError as e:
            logging.warning(f"Can not connect to MySQL: {e}. Try again in {delay} second...")
            time.sleep(delay)
    logging.error(f"Can not connect to MySQL after {retries} tries. Exit job.")
    sys.exit(-1)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    mysql_is_ready()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
