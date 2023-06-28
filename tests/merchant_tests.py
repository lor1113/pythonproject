import unittest

from models.tag import Tag
from models.merchant import Merchant

class TestMerchant(unittest.TestCase):
    def setUp(self):
        self.tag1 = Tag("Richmond","Yellow")
        self.merchant1 = Merchant("Origin Coffee",[self.tag1],"Orange")
        self.tag2 = Tag("London","Green",id=5)
        self.merchant2 = Merchant("Pleasant Lane Bakery",[self.tag2],"White")
    
    def test_merchant_has_name(self):
        self.assertEqual("Origin Coffee",self.merchant1.name)
    
    def test_merchant_has_tag(self):
        self.assertEqual(self.merchant1.tags[0],self.tag1)
    
    def test_merchant_has_color(self):
        self.assertEqual("Orange",self.merchant1.colour)
    
    def test_merchant_tag_ids(self):
        self.assertEqual([5],self.merchant2.tag_ids)