import os
import requests
import time
import sys
import json
from datetime import datetime
import ctypes
from ctypes import wintypes



NOTIFIER_AVAILABLE = True

session = requests.Session()

class WindowsNotification:
    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        
        self.user32.MessageBoxW.argtypes = [
            wintypes.HWND,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.UINT
        ]
        self.user32.MessageBoxW.restype = wintypes.INT
        
        self.MB_OK = 0x00000000
        self.MB_ICONINFORMATION = 0x00000040
        self.MB_TOPMOST = 0x00040000
    
    def notify(self, title, message, timeout=10):
        try:
            flags = self.MB_OK | self.MB_ICONINFORMATION | self.MB_TOPMOST
            self.user32.MessageBoxW(None, message, title, flags)
            return True
        except Exception as e:
            print(f'通知失败: {e}')
            return False

windows_notifier = WindowsNotification()

api = {
    'url': 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6',
    'method': 'GET',
    'timeout': 3,
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
    'morning': {'start': 7, 'end': 13.8},
    'afternoon': {'start': 13.8, 'end': 23}
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

REQUEST_INTERVAL = 4


class Logger:
    def print_log(self, prefix, msg):
        try:
            print(f'{prefix} {msg}')
        except UnicodeEncodeError:
            msg = msg.encode('ascii', 'replace').decode('ascii')
            print(f'{prefix} {msg}')
    
    def info(self, msg):
        self.print_log('[INFO]', msg)
    
    def warn(self, msg):
        self.print_log('[WARN]', msg)
    
    def error(self, msg):
        self.print_log('[ERROR]', msg)
    
    def debug(self, msg):
        if log['minLogLevel'] == 'debug':
            self.print_log('[DEBUG]', msg)
    
    def trace(self, msg):
        if log['enableTrace']:
            self.print_log('[TRACE]', msg)

logger = Logger()

class AlertManager:
    @staticmethod
    def consoleAlert(message):
        if alert['enableConsole']:
            print('\n' + '=' * 50)
            print('🚨 🚨 🚨 房间可用提醒 🚨 🚨 🚨')
            print(message)
            print('=' * 50 + '\n')
    
    @staticmethod
    def sendNotification(title, message):
        if alert['enableNotification'] and NOTIFIER_AVAILABLE:
            try:
                windows_notifier.notify(title, message)
            except Exception as e:
                logger.error(f'发送通知失败: {e}')
    
    @staticmethod
    def alert(address, roomNum):
        message = f'''
地址：{address}
房间数量：{roomNum}
检测时间：{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
        '''
        AlertManager.consoleAlert(message)
        
        if roomNum > 0:
            AlertManager.sendNotification(
                '🎉 房间可用！',
                f'{address}\n剩余房间：{roomNum}个\n立即查看！'
            )

currentTargetAddress = ''

def formatTime(time_val):
    hours = int(time_val)
    minutes = int((time_val - hours) * 60)
    return f'{hours:02d}:{minutes:02d}'

def getTargetAddressByTime():
    now = datetime.now()
    currentTime = now.hour + now.minute / 60
    
    if timeRanges['morning']['start'] <= currentTime <= timeRanges['morning']['end']:
        return addresses['morning']
    elif timeRanges['afternoon']['start'] <= currentTime <= timeRanges['afternoon']['end']:
        return addresses['afternoon']
    return ''

def fetch_cookie_from_gitee():
    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(gitee['cookie_url'], timeout=gitee['timeout'])
        response.raise_for_status()
        cookie = response.text.strip()
        if cookie:
            logger.info('✅ 成功从获取Cookie')
            return cookie
    except requests.exceptions.RequestException as e:
        logger.warn(f'❌ 从Gitee获取Cookie失败: {e}')
    
    logger.info('⚠️ 使用本地默认Cookie')
    return DEFAULT_COOKIE

def checkRooms():
    global currentTargetAddress
    
    try:
        newTargetAddress = getTargetAddressByTime()
        
        if currentTargetAddress != newTargetAddress:
            currentTargetAddress = newTargetAddress
            if currentTargetAddress:
                logger.info(f'⏰ 监控时间段切换')
            else:
                logger.info('⏰ 当前非监控时段，跳过检查')
                return
        
        timestamp = datetime.now().strftime('%H:%M:%S') if log['enableTimestamp'] else ''
        logger.debug(f'🕐 {timestamp} - 正在检查房间数据...')
        
        requestConfig = api.copy()
        
        response = session.request(
            method=requestConfig['method'],
            url=requestConfig['url'],
            headers=requestConfig['headers'],
            timeout=requestConfig['timeout']
        )
        
        try:
            originalHtml = response.json()
        except ValueError:
            originalHtml = response.text
        
        totalRoomNum = 0
        targetProject = None
        
        if isinstance(originalHtml, dict) and originalHtml.get('data') and originalHtml['data'].get('projects'):
            projects = originalHtml['data']['projects']
            
            for project in projects:
                if project.get('houseType'):
                    for house in project['houseType']:
                        if house.get('roomNum'):
                            roomNum = house['roomNum']
                            if isinstance(roomNum, list):
                                totalRoomNum += sum(num or 0 for num in roomNum)
                            else:
                                totalRoomNum += roomNum or 0
                                
            logger.info(f'📊 当前房间数 : {totalRoomNum}')
            if totalRoomNum > 0:
                
                AlertManager.alert(currentTargetAddress, totalRoomNum)
            else:
                if getTargetAddressByTime():
                    logger.info('✅ 当前没有可用房间')
                else:
                    logger.info('当前非监控时段，跳过检查')
            
            targetAddress = getTargetAddressByTime()
            
            if targetAddress:
                logger.info(f'当前关注地址: {targetAddress}')
                
                targetProject = next((p for p in projects if targetAddress in p.get('address', '') or p.get('address', '') in targetAddress), None)
                
                if targetProject:
                    logger.info(f'项目: {targetProject.get("name")}')
                    if targetProject.get('houseType'):
                        for house in targetProject['houseType']:
                            logger.info(f'  - {house.get("name")}: {house.get("roomNum")}间')
                            if house.get('roomNum'):
                                logger.info(f'系统提示: {targetProject.get("name")} - {house.get("name")} 已有房间数信息: {house.get("roomNum")}间')
                else:
                    logger.info('未找到对应项目')
            else:
                logger.info('当前非监控时段，跳过检查')
        else:
            logger.info(str(originalHtml)[:500] if len(str(originalHtml)) > 500 else str(originalHtml))
        
        

        logger.debug('----------------------------------------')
        
    except requests.exceptions.RequestException as e:
        logger.error(f'❌ 请求失败: {e}')
        if hasattr(e, 'response') and e.response:
            logger.error(f'   状态码: {e.response.status_code}')
        logger.debug('----------------------------------------')

def handleExit():
    logger.info('\n👋 监控程序已停止')
    sys.exit(0)

def init():
    logger.info('🏠 房间监控系统启动')
    
    cookie = fetch_cookie_from_gitee()
    api['headers']['Cookie'] = cookie
    
    logger.info('📍 监控配置：')
    logger.info(f'   - 上午时段 ({formatTime(timeRanges["morning"]["start"])}-{formatTime(timeRanges["morning"]["end"])}): {addresses["morning"]}')
    logger.info(f'   - 下午时段 ({formatTime(timeRanges["afternoon"]["start"])}-{formatTime(timeRanges["afternoon"]["end"])}): {addresses["afternoon"]}')
    logger.info('----------------------------------------')
    
    
    
    
    while True:
        try:
            check_start_time = time.time()
            logger.info(f'[TIMER] checkRooms开始')
            checkRooms()
            check_end_time = time.time()
            check_duration = check_end_time - check_start_time
            logger.info(f'[TIMER] checkRooms耗时: {check_duration:.3f}秒')
            logger.info('----------------------------------------')
            time.sleep(REQUEST_INTERVAL)
        except KeyboardInterrupt:
            handleExit()

if __name__ == '__main__':
    init()