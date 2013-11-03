from unittest import TestCase
from Ruler import Ruler

__author__ = 'Vince'


class TestRuler(TestCase):
    def test_get_rule_subset_by_phase_field_parent(self):
        self.assertEqual(len(Ruler().get_rule_subset_by_phase_field_parent('Category 1', 1, 'Financial Market Professionals')), 242)

    def test_get_classes(self):
        self.assertEqual(len(Ruler().get_classes('Category 1', 'Financial Market Professionals')), 8)