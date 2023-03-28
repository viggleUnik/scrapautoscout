import unittest

from scrapautoscout.scrapper import calculate_nr_of_pages


class test_calculate_nr_of_pages(unittest.TestCase):

    def test_various_inputs(self):
        self.assertEqual(1, calculate_nr_of_pages(1))
        self.assertEqual(1, calculate_nr_of_pages(10))
        self.assertEqual(6, calculate_nr_of_pages(101))
        self.assertEqual(20, calculate_nr_of_pages(400))
        self.assertEqual(20, calculate_nr_of_pages(401))
        self.assertEqual(20, calculate_nr_of_pages(99999))
