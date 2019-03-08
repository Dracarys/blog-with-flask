# setup.py 文件用于描述项目及其丛书的文件

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0'
    # 指明 Python 包所包含的文件，这里通过函数自动查找，免除手动的麻烦
    packages=find_packages(),
    # 静态文件、模板文件不会被上面的函数自动包含进去，需要显示设置为 true
    # 需要配合 MANIFEST.in 文件配合，列明要包含的内容
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
