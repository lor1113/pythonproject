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
tag_repository.save_tag(tag1)
merchant1 = Merchant("Amazon",[1,2,3,45,666],"Green")
merchant_repository.save_merchant(merchant1)
now = datetime.utcnow()
transaction1 = Transaction("Food from Amazon",20,[1,2,3],5,now.strftime("%Y-%m-%d %H:%M:%S"))
transaction_repository.save_transaction(transaction1)

print(transaction_repository.select_all())
print(tag_repository.select_all())
print(merchant_repository.select_all())
