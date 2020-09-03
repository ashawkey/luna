import os
import glob
import time
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flaskext.mysql import MySQL

SCHEMA = [
    '''
    DROP TABLE if exists nonsense;
    ''',
    '''
    CREATE TABLE nonsense (
        nid INT NOT NULL AUTO_INCREMENT,
        ctime BIGINT NOT NULL,
        mtime BIGINT NOT NULL,
        body TEXT NOT NULL,
        deleted INT NOT NULL DEFAULT 0,
        token VARCHAR(100) NOT NULL,
        PRIMARY KEY (nid),
        FULLTEXT (body) WITH PARSER ngram
    ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4;
    ''',
]

mysql = MySQL()

stmt_size = "select count(*) from nonsense"
stmt_meta = "select nid, ctime, mtime, body from nonsense where (deleted = 0) and (token = (%s)) order by mtime desc"
stmt_get = "select ctime, mtime, body from nonsense where nid = (%s)"
stmt_post = "insert into nonsense(ctime, mtime, body, token) values(%s, %s, %s, %s)"
stmt_update = "update nonsense set mtime = (%s), body = (%s) where nid = (%s)"
#stmt_post_or_update = "insert into nonsense(nid, ctime, mtime, body) values(%s, %s, %s, %s) on duplicate key update mtime = values(mtime), body = values(body)"
#stmt_delete = "delete from nonsense where nid = (%s)"
stmt_delete = "update nonsense set deleted = 1 where nid = (%s)"
stmt_search = "select nid, ctime, mtime, body from nonsense where (deleted = 0) and (match (body) against (%s in boolean mode)) and (token = (%s)) order by mtime desc"

def init_db():
    db = mysql.get_db()
    cur = db.cursor()
    for stmt in SCHEMA:
        cur.execute(stmt)
    db.commit()
    db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    mysql.init_app(app)
    app.cli.add_command(init_db_command)
