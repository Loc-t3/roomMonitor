# 房间监控系统 (Python版)

## 项目结构

```
room-monitor-python/
├── config.py          # 配置文件（API、地址、时段、提醒设置）
├── room_monitor.py    # 主监控程序
├── requirements.txt   # Python依赖清单
├── build.py           # PyInstaller打包脚本
├── README.md          # 说明文档
└── dist/              # 打包输出目录
    ├── room-monitor.exe  # 可执行文件
    └── config.py         # 配置文件
```

## 功能说明

1. **时间规则**：
   - 12:00 - 13:30：关注 "深圳市南山区桃源街道平山村353号楼"
   - 13:55 - 15:30：关注 "深圳市南山区南头街道中山南街34号"

2. **监控规则**：
   - 每15秒发起一次HTTP请求
   - 智能过滤干扰数据，只识别真实的房间数量
   - 当房间数 > 0 时触发控制台和系统通知提醒
   - 房间数 > 1 时弹出系统通知弹窗

## 使用方法

### 方式一：直接运行（需要Python环境）

```bash
cd room-monitor-python
pip install -r requirements.txt
python room_monitor.py
```

### 方式二：运行已打包的可执行文件（推荐）

```bash
cd room-monitor-python\dist
# Windows
room-monitor.exe
```

## 打包说明

如需重新打包：

```bash
cd room-monitor-python
python build.py
```

打包后，可执行文件位于 `dist/room-monitor.exe`，用户无需安装Python或任何依赖即可直接运行。

## 配置说明

编辑 `config.py` 文件可以修改：

- `api.url`：API请求地址
- `addresses`：监控的地址
- `timeRanges`：监控时间段（24小时制，小数点表示分钟）
- `alert`：提醒设置（控制台/系统通知）
- `log`：日志级别

## 停止程序

按 `Ctrl+C` 停止程序运行。