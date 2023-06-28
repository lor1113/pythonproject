import unittest

from models.tag import Tag

class TestTag(unittest.TestCase):
    def setUp(self):
        self.tag1 = Tag("Richmond","Yellow")
    
    def test_tag_has_name(self):
        self.assertEqual("Richmond",self.tag1.name)
    
    def test_tag_has_colour(self):
        self.assertEqual("Yellow",self.tag1.colour)