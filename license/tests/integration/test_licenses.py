"""
.. module: license.tests.integration.test_licenses
    :synopsis: Integration licenses tests..
"""

from __future__ import unicode_literals
import unittest
from datetime import datetime, timedelta
from license.models.customer import Customer
from license.models.plan import Plan
from license.exceptions.subscription import (
    SubscriptionExistent,
    SubscriptionPlanNotValid,
)
from license.exceptions.plan import (
    PlanTypeError,
)


class TestLicenses(unittest.TestCase):
    """Tests licenses."""

    def setUp(self):
        """Set up test customer."""
        self.customer = Customer('name', 'email', 'password')
        self.customer.subscribe(Plan.SINGLE)

    def test_subscribe(self):
        """Test subcribe."""
        self.customer.subscription = None
        self.customer.subscribe(Plan.SINGLE)
        self.assertEqual(
            self.customer.subscription.plan.plan_type,
            Plan.SINGLE
        )

    def test_subscribe_error(self):
        """Test subscribe error."""
        with self.assertRaises(SubscriptionExistent):
            self.customer.subscribe(Plan.SINGLE)

    def test_subscribe_invalid_type(self):
        """Test subscribe with invalid type."""
        self.customer.subscription = None
        with self.assertRaises(PlanTypeError):
            self.customer.subscribe('not valid')

    def test_add_website(self):
        """Test add a website."""
        self.customer.subscription.add_website('url1')
        self.assertEqual(
            len(self.customer.subscription.enabled_websites()),
            1
        )
        self.assertEqual(
            self.customer.subscription.enabled_websites()[0].url,
            'url1'
        )

    def test_disable_website(self):
        """Test disable website."""
        self.customer.subscription.add_website('url1')
        self.customer.subscription.disable_website('url1')
        self.assertEqual(
            len(self.customer.subscription.enabled_websites()),
            0
        )

    def test_update_plan(self):
        """Test upgrade/downgrade plan."""
        self.customer.subscription.update_plan(Plan.INFINITE)
        self.assertEqual(
            self.customer.subscription.plan.plan_type,
            Plan.INFINITE
        )
        self.customer.subscription.add_website('url2')
        self.customer.subscription.add_website('url3')
        self.customer.subscription.add_website('url4')
        self.customer.subscription.update_plan(Plan.PLUS)
        self.assertEqual(
            self.customer.subscription.plan.plan_type,
            Plan.PLUS
        )
        self.assertEqual(
            len(self.customer.subscription.enabled_websites()),
            Plan.ALLOWANCE[Plan.PLUS]
        )
