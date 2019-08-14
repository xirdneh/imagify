"""
.. module: license.tests.models.test_subscription
    :synopsis: Subscription model tests.
"""

from __future__ import unicode_literals
import unittest
try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock
from license.models.subscription import Subscription
from license.exceptions.subscription import (
    SubscriptionWebsiteLimitReached,
    SubscriptionPlanNotValid
)
from license.exceptions.plan import (
    PlanUpgradeError,
    PlanDowngradeError
)


class TestSubscriptionModel(unittest.TestCase):
    """Test subscription model."""

    @patch('license.models.subscription.Plan')
    def setUp(self, plan_init_mock):
        """Set up fixtures."""
        user_mock = Mock()
        self.subscription = Subscription(
            plan=Mock(),
            user=user_mock
        )

    def test_add_website(self):
        """Test add a website."""
        self.subscription.plan.allowance.return_value = 1
        self.subscription.add_website('url')
        self.assertEqual(len(self.subscription.enabled_websites()), 1)
        self.assertEqual(self.subscription.enabled_websites()[-1].url, 'url')

    @patch(
        'license.models.subscription.Subscription.enabled_websites',
        return_value=[Mock()]
    )
    def test_add_website_error(self, enabled_websites_mock):
        """Test add website error."""
        self.subscription.plan.allowance.return_value = 1
        with self.assertRaises(SubscriptionWebsiteLimitReached):
            self.subscription.add_website('url')
            self.assertEqual(len(self.subscription.enabled_websites()), 1)

    def test_remove_website(self):
        """Test remove website."""
        websites = [Mock(url='url1', enabled=True),
                    Mock(url='url2', enabled=True),
                    Mock(url='url3', enabled=True)]
        self.subscription._websites = websites
        self.subscription.remove_website('url2')
        self.assertEqual(len(self.subscription.enabled_websites()), 2)
        self.assertEqual(self.subscription.enabled_websites()[0].url, 'url1')
        self.assertEqual(self.subscription.enabled_websites()[1].url, 'url3')
        self.subscription.remove_website()
        self.assertEqual(len(self.subscription.enabled_websites()), 1)
        self.assertEqual(self.subscription.enabled_websites()[0].url, 'url1')

    def test_disable_website(self):
        """Test disable website."""
        websites = [Mock(url='url1', enabled=True),
                    Mock(url='url2', enabled=True),
                    Mock(url='url3', enabled=True)]
        self.subscription._websites = websites
        self.subscription.disable_website('url1')
        enabled = self.subscription.enabled_websites()
        self.assertFalse([website for website in enabled
                          if website.url == 'url1'])

    def test_update_plan_upgrade(self):
        """Test update plan."""
        self.subscription.plan.downgrade.side_effect = PlanDowngradeError()
        self.subscription.update_plan('new_plan')
        self.assertTrue(self.subscription.plan.upgrade.called)
        self.assertFalse(self.subscription.plan.allowance.called)

    def test_update_plan_downgrade(self):
        """Test update plan."""
        websites = [Mock(url='url1', enabled=True),
                    Mock(url='url2', enabled=True),
                    Mock(url='url3', enabled=True)]
        self.subscription._websites = websites
        self.subscription.plan.upgrade.side_effect = PlanUpgradeError()
        self.subscription.plan.allowance.return_value = 1
        self.subscription.update_plan('new_plan')
        self.assertTrue(self.subscription.plan.downgrade.called)
        self.assertTrue(self.subscription.plan.allowance.called)
        self.assertEqual(len(self.subscription.enabled_websites()), 1)

    def test_update_plan_error(self):
        """Test update plan error."""
        self.subscription.plan.downgrade.side_effect = PlanDowngradeError()
        self.subscription.plan.upgrade.side_effect = PlanUpgradeError()
        with self.assertRaises(SubscriptionPlanNotValid):
            self.subscription.update_plan('new_plan')
