import unittest
from datetime import datetime

from models.tag import Tag
from models.merchant import Merchant
from models.transaction import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%dT%H:%M")
        self.tag1 = Tag("London","Green",id=6)
        self.merchant1 = Merchant("Pleasant Lane Bakery",[self.tag1],"White")
        self.transaction1 = Transaction("Cupcake",5,[self.tag1],self.merchant1,date_string)
    
    def test_transaction_has_name(self):
        self.assertEqual("Cupcake",self.transaction1.name)
    
    def test_transaction_has_amount(self):
        self.assertEqual(5,self.transaction1.amount)

    def test_transaction_has_tag(self):
        self.assertEqual(self.tag1,self.transaction1.tags[0])
    
    def test_transaction_tag_ids(self):
        self.assertEqual(6,self.transaction1.tag_ids[0])
    
