import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch, MagicMock
from datetime import datetime


def test_morning_no_rooms():
    """测试上午时段（12:00-13:30）上午地址房间数量为0的情况"""
    print('\n=== 测试1：上午时段，房间数量为0 ===')
    
    with patch('room_monitor.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 5, 11, 15, 30, 0)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        with patch('room_monitor.requests.Session') as mock_session:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'data': {
                    'projects': [
                        {
                            'name': '泊寓｜大学城店',
                            'address': '深圳市南山区桃源街道平山村353号楼',
                            'houseType': [
                                {'name': '单人间', 'roomNum': 10},
                                {'name': '双人间', 'roomNum': 0}
                            ]
                        },
                        {
                            'name': '泊寓｜南头古城店',
                            'address': '深圳市南山区南头街道中山南街34号',
                            'houseType': [
                                {'name': '单人间', 'roomNum': 0},
                                {'name': '双人间', 'roomNum': 0}
                            ]
                        }
                    ]
                }
            }
            mock_session.return_value.request.return_value = mock_response
            
            import room_monitor
            room_monitor.currentTargetAddress = ''
            room_monitor.checkRooms()
    
    print('✅ 测试1完成：上午时段房间数量为0')


def test_afternoon_has_rooms():
    """测试下午时段（13:33-18:00）下午地址房间数量为10的情况"""
    print('\n=== 测试2：下午时段，房间数量为10 ===')
    
    with patch('room_monitor.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 5, 11, 14, 30, 0)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        with patch('room_monitor.requests.Session') as mock_session:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'data': {
                    'projects': [
                        {
                            'name': '泊寓｜大学城店',
                            'address': '深圳市南山区桃源街道平山村353号楼',
                            'houseType': [
                                {'name': '单人间', 'roomNum': 0},
                                {'name': '双人间', 'roomNum': 0}
                            ]
                        },
                        {
                            'name': '泊寓｜南头古城店',
                            'address': '深圳市南山区南头街道中山南街34号',
                            'houseType': [
                                {'name': '单人间', 'roomNum': 0},
                                {'name': '双人间', 'roomNum': 0}
                            ]
                        }
                    ]
                }
            }
            mock_session.return_value.request.return_value = mock_response
            
            import room_monitor
            room_monitor.currentTargetAddress = ''
            room_monitor.checkRooms()
    
    print('✅ 测试2完成：下午时段房间数量为10')


def test_non_monitoring_hours():
    """测试非监控时段（如上午10点）跳过检查"""
    print('\n=== 测试3：非监控时段 ===')
    
    with patch('room_monitor.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 5, 11, 10, 0, 0)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        import room_monitor
        room_monitor.currentTargetAddress = ''
        room_monitor.checkRooms()
    
    print('✅ 测试3完成：非监控时段跳过检查')


if __name__ == '__main__':
    test_morning_no_rooms()
    test_afternoon_has_rooms()
    test_non_monitoring_hours()
    print('\n🎉 所有测试完成！')