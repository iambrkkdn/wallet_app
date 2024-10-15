import os

DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_PORT = os.getenv('MYSQL_PORT', '3306')
DB_USER = os.getenv('MYSQL_USER', 'user')
DB_PASS = os.getenv('MYSQL_PASSWORD', 'password')
DB_NAME = os.getenv('MYSQL_DATABASE', 'wallet')
DB_ROOT_USER = os.getenv('MYSQL_ROOT_USER', 'root')
DB_ROOT_PASS = os.getenv('MYSQL_ROOT_PASSWORD', 'supersecretpassword')

TEST_DB_NAME = os.getenv('TEST_MYSQL_DATABASE', 'test_wallet')
