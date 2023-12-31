from db.run_sql import run_sql
from models.merchant import Merchant
import repositories.tag_repository as tag_repository

def save_merchant(merchant):
    sql = "INSERT INTO merchants(name,tags,colour,deactivated) VALUES (%s,%s,%s,%s) RETURNING id"
    values = [merchant.name,merchant.tag_ids,merchant.colour,merchant.deactivated]
    results = run_sql(sql,values)
    merchant.id = results[0]["id"]
    return merchant.id

def select_all():
    merchants = []
    sql = "SELECT * FROM merchants"
    results = run_sql(sql)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        merchant = Merchant(row["name"],tags,row["colour"],row["deactivated"],row["id"])
        merchants.append(merchant)
    return merchants

def select_active():
    merchants = []
    sql = "SELECT * FROM merchants WHERE deactivated = %s"
    values = [False]
    results = run_sql(sql, values)
    for row in results:
        tags = []
        for tag in row["tags"]:
            tags.append(tag_repository.select(tag))
        merchant = Merchant(row["name"],tags,row["colour"],row["deactivated"],row["id"])
        merchants.append(merchant)
    return merchants

def select(id):
    merchant = None
    sql = "SELECT * FROM merchants WHERE id = %s"
    values = [id]
    results = run_sql(sql, values)

    if results:
        result = results[0]
        tags = []
        for tag in result["tags"]:
            tags.append(tag_repository.select(tag))
        merchant = Merchant(result["name"],tags,result["colour"],result["deactivated"],result["id"])
    return merchant

def update(merchant):
    sql = "UPDATE merchants SET (name,tags,colour,deactivated) = (%s,%s,%s,%s) WHERE id = %s"
    values = [merchant.name, merchant.tag_ids,merchant.colour,merchant.deactivated, merchant.id]
    run_sql(sql, values)

def delete(id):
    sql = "DELETE FROM merchants WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def delete_all():
    sql = "DELETE FROM merchants"
    run_sql(sql)