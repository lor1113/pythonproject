from db.run_sql import run_sql
from models.transaction import Transaction
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

def save_transaction(transaction):
    sql = "INSERT INTO transactions(name,amount,tags,merchant,timestamp) VALUES (%s,%s,%s,%s,%s) RETURNING id"
    values = [transaction.name,transaction.amount,transaction.tags,transaction.merchant,transaction.timestamp]
    results = run_sql(sql,values)
    transaction.id = results[0]["id"]
    return transaction

def select_all():
    transactions = []
    sql = "SELECT * FROM transactions"
    results = run_sql(sql)
    for row in results:
        transaction = Transaction(row["name"],row["amount"],row["tags"],row["merchant"],row["timestamp"],row["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transaction.tags = [tag_repository.select(tag) for tag in transaction.tags]
        transactions.append(transaction)
    return transactions

def select(id):
    transaction = None
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    results = run_sql(sql, values)

    if results:
        result = results[0]
        transaction = Transaction(result["name"],result["amount"],result["tags"],result["merchant"],result["timestamp"],result["id"])
        transaction.merchant = merchant_repository.select(transaction.merchant)
        transaction.tags = [tag_repository.select(tag) for tag in transaction.tags]
    return transaction

def update(transaction):
    sql = "UPDATE transactions SET (name,amount,tags,merchant,timestamp) VALUES (%s,%s,%s,%s,%s) WHERE id = %s"
    values = [transaction.name,transaction.amount,transaction.tags,transaction.merchant,transaction.timestamp,transaction.id]
    run_sql(sql, values)

def delete(id):
    sql = "DELETE FROM transactions WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def delete_all():
    sql = "DELETE FROM transactions"
    run_sql(sql)