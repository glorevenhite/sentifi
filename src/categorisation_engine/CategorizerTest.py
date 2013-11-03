from unittest import TestCase
from Categorizer import Categorizer

__author__ = 'Vince'


class TestCategorizer(TestCase):
    def test__get_classes(self):
        categorizer = Categorizer()
        self.assertEquals(categorizer._get_classes('Publisher Group', 'P'), ['Other Stakeholders', 'Financial Market Professionals'])
        self.assertEquals(len(categorizer._get_classes('Publisher Group', 'O')), 8)

    def test_categorize_twitter_profile_step(self):
        self.fail()