"""
.. module: license.tests.models.test_customer
    :synopsis: Customer model tests.
"""

from __future__ import unicode_literals
import unittest
from license.models.customer import Customer


class TestCustomerModel(unittest.TestCase):
    """Tests for customer model."""

    def test__init(self):
        """Test customer __init__."""
        customer = Customer(
            'name',
            'email@email.com',
            'password'
        )
        self.assertEqual(customer.name, 'name')
        self.assertEqual(customer.email, 'email@email.com')
        self.assertEqual(customer.password, 'password')
        self.assertIsNone(customer.subscription)
        self.assertIsNone(customer.subscription_renewal)

    def test__str(self):
        """Test customer __str__."""
        customer = Customer(
            'name',
            'email@email.com',
            'password'
        )
        self.assertEqual(str(customer), "name <email@email.com>")
