#coding:utf-8
import logging

logger = logging.getLogger('marserv')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='marserv.log',
    filemode='a'
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
