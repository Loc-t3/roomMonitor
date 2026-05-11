import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime

try:
    from plyer import notification
    NOTIFIER_AVAILABLE = True
except ImportError:
    NOTIFIER_AVAILABLE = False
    print('⚠️ plyer未安装，将无法使用弹窗通知功能')
    print('请运行: pip install plyer')

def test_notification():
    print('🧪 开始测试系统通知功能...')
    
    if NOTIFIER_AVAILABLE:
        test_address = '深圳市南山区桃源街道平山村353号楼'
        test_room_num = 3
        
        message = f'''
地址：{test_address}
房间数量：{test_room_num}
检测时间：{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
        '''
        
        print('\n' + '=' * 50)
        print('🚨 🚨 🚨 房间可用提醒 🚨 🚨 🚨')
        print(message)
        print('=' * 50 + '\n')
        
        print('📤 发送系统通知...')
        try:
            notification.notify(
                title='🎉 房间可用！',
                message=f'{test_address}\n剩余房间：{test_room_num}个\n立即查看！',
                timeout=10
            )
            print('✅ 系统通知发送成功！')
            print('请检查是否收到弹窗通知')
        except Exception as e:
            print(f'❌ 发送通知失败: {e}')
    else:
        print('❌ plyer未安装，请先安装依赖')
        print('运行: pip install plyer')

if __name__ == '__main__':
    test_notification()