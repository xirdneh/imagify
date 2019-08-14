"""
.. module: license.tests.models.test_plan
    :synopsis: Plan model tests.
"""

from __future__ import unicode_literals
import unittest
from license.models.plan import Plan
from license.exceptions.plan import (
    PlanTypeError,
    PlanUpgradeError,
    PlanDowngradeError,
)


class TestPlanModel(unittest.TestCase):
    """Test Plan Model."""

    def test__init(self):
        """Test __init__."""
        for plan_type in Plan.PLANS:
            plan = Plan(plan_type)
            self.assertEqual(plan.plan_type, plan_type)
            self.assertEqual(plan.allowance(), Plan.ALLOWANCE[plan_type])
            self.assertEqual(plan.price(), Plan.PRICES[plan_type])

    def test_invalid_plan_type(self):
        """Test invalid plan type."""
        with self.assertRaises(PlanTypeError):
            Plan('not valid')

    def test_upgrade(self):
        """Test plan upgrade."""
        plan = Plan(Plan.PLANS[0])
        for plan_type in Plan.PLANS[1:]:
            plan.upgrade(plan_type)
            self.assertEqual(plan.plan_type, plan_type)

    def test_downgrade(self):
        """Test plan downgrade."""
        plans = Plan.PLANS[:]
        plans.reverse()
        plan = Plan(plans[0])
        for plan_type in plans[1:]:
            plan.downgrade(plan_type)
            self.assertEqual(plan.plan_type, plan_type)

    def test_upgrade_error(self):
        """Test upgrade error."""
        plan = Plan(Plan.PLANS[-1])
        for plan_type in Plan.PLANS[:-1]:
            with self.assertRaises(PlanUpgradeError):
                plan.upgrade(plan_type)
                self.assertEqual(plan.plan_type, Plan.PLANS[-1])

    def test_downgrade_error(self):
        """Test downgrade error."""
        plan = Plan(Plan.PLANS[0])
        for plan_type in Plan.PLANS[1:]:
            with self.assertRaises(PlanDowngradeError):
                plan.downgrade(plan_type)
                self.assertEqual(plan.plan_type, Plan.PLANS[0])

    def test_upgrade_invalid_error(self):
        """Test upgrade to an invalid plan."""
        plan = Plan(Plan.PLANS[0])
        with self.assertRaises(PlanUpgradeError):
            plan.upgrade('not valid')

    def test_downgrade_invalid_error(self):
        """Test downgrade to an invalid plan."""
        plan = Plan(Plan.PLANS[-1])
        with self.assertRaises(PlanDowngradeError):
            plan.downgrade('not valid')
