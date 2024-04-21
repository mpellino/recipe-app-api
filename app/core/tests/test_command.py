"""
Test custom Django management command
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test command"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error"""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
        [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])



"""
unittest.mock.patch: 
This is a function from the unittest.mock module in Python's standard library. 
It's used for mocking - replacing parts of your system under test and making assertions 
about how they have been used. patch is used as a decorator, context manager, or in a 
with statement to mock out objects within the scope of a block of code.

psycopg2.OperationalError: 
This is an exception class from the psycopg2 module, which is a PostgreSQL database 
adapter for Python. OperationalError is raised when an error of a database operation,
 a connection problem, or similar, occurs.

django.core.management.call_command: 
This is a function from Django's django.core.management module. 
It's used to call management commands programmatically, i.e., from your code,
 as opposed to from the command line.

django.db.utils.OperationalError: 
This is an exception class from Django's django.db.utils module. 
Similar to psycopg2.OperationalError, Django's OperationalError is raised when a 
database-related error occurs, but it's database-agnostic, 
meaning it can be used with any database, not just PostgreSQL.

django.test.SimpleTestCase: 
This is a class from Django's django.test module. It's used as a base class for simpler 
test cases that don't involve a database. For tests involving a database, 
Django provides other base classes like TestCase and TransactionTestCase.

"""
