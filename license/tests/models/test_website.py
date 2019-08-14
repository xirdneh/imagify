"""
.. module: license.tests.models.test_website
    :synopsis: Website model tests.
"""

from __future__ import unicode_literals
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from license.models.website import Website


class TestWebsiteModel(unittest.TestCase):
    """Tests for website model."""

    def test__init(self):
        """Test website __init__."""
        customer_mock = Mock()
        website = Website('url', customer_mock)
        self.assertEqual(website.url, 'url')
        self.assertEqual(website.customer, customer_mock)

    def test__str(self):
        """Test customer __str__."""
        customer_mock = Mock()
        website = Website('url', customer_mock)
        self.assertEqual(str(website), 'url (True)')
