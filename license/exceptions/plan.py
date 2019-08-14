"""
.. module: license.models.plan
    :synopsis: Plan model..
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible


@python_2_unicode_compatible
class PlanTypeError(Exception):
    """Plan type error.

    Used when the type of subscription does not exists.
    """

    pass


@python_2_unicode_compatible
class PlanUpgradeError(Exception):
    """Plan type error.

    Used when the current subscription type cannot be upgraded to the given
    subscription type.
    """

    pass


@python_2_unicode_compatible
class PlanDowngradeError(Exception):
    """Plan type error.

    Used when the current subscription type cannot be upgraded to the given
    subscription type.
    """

    pass
