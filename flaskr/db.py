import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    '''
    g 特殊对象，独立于每一个请求。在处理请求的过程中，它可以用于存储可能多个函数都会
    用到的数据。将数据连接存于其中可避免多次重新建立。（看解释类似单例）
    '''
    if 'db' not in g:
        # 根据指定的配置建立一个数据库连接
        g.db = sqlite3.connect(
            # 特殊对象，指当前处理请求的 Flask 应用。
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # 该方法会将表以字典的形式返回，具体还有带进一步验证
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # 该命令会打开一个相对于应用包位置的文件
    with current_app.open_resource('schema.sql') as file:
        content = file.read().decode('utf8')
        db.executescript(content)


# 将该函数添加为 flask 命令
# $ falsk init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    重置并初始化数据库，创建相应表
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # 告诉 Flask 在返回响应后进行清理时调用该函数
    # 向 flask 添加一个命令
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
