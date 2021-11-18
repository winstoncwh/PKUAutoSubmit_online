# -*- coding: utf-8
# hi
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser
from func import *
from time import strftime, localtime
import warnings
import sys

warnings.filterwarnings('ignore')


def sys_path(browser):
    path = f'./{browser}/bin/'
    if sys.platform.startswith('win'):
        return path + f'{browser}.exe'
    elif sys.platform.startswith('linux'):
        return path + f'{browser}'
    elif sys.platform.startswith('darwin'):
        return path + f'{browser}'
    else:
        raise Exception('暂不支持该系统')


def go(config, num):
    conf = ConfigParser()
    conf.read(config, encoding='utf8')
    now_time = str(strftime("%Y-%m-%d", localtime()))

    campus, reason, detail = dict(conf['common']).values()
    destination, track = dict(conf['out']).values()
    habitation, district, street = dict(conf['in']).values()
    capture = conf.getboolean('capture', '是否需要备案历史截图')
    path = conf['capture']['截图保存路径']
    wechat = conf.getboolean('wechat', '是否需要微信通知')
    time = conf['time']['time']

    if time == now_time:
        print("今天已經報備過了!")
    else:
        run(driver_pjs, argconf.ID[num - 1], argconf.PASSWORD[num - 1], campus, argconf.MAIL_ADDRESS[num - 1],
            argconf.PHONE_NUMBER[num - 1], reason, detail, destination, track, habitation, district, street, capture,
            path, wechat, argconf.SENDKEY[num - 1])
        conf.set("time", "time", now_time)
        conf.write(open("config" + str(num) + ".ini", "w"))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--ID', nargs="+", type=str)
    parser.add_argument('--PASSWORD', nargs="+", type=str)
    parser.add_argument('--MAIL_ADDRESS', nargs="+", type=str)
    parser.add_argument('--PHONE_NUMBER', nargs="+", type=str)
    parser.add_argument('--SENDKEY', nargs="+", type=str)
    argconf = parser.parse_args()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver_pjs = webdriver.Edge(
        options=chrome_options,
        executable_path=sys_path(browser="chromedriver"),
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    print('Driver Launched\n')

    for i in range(1, len(argconf.ID) + 1):
        print("第" + str(i) + "位同學開始報備")
        go('config' + str(i) + '.ini', i)

    driver_pjs.quit()
