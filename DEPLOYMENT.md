# 部署指南

## Cloudflare Workers 部署

### 步骤 1: 登录 Cloudflare 账户
1. 访问 [Cloudflare 控制台](https://dash.cloudflare.com/)
2. 登录你的 Cloudflare 账户

### 步骤 2: 创建 Workers 项目
1. 在左侧菜单中选择 "Workers & Pages"
2. 点击 "Create Application"
3. 选择 "Create Worker"
4. 为你的 Worker 命名（例如：`room-monitor-worker`）
5. 点击 "Deploy"

### 步骤 3: 部署代码
1. 点击 "Edit Code"
2. 将 `worker.js` 文件的内容复制到编辑器中
3. 点击 "Save and Deploy"
4. 记录下你的 Worker URL（例如：`https://room-monitor-worker.your-account.workers.dev`）

### 步骤 4: 配置本地访问程序
1. 打开 `local-monitor.js` 文件
2. 将 `CLOUDFLARE_WORKER_URL` 变量修改为你的 Worker URL

```javascript
// Cloudflare Workers URL - 请替换为你的实际部署地址
const CLOUDFLARE_WORKER_URL = 'https://room-monitor-worker.your-account.workers.dev';
```

## 本地访问程序使用

### 安装依赖
```bash
npm install
```

### 运行本地监控程序
```bash
# 启动本地监控程序
npm run local

# 启动本地监控程序（开发模式，自动重启）
npm run local:dev
```

### 运行原有的直接监控程序
```bash
# 启动原有的直接监控程序
npm start

# 启动原有的直接监控程序（开发模式，自动重启）
npm run dev
```

## 测试

### 测试 Cloudflare Workers
1. 在浏览器中访问你的 Worker URL
2. 你应该看到类似以下的 JSON 响应：

```json
{
  "success": true,
  "data": {
    "currentTime": "2024-01-01 12:00:00",
    "targetAddress": "深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)",
    "totalRoomNum": 5,
    "targetProject": {
      "name": "项目名称",
      "address": "深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)",
      "houseType": [
        {
          "name": "房型1",
          "roomNum": 3
        },
        {
          "name": "房型2",
          "roomNum": 2
        }
      ]
    },
    "isMonitoringTime": true
  }
}
```

### 测试本地访问程序
1. 运行本地监控程序：`npm run local`
2. 查看控制台输出，确认程序能够正确从 Cloudflare Workers 获取数据
3. 检查提醒功能是否正常工作

## 注意事项

1. **CORS 配置**：Cloudflare Workers 代码中已经添加了 CORS 支持，允许本地访问程序跨域请求

2. **API 依赖**：Cloudflare Workers 会直接请求原始 API，因此需要确保 `worker.js` 中的 `config.api` 配置正确

3. **监控时段**：系统会根据配置的时间段自动切换监控地址

4. **错误处理**：如果 Cloudflare Workers 无法访问 API，本地程序会收到错误信息并在控制台显示

5. **部署频率**：Cloudflare Workers 有免费额度限制，请注意控制请求频率
