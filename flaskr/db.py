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
		g.db.row_facroty = sqlite3.Row

	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()