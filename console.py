from models.transaction import Transaction
from models.tag import Tag
from models.merchant import Merchant

import repositories.transaction_repository as transaction_repository
import repositories.tag_repository as tag_repository
import repositories.merchant_repository as merchant_repository

from datetime import datetime

transaction_repository.delete_all()
tag_repository.delete_all()
merchant_repository.delete_all()

print(transaction_repository.select_all())
print(tag_repository.select_all())
print(merchant_repository.select_all())

tag1 = Tag("food","Red")
tag_id = tag_repository.save_tag(tag1)
merchant1 = Merchant("Amazon",None,"Green",tag_ids=[tag_id])
merchant_id = merchant_repository.save_merchant(merchant1)
now = datetime.utcnow()
transaction1 = Transaction("Food from Amazon",20,None,merchant1,now.strftime("%Y-%m-%d %H:%M:%S"),tag_ids=[tag_id])
transaction_repository.save_transaction(transaction1)


print(transaction_repository.select_all())
print(transaction_repository.select_active())
print(transaction_repository.select_tag(9))
