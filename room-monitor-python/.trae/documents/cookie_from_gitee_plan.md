# Cookie从Gitee仓库获取 - 实现方案

## 一、需求分析

### 1.1 问题背景
当前项目中Cookie硬编码在配置文件中，由于Cookie每天更新，需要重新编译程序才能更新Cookie，非常不便。

### 1.2 需求目标
- 将Cookie存储在Gitee仓库的文件中
- 程序启动时自动从Gitee获取最新Cookie
- 网络失败时使用本地默认Cookie作为备用

---

## 二、可行性分析

| 维度 | 说明 | 可行性 |
|------|------|--------|
| 技术实现 | Gitee支持Raw文件访问，可通过HTTP GET获取文件内容 | ✅ |
| 安全性 | Cookie属于敏感信息，建议使用私有仓库或加密存储 | ⚠️ |
| 网络依赖 | 需要网络连接获取Cookie，需处理网络异常 | ✅ |
| 兼容性 | 使用现有requests库即可实现，无需额外依赖 | ✅ |

---

## 三、执行方案

### 3.1 Gitee仓库准备
1. 在Gitee创建仓库（建议私有仓库）
2. 创建 `cookie.txt` 文件，内容为纯Cookie字符串

### 3.2 代码修改

#### 文件1：`config.py`
- 添加Gitee仓库配置项
- 保留默认Cookie作为fallback

#### 文件2：`room_monitor.py`
- 添加 `fetch_cookie_from_gitee()` 函数
- 在 `init()` 函数开头调用获取Cookie
- 更新请求头中的Cookie值

---

## 四、修改清单

| 文件 | 修改内容 | 类型 |
|------|----------|------|
| `config.py` | 添加gitee配置字典 | 修改 |
| `room_monitor.py` | 添加Cookie获取函数，修改init() | 修改 |

---

## 五、代码示例

### 5.1 config.py 修改后
```python
api = {
    'url': 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6',
    'method': 'GET',
    'timeout': 10,
    'headers': {
        'Host': 'sz.inboyu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': '',  # 留空，程序启动时填充
        'Connection': 'keep-alive',
        'Sec-Fetch-Mode': 'cors',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/WIFI Language/zh_CN miniProgram/wx4e093affadd67bb1',
        'Referer': 'https://sz.inboyu.com/activity/graduate?id=8248ec76-016d-11f0-aa1d-a088c260cfb6&code=051oENll2sHnzh4zLjll2yO1rw1oENl4&state=OpenId',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
}

# Gitee Cookie配置
gitee = {
    'cookie_url': 'https://gitee.com/<username>/<repo>/raw/main/cookie.txt',
    'timeout': 5
}

# 默认Cookie（备用）
DEFAULT_COOKIE = 'HMACCOUNT=A4EA9ED87F1F390A; Hm_lpvt_eb3a04775ee04174fb328fa239cd9f3c=1778471064; ...'

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
```

### 5.2 room_monitor.py 修改后
```python
def fetch_cookie_from_gitee():
    """从Gitee仓库获取最新Cookie"""
    try:
        response = requests.get(gitee['cookie_url'], timeout=gitee['timeout'])
        response.raise_for_status()
        cookie = response.text.strip()
        if cookie:
            logger.info(f'✅ 成功从Gitee获取Cookie')
            return cookie
    except requests.exceptions.RequestException as e:
        logger.warn(f'❌ 从Gitee获取Cookie失败: {e}')
    
    logger.info('⚠️ 使用本地默认Cookie')
    return DEFAULT_COOKIE

def init():
    global api
    logger.info('🏠 房间监控系统启动')
    
    # 获取Cookie
    cookie = fetch_cookie_from_gitee()
    api['headers']['Cookie'] = cookie
    
    logger.info('📍 监控配置：')
    logger.info(f'   - 上午时段 ({formatTime(timeRanges["morning"]["start"])}-{formatTime(timeRanges["morning"]["end"])}): {addresses["morning"]}')
    logger.info(f'   - 下午时段 ({formatTime(timeRanges["afternoon"]["start"])}-{formatTime(timeRanges["afternoon"]["end"])}): {addresses["afternoon"]}')
    logger.info(f'⏱️  请求间隔：{REQUEST_INTERVAL}秒')
    logger.info(f'🌐 API地址：{api["url"]}')
    logger.info(f'📊 日志级别：{log["minLogLevel"]}')
    logger.info('----------------------------------------')
    
    checkRooms()
    
    while True:
        try:
            checkRooms()
            time.sleep(REQUEST_INTERVAL)
        except KeyboardInterrupt:
            handleExit()
```

---

## 六、风险与注意事项

### 6.1 安全性风险
- **Cookie泄露**：如果仓库设为公开，Cookie可能被他人获取
- **建议**：使用Gitee私有仓库，或对Cookie进行加密存储

### 6.2 网络依赖
- 如果网络不可用，将使用默认Cookie（可能已过期）
- 建议定期更新默认Cookie

### 6.3 Gitee URL格式
私有仓库的Raw文件URL需要包含访问令牌：
```
https://gitee.com/<username>/<repo>/raw/main/cookie.txt?access_token=<token>
```

---

## 七、操作步骤

1. 在Gitee创建仓库并上传 `cookie.txt`
2. 修改 `config.py` 配置Gitee URL
3. 修改 `room_monitor.py` 添加Cookie获取逻辑
4. 测试运行程序
5. 重新打包（如需）
