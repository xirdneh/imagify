"""
.. module: license.models.plan
    :synopsis: Plan model..
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class SubscriptionWebsiteLimitReached(Exception):
    """Website limit reached.

    Used when the limit of websites has been reached for a specific
    subscription.
    """

    pass

@python_2_unicode_compatible
class SubscriptionPlanNotValid(Exception):
    """Subscription plan not vali.

    Used when a subscription is modified to a plan that is not valid.
    """

    pass

@python_2_unicode_compatible
class SubscriptionExistent(Exception):
    """Subscription existent.

    Used when a client is trying to subscribe with an existent subscription.
    """

    pass
