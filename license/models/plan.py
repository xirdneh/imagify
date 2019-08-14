"""
.. module: license.models.plan
    :synopsis: Plan model..
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible
import logging
from license.exceptions.plan import (
    PlanTypeError,
    PlanUpgradeError,
    PlanDowngradeError
)


LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class Plan(object):
    """Plan model.

    There are three types of subscriptions: Single, Plus and Infinite.
    The 'Single' plan has an allowance of 1.
    The 'Plus' plan has an allowance of 3.
    The 'Infinite' plan has an infinite allowance represented by a -1.
    """

    SINGLE = 'Single'
    PLUS = 'Plus'
    INFINITE = 'Infinite'
    PLANS = [SINGLE, PLUS, INFINITE]
    ALLOWANCE = {
        SINGLE: 1,
        PLUS: 3,
        INFINITE: -1,
    }
    PRICES = {
        SINGLE: 49.00,
        PLUS: 99.00,
        INFINITE: 249.00,
    }

    def __init__(self, plan_type, websites=None):
        """Plan model.

        :param str subscription_type: one of 'Single', 'Plus' or 'Infinite'.
        :param str webstie: Websites attached to the subscription.
        """
        if plan_type not in self.PLANS:
            raise PlanTypeError(
                "Plan type '{plan_type}' does not exists.".format(
                    plan_type=plan_type
                )
            )
        self.plan_type = plan_type

    def allowance(self):
        """Return a plan's allowance."""
        return self.ALLOWANCE.get(self.plan_type, -1)

    def price(self):
        """Return a plan's price."""
        return self.PRICES[self.plan_type]

    def upgrade(self, new_plan):
        """Upgrade plan.

        :param str new_plan: One of :attr:`PLANS`
        :return: self for chain-ability
        :raise: :class:`PlanUpgradeError` if there's an error while upgrading.
        """
        current_plan_weight = self.PLANS.index(self.plan_type)
        try:
            new_plan_weight = self.PLANS.index(new_plan)
        except ValueError:
            LOG.exception(
                "Error upgrading plan from '{plan}' to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
            raise PlanUpgradeError(
                "'{plan}' cannot be upgraded to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
        if current_plan_weight > new_plan_weight:
            LOG.exception(
                "Error upgrading plan from '{plan}' to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
            raise PlanUpgradeError(
                "'{plan}' cannot be upgraded to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
        self.plan_type = new_plan
        return self

    def downgrade(self, new_plan):
        """Downgrade plan.

        :param str new_plan: One of :attr:`PLANS`
        :return: self for chain-ability
        :raise: :class:`PlanDowngradeError` if there's an error while
            upgrading.
        """
        current_plan_weight = self.PLANS.index(self.plan_type)
        try:
            new_plan_weight = self.PLANS.index(new_plan)
        except ValueError:
            LOG.exception(
                "Error downgrading plan from '{plan}' to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
            raise PlanDowngradeError(
                "'{plan}' cannot be downgraded to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
        if current_plan_weight < new_plan_weight:
            LOG.exception(
                "Error downgrading plan from '{plan}' to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
            raise PlanDowngradeError(
                "'{plan}' cannot be downgraded to '{new_plan}'".format(
                    plan=self.plan_type,
                    new_plan=new_plan
                )
            )
        self.plan_type = new_plan
        return self

    def __str__(self):
        """Str -> Plan Type (Price): Allowance."""
        return "{plan_type} ({price}): {allowance}".format(
            plan_type=self.plan_type,
            price=self.price(),
            allowance=self.allowance()
        )

    def __repr__(self):
        """Repr -> Plan(plan_type)."""
        return "Plan({plan_type})""".format(
            plan_type=self.plan_type
        )
