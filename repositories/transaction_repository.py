from db.run_sql import run_sql
from models.transaction import Transaction
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

def save_transaction(transaction):
    sql = "INSERT INTO transactions(name,amount,tags,merchant,timestamp,deactivated) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id"
    values = [transaction.name,transaction.amount,transaction.tag_ids,transaction.merchant.id,transaction.timestamp,transaction.deactivated]
    results = run_sql(sql,values)
    transaction.id = results[0]["id"]
    return transaction

def select_active():
    transactions = []
    sql = "SELECT * FROM transactions WHERE deactivated = %s"
    values = [False]
    results = run_sql(sql, values)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        transaction = Transaction(row["name"],row["amount"],tags,row["merchant"],row["timestamp"],row["deactivated"],row["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transactions.append(transaction)
    return transactions


def select_all():
    transactions = []
    sql = "SELECT * FROM transactions"
    results = run_sql(sql)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        transaction = Transaction(row["name"],row["amount"],tags,row["merchant"],row["timestamp"],row["deactivated"],row["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transactions.append(transaction)
    return transactions

def select(id):
    transaction = None
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    results = run_sql(sql, values)

    if results:
        result = results[0]
        tags = []
        for tag in result["tags"]:
            tags.append(tag_repository.select(tag))
        transaction = Transaction(result["name"],result["amount"],tags,result["merchant"],result["timestamp"],result["deactivated"],result["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
    return transaction

def select_merchant(id):
    transactions = []
    sql = "SELECT * FROM transactions WHERE merchant = %s"
    values = [id]
    results = run_sql(sql, values)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        transaction = Transaction(row["name"],row["amount"],tags,row["merchant"],row["timestamp"],row["deactivated"],row["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transactions.append(transaction)
    return transactions

def select_tag(id):
    transactions = []
    sql = "SELECT * FROM transactions WHERE %s = ANY(tags)"
    values = [id]
    results = run_sql(sql, values)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        transaction = Transaction(row["name"],row["amount"],tags,row["merchant"],row["timestamp"],row["deactivated"],row["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transactions.append(transaction)
    return transactions

def update(transaction):
    sql = "UPDATE transactions SET (name,amount,tags,merchant,timestamp,deactivated) = (%s,%s,%s,%s,%s,%s) WHERE id = %s"
    values = [transaction.name,transaction.amount,transaction.tag_ids,transaction.merchant.id,transaction.timestamp,transaction.deactivated,transaction.id]
    run_sql(sql, values)

def delete(id):
    sql = "DELETE FROM transactions WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def delete_all():
    sql = "DELETE FROM transactions"
    run_sql(sql)