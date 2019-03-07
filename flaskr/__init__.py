import os

from flask import Flask


def create_app(test_config=None):
    # 创建Flask实例
    app = Flask(__name__, instance_relative_config=True)
    # 对其进行配置，这里配置了密钥和数据库地址
    app.config.from_mapping(
        SECRET_KEY='dev',  # 注意发布时无比要将此替换为一个随机值
        DATABASE=os.path.join(app.instance_path, ''),
    )

    if test_config is None:
        # 如果创建没有指定配置，那么就从文件中重载缺省配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)  # 确保创建该文件夹
    except OSError:
        pass

    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    return app
