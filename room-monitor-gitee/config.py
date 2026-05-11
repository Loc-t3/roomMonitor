api = {
    'url': 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6',
    'method': 'GET',
    'timeout': 10,
    'headers': {
        'Host': 'sz.inboyu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': '',
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/WIFI Language/zh_CN miniProgram/wx4e093affadd67bb1',
        'Referer': 'https://sz.inboyu.com/activity/graduate?id=8248ec76-016d-11f0-aa1d-a088c260cfb6&code=051oENll2sHnzh4zLjll2yO1rw1oENl4&state=OpenId',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
}

gitee = {
    'cookie_url': 'https://gitee.com/spectacularss/cookie-store/raw/master/cookie.txt',
    'timeout': 5
}

DEFAULT_COOKIE = ''

addresses = {
    'morning': '深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)',
    'afternoon': '深圳市南山区南头街道中山南街34号（12号线南头古城站C出口）'
}

timeRanges = {
    'morning': {'start': 12, 'end': 13.5},
    'afternoon': {'start': 13.55, 'end': 15.5}
}

alert = {
    'enableConsole': True,
    'enableNotification': True
}

log = {
    'enableTimestamp': True,
    'minLogLevel': 'info',
    'enableDebugAll': False,
    'enableTrace': True
}

REQUEST_INTERVAL = 5
CLOUDFLARE_WORKER_URL = 'https://cool-cherry-65c2.xiao-lo01.workers.dev/'