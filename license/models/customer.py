"""
.. module: license.models.customer
    :synopsis: Customer model.
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible
import logging
from datetime import datetime, timedelta
from license.models.subscription import Subscription
from license.exceptions.subscription import SubscriptionExistent


LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class Customer(object):
    """Client model."""

    def __init__(self, name, email, password, plan=None):
        """Client class to hold subscription types.

        :param str name: client's name.
        :param str email: client's email.
        :param str password: client's password.
        :param str plan: Plan type, one of:
            ['Single', 'Plus', 'Infinite'].
        """
        self.name = name
        self.email = email
        self.password = password
        self.subscription = None
        self.subscription_renewal = None
        if plan:
            self.subscribe(plan)

    def subscribe(self, plan):
        """Subscribe client to a plan.

        :param str plan_type: Plan type
        :return: self for chain-ability.
        """
        if self.subscription is not None:
            raise SubscriptionExistent("Customer already has a subscription.")

        self.subscription = Subscription(plan, self)
        self.subscription_renewal = datetime.utcnow() + timedelta(days=365)
        return self

    def __str__(self):
        """Str -> name <email>."""
        return "{name} <{email}>".format(name=self.name, email=self.email)

    def __repr__(self):
        """Repr => Customer(name, email, plan_type)."""
        return "Customer({name}, {email}, {plan_type})".format(
            name=self.name,
            email=self.email,
            plan_type=self.plan_type
        )
