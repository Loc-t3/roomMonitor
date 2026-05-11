api = {
    'url': 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6',
    'method': 'GET',
    'timeout': 10,
    'headers': {
        'Host': 'sz.inboyu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'HMACCOUNT=A4EA9ED87F1F390A; Hm_lpvt_eb3a04775ee04174fb328fa239cd9f3c=1778471064; Hm_lvt_eb3a04775ee04174fb328fa239cd9f3c=1778393502,1778471064; a079f784704ff034_gr_cs1=BDCCD928-E8DF-308A-5892-6FB80F841602; a079f784704ff034_gr_session_id_9c389cec-42ec-41ab-b5fb-6793a976fbff=true; PHPSESSID=i07pqkhc2ab5qammg3u5tqn0a1; _identity=6c4d9d67b5344a4ba882ceeb2120b6cb5075c8d2438f8f6e880c7fd39d30fae2a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A49%3A%22%5B%22BDCCD928-E8DF-308A-5892-6FB80F841602%22%2C%22%22%2C86400%5D%22%3B%7D; a079f784704ff034_gr_session_id=9c389cec-42ec-41ab-b5fb-6793a976fbff; _csrf=d4dc07b7cc1fde4192c4247f815418461cd8a6202ba58e59086f470a436aa014a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%228TDrjv1a4IfKOuSQ4qgqef1UkV3kx9ON%22%3B%7D; acw_tc=2f6a1fbc17784710613896219ebc2da5efe7c8de39e8df66a1fe1526cdba6d; gr_user_id=dcd7a3a6-ab09-4fb9-8406-5fb4b375dbbc',
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/WIFI Language/zh_CN miniProgram/wx4e093affadd67bb1',
        'Referer': 'https://sz.inboyu.com/activity/graduate?id=8248ec76-016d-11f0-aa1d-a088c260cfb6&code=051oENll2sHnzh4zLjll2yO1rw1oENl4&state=OpenId',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
}

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