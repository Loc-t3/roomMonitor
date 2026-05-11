import requests
import time
import sys
from datetime import datetime

CLOUDFLARE_WORKER_URL = 'https://cool-cherry-65c2.xiao-lo01.workers.dev/'

alert = {
    'enableConsole': True,
    'enableNotification': True
}

log = {
    'enableTimestamp': True,
    'minLogLevel': 'info',
    'enableTrace': False
}

REQUEST_INTERVAL = 15

try:
    from plyer import notification
    NOTIFIER_AVAILABLE = True
except ImportError:
    NOTIFIER_AVAILABLE = False
    print('⚠️ plyer未安装，将无法使用弹窗通知功能')
    print('请运行: pip install plyer')

class Logger:
    def info(self, msg):
        print(f'[INFO] {msg}')
    
    def warn(self, msg):
        print(f'[WARN] {msg}')
    
    def error(self, msg):
        print(f'[ERROR] {msg}')
    
    def debug(self, msg):
        if log['minLogLevel'] == 'debug':
            print(f'[DEBUG] {msg}')
    
    def trace(self, msg):
        if log['enableTrace']:
            print(f'[TRACE] {msg}')

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
                notification.notify(
                    title=title,
                    message=message,
                    timeout=10
                )
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
        
        if roomNum > 1:
            AlertManager.sendNotification(
                '🎉 房间数量充足！',
                f'{address}\n剩余房间：{roomNum}个\n立即查看！'
            )

currentTargetAddress = ''

def checkRooms():
    global currentTargetAddress
    
    try:
        timestamp = datetime.now().strftime('%H:%M:%S') if log['enableTimestamp'] else ''
        logger.debug(f'🕐 {timestamp} - 正在从Cloudflare Worker获取房间数据...')
        
        response = requests.get(CLOUDFLARE_WORKER_URL, timeout=10)
        result = response.json()
        
        if result.get('success'):
            data = result['data']
            
            if currentTargetAddress != data.get('targetAddress'):
                currentTargetAddress = data.get('targetAddress', '')
                if currentTargetAddress:
                    logger.info(f'⏰ 监控时间段切换，当前关注地址：{currentTargetAddress}')
                else:
                    logger.info('⏰ 当前非监控时段，跳过检查')
                    return
            
            if data.get('targetProject'):
                logger.info(f'项目: {data["targetProject"].get("name")}')
                if data['targetProject'].get('houseType'):
                    for house in data['targetProject']['houseType']:
                        logger.info(f'  - {house.get("name")}: {house.get("roomNum")}间')
                        if house.get('roomNum'):
                            logger.info(f'系统提示: {data["targetProject"].get("name")} - {house.get("name")} 已有房间数信息: {house.get("roomNum")}间')
            elif data.get('isMonitoringTime'):
                logger.info('未找到对应项目')
            
            totalRoomNum = data.get('totalRoomNum', 0)
            logger.info(f'📊 当前房间数 (totalRoomNum): {totalRoomNum}')
            
            if totalRoomNum > 0:
                AlertManager.alert(currentTargetAddress, totalRoomNum)
            elif data.get('isMonitoringTime'):
                logger.info('✅ 当前没有可用房间')
            else:
                logger.info('当前非监控时段，跳过检查')
        
        else:
            logger.error('❌ Cloudflare Worker返回错误: ' + result.get('error', '未知错误'))
        
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
    logger.info('🏠 房间监控系统启动 (远程模式)')
    logger.info(f'🌐 Cloudflare Worker地址：{CLOUDFLARE_WORKER_URL}')
    logger.info(f'⏱️  请求间隔：{REQUEST_INTERVAL}秒')
    logger.info(f'📊 日志级别：{log["minLogLevel"]}')
    logger.info('----------------------------------------')
    
    checkRooms()
    
    while True:
        try:
            time.sleep(REQUEST_INTERVAL)
            checkRooms()
        except KeyboardInterrupt:
            handleExit()

if __name__ == '__main__':
    init()