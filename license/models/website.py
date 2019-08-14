"""
.. module: license.models.subscription
    :synopsis: Subscription model..
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible
import logging


LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class Website(object):
    """Website model."""

    def __init__(self, url, customer, enabled=True):
        """Initialize website obj.

        :param str url: Website url.
        :param bool enabled: Weather or not the website will be enabled.
            `True` by default.
        :param customer: Customer who registered a site.
        """
        self.url = url
        self.enabled = enabled
        self.customer = customer

    def __str__(self):
        """Str -> self.url (self.enabled)."""
        return "{url} ({enabled})".format(url=self.url, enabled=self.enabled)

    def __repr__(self):
        """Repr -> Website(url, customer, enabled)."""
        return "Website({url}, {customer}, {enabled})""".format(
            url=self.url,
            customer=self.customer,
            enabled=self.enabled
        )
