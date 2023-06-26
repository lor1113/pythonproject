from db.run_sql import run_sql
from models.tag import Tag

def save_tag(tag):
    sql = "INSERT INTO tags(name,colour,deactivated) VALUES (%s,%s,%s) RETURNING id"
    values = [tag.name,tag.colour,tag.deactivated]
    results = run_sql(sql,values)
    tag.id = results[0]["id"]
    return tag.id

def select_all():
    tags = []
    sql = "SELECT * FROM tags"
    results = run_sql(sql)
    for row in results:
        tag = Tag(row["name"],row["colour"],row["deactivated"],row["id"])
        tags.append(tag)
    return tags

def select(id):
    tag = None
    sql = "SELECT * FROM tags WHERE id = %s"
    values = [id]
    results = run_sql(sql, values)
    if results:
        result = results[0]
        tag = Tag(result["name"],result["colour"],result["deactivated"],result["id"])
    return tag

def update(tag):
    sql = "UPDATE tags SET (name,colour,deactivated) = (%s,%s,%s) WHERE id = %s"
    values = [tag.name,tag.colour,tag.deactivated, tag.id]
    run_sql(sql, values)

def delete(id):
    sql = "DELETE FROM tags WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def delete_all():
    sql = "DELETE FROM tags"
    run_sql(sql)