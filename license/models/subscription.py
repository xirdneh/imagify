"""
.. module: license.models.subscription
    :synopsis: Subscription model.
"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible
import logging
from license.models.plan import Plan
from license.models.website import Website
from license.exceptions.subscription import (
    SubscriptionWebsiteLimitReached,
    SubscriptionPlanNotValid
)
from license.exceptions.plan import (
    PlanUpgradeError,
    PlanDowngradeError
)


LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class Subscription(object):
    """Subscription model.

    This model will hold the plan type and the websites attached to a client
    """

    def __init__(self, plan, user):
        """Subscription class."""
        self.plan = Plan(plan)
        self.user = user
        self._websites = []

    def enabled_websites(self):
        """Return all enabled websites for this subscription."""
        return [
            website for website in self._websites if website.enabled
        ]

    def add_website(self, url):
        """Add website to subscription.

        :param str url: website's url.
        :return: self for chain-ability
        """
        enabled_websites = self.enabled_websites()
        count = len(enabled_websites)
        if self.plan.allowance() > 0 and count >= self.plan.allowance():
            LOG.exception(
                "Allowance for plan '{plan}' has been reached".format(
                    plan=self.plan
                )
            )
            raise SubscriptionWebsiteLimitReached(
                "Cannot add any more websites to plan '{plan}'".format(
                    plan=self.plan
                )
            )
        websites = [website for website in self._websites
                    if website.url == url]
        if websites:
            return self

        self._websites.append(Website(url, self.user))
        return self

    def remove_website(self, url=None):
        """Remove a website from subscription.

        If no url is given the last website added will be removed

        :param str url: Url of website to remove.
        """
        if not len(self._websites):
            return self

        if url:
            self._websites = [website for website in self._websites
                              if website.url != url]
        else:
            self._websites.pop()

        return self

    def disable_website(self, url):
        """Disable a specific website.

        :param str url: Url of website to disable.
        """
        websites = [website for website in self._websites
                    if website.url == url]
        if not websites:
            return self

        website = websites[0]
        website.enabled = False
        return self

    def update_plan(self, new_plan):
        """Update plan.

        This method will upgrade or downgrade the plan.

        :param str new_plan: New plan name.
        """
        upgraded = False
        downgraded = False
        try:
            self.plan.upgrade(new_plan)
            upgraded = True
        except PlanUpgradeError:
            pass
        try:
            self.plan.downgrade(new_plan)
            downgraded = True
        except PlanDowngradeError:
            pass
        if downgraded:
            enabled_websites = self.enabled_websites()
            if len(enabled_websites) > self.plan.allowance():
                for website in enabled_websites[self.plan.allowance():]:
                    website.enabled = False
            return self
        if upgraded:
            return self

        # If we couldn't upgrade or downgrade then we raise an error.
        LOG.exception(
            "Error modifying subscription '{subscription}' to '{plan}'".format(
                subscription=self,
                plan=new_plan
            )
        )
        raise SubscriptionPlanNotValid(
            "'{subscription}' cannot be updated to plan '{new_plan}'".format(
                subscription=self,
                new_plan=new_plan
            )
        )

    def __str__(self):
        """Str -> Plan: User."""
        return "{plan}: {user}".format(
            plan=self.plan,
            user=self.user
        )

    def __repr__(self):
        """Str -> Subscription(plan, user)."""
        return "Subscription({plan}, {user})".format(
            plan=self.plan,
            user=self.user
        )
