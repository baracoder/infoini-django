# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from cafe_server import ArduinoParser

class TestParser(TestCase):
    def setUp(self):
        self.parser = ArduinoParser()
    
    def test_parser_empty(self):
        """Leere Zeile"""
        self.assertFalse(self.parser.parse(""), "Leere Zeile")
        
    def test_parser_normal(self):
        """Normale Zeile"""
        self.assertTrue(self.parser.parse(
                "ACK pots:[809,234],[2345,345] tueroffen:1 stat:200"),
                 "Normale Zeile")
        
        self.assertEqual(self.parser.getTueroffen(), True, "tueroffen")
        self.assertEqual(self.parser.getStatus(), 200, "status")
        
        [pot1, pot2] = self.parser.getCoffepots()
        self.assertEqual(pot1['level'], 809, "level")
        self.assertEqual(pot2['level'], 2345, "level")
        self.assertEqual(pot1['sd'], 234, "sd")
        self.assertEqual(pot2['sd'], 345, "sd")
        
    def test_parser_partional(self):
        """Abgeschnittene Zeile"""
