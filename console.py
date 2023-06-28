from models.transaction import Transaction
from models.tag import Tag
from models.merchant import Merchant

import repositories.transaction_repository as transaction_repository
import repositories.tag_repository as tag_repository
import repositories.merchant_repository as merchant_repository

import time
from datetime import datetime


transaction_repository.delete_all()
tag_repository.delete_all()
merchant_repository.delete_all()

tag1 = Tag("Food","Red")
tag_id1 = tag_repository.save_tag(tag1)
tag2 = Tag("Water","Blue")
tag_id2 = tag_repository.save_tag(tag2)
tag3 = Tag("Movies","Gold")
tag_id3 = tag_repository.save_tag(tag3)
tag4 = Tag("Stuff","Maroon")
tag_id4 = tag_repository.save_tag(tag4)

merchant1 = Merchant("Amazon",None,"Brown",tag_ids=[tag_id3])
merchant_id1 = merchant_repository.save_merchant(merchant1)
merchant2 = Merchant("Carrefour",None,"Blue",tag_ids=[tag_id1,tag_id2])
merchant_id2 = merchant_repository.save_merchant(merchant2)
merchant3 = Merchant("Fruttivendolo",None,"Green",tag_ids=[tag_id1])
merchant_id3 = merchant_repository.save_merchant(merchant3)

now = int(time.time())
time1 = now - 100
timestr1 = datetime.utcfromtimestamp(time1).strftime("%Y-%m-%d %H:%M:%S")
time2 = now - 1000000
timestr2 = datetime.utcfromtimestamp(time2).strftime("%Y-%m-%d %H:%M:%S")
time3 = now + 500
timestr3 = datetime.utcfromtimestamp(time3).strftime("%Y-%m-%d %H:%M:%S")


transaction1 = Transaction("Movies from Amazon",20,None,merchant1,timestr2,tag_ids=[tag_id3])
transaction_repository.save_transaction(transaction1)
transaction2 = Transaction("Stuff from Amazon",50,None,merchant1,timestr1,tag_ids=[tag_id2,tag_id4])
transaction_repository.save_transaction(transaction2)
transaction3 = Transaction("Grocery Shopping",10,None,merchant2,timestr3,tag_ids=[tag_id1])
transaction_repository.save_transaction(transaction3)
transaction4 = Transaction("Shopping",5000,None,merchant3,timestr1,tag_ids=[tag_id3])
transaction_repository.save_transaction(transaction4)
transaction5 = Transaction("Stuff",49,None,merchant2,timestr1,tag_ids=[tag_id4])
transaction_repository.save_transaction(transaction5)
transaction6 = Transaction("More stuff",75,None,merchant3,timestr2,tag_ids=[tag_id2])
transaction_repository.save_transaction(transaction6)
transaction7 = Transaction("I'm too tired to think of creative names",1024,None,merchant1,timestr3,tag_ids=[tag_id4])
transaction_repository.save_transaction(transaction7)
transaction8 = Transaction("Test transaction",500,None,merchant1,timestr3,tag_ids=[tag_id1])
transaction_repository.save_transaction(transaction8)
transaction9 = Transaction("Also a test",350,None,merchant3,timestr1,tag_ids=[tag_id1,tag_id2,tag_id3])
transaction_repository.save_transaction(transaction9)
transaction10 = Transaction("blah",20.5,None,merchant2,timestr2,tag_ids=[tag_id2])
transaction_repository.save_transaction(transaction10)


print(tag_repository.select_all())
print(merchant_repository.select_all())
print(transaction_repository.select_all())
