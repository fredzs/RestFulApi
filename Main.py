import logging
from logging.config import fileConfig
from flask import Flask


fileConfig('logging_config.ini')
logger = logging.getLogger()


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


if "__main__" == __name__:
    logger.info('-------------------------------------------'
                '程序开始执行-------------------------------------------')
    app.run(debug=True)
    logger.info('-------------------------------------------'
                '程序执行结束-------------------------------------------')
