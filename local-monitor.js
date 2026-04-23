const axios = require('axios');
const { setInterval } = require('timers');
const config = require('./config');

// 尝试导入通知模块
let notifier = null;
try {
  notifier = require('node-notifier');
} catch (error) {
  console.warn('⚠️ node-notifier未安装，将无法使用弹窗通知功能');
  console.warn('请运行: npm install node-notifier');
}

// 日志工具
const logger = {
  info: (msg) => console.log(`[INFO] ${msg}`),
  warn: (msg) => console.warn(`[WARN] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`),
  debug: (msg) => {
    if (config.log.minLogLevel === 'debug') {
      console.log(`[DEBUG] ${msg}`);
    }
  },
  trace: (msg) => {
    if (config.log.enableTrace) {
      console.log(`[TRACE] ${msg}`);
    }
  }
};

// 提醒管理器
const alertManager = {
  consoleAlert: (message) => {
    if (config.alert.enableConsole) {
      console.log('\n' + '='.repeat(50));
      console.log('🚨 🚨 🚨 房间可用提醒 🚨 🚨 🚨');
      console.log(message);
      console.log('='.repeat(50) + '\n');
    }
  },

  // 发送系统通知
  sendNotification: (title, message) => {
    if (config.alert.enableNotification && notifier) {
      notifier.notify({
        title: title,
        message: message,
        sound: true, // 播放声音
        wait: true,  // 等待用户响应
        timeout: 10  // 10秒后自动关闭
      });
    }
  },

  // 组合提醒
  alert: (address, roomNum) => {
    const message = `
地址：${address}
房间数量：${roomNum}
检测时间：${new Date().toLocaleString()}
    `;

    // 控制台提醒
    alertManager.consoleAlert(message);

    // 系统通知（仅在房间数大于1时弹窗）
    if (roomNum > 1) {
      alertManager.sendNotification(
        '🎉 房间数量充足！',
        `${address}\n剩余房间：${roomNum}个\n立即查看！`
      );
    }
  }
};

// 当前关注的地址
let currentTargetAddress = '';

// Cloudflare Workers URL - 请替换为你的实际部署地址
const CLOUDFLARE_WORKER_URL = 'https://cool-cherry-65c2.xiao-lo01.workers.dev/';

// 初始化
function init() {
  logger.info('🏠 房间监控系统启动');
  logger.info('📍 监控配置：');
  logger.info(`   - 上午时段 (${formatTime(config.timeRanges.morning.start)}-${formatTime(config.timeRanges.morning.end)}): ${config.addresses.morning}`);
  logger.info(`   - 下午时段 (${formatTime(config.timeRanges.afternoon.start)}-${formatTime(config.timeRanges.afternoon.end)}): ${config.addresses.afternoon}`);
  logger.info(`⏱️  请求间隔：15秒`);
  logger.info(`📊 日志级别：${config.log.minLogLevel}`);
  logger.info('----------------------------------------');

  // 立即执行一次
  checkRooms();

  // 设置定时器，每15秒执行一次
  setInterval(checkRooms, 2000);
}

// 格式化时间显示
function formatTime(time) {
  const hours = Math.floor(time);
  const minutes = Math.round((time - hours) * 60);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

// 检查房间数量
async function checkRooms() {
  try {
    const timestamp = config.log.enableTimestamp ? new Date().toLocaleTimeString() : '';
    logger.debug(`🕐 ${timestamp} - 正在从Cloudflare Worker获取房间数据...`);

    // 从Cloudflare Worker获取数据
    const response = await axios.get(CLOUDFLARE_WORKER_URL);
    const result = response.data;

    if (result.success) {
result.data={
        currentTime: new Date().toLocaleString(),
        targetAddress: '深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)',
        totalRoomNum: 20,
        targetProject: {
              name: '单人间',
              address: '深圳市南山区桃源街道平山村353号楼',
              houseType: '单人'
            },
}
      const data = result.data;
      
      // 更新当前目标地址
      if (currentTargetAddress !== data.targetAddress) {
        currentTargetAddress = data.targetAddress;
        if (currentTargetAddress) {
          logger.info(`⏰ 监控时间段切换，当前关注地址：${currentTargetAddress}`);
        } else {
          logger.info('⏰ 当前非监控时段，跳过检查');
          return;
        }
      }

      // 打印项目信息
      if (data.targetProject) {
        logger.info(`项目: ${data.targetProject.name}`);
        if (data.targetProject.houseType) {
          data.targetProject.houseType.forEach((house) => {
            logger.info(`  - ${house.name}: ${house.roomNum}间`);

            // 系统提示 - 如果存在房间数信息
            if (house.roomNum) {
              logger.info(`系统提示: ${data.targetProject.name} - ${house.name} 已有房间数信息: ${house.roomNum}间`);
            }
          });
        }
      } else if (data.isMonitoringTime) {
        logger.info('未找到对应项目');
      }

      // 打印当前的总房间数
      logger.info(`📊 当前房间数 (totalRoomNum): ${data.totalRoomNum}`);

      // 检查总房间数是否大于0
      if (data.totalRoomNum > 0) {
        alertManager.alert(data.targetAddress, data.totalRoomNum);
      } else if (data.isMonitoringTime) {
        logger.info(`✅ 当前没有可用房间`);
      } else {
        logger.info('当前非监控时段，跳过检查');
      }

    } else {
      logger.error('❌ Cloudflare Worker返回错误: ' + result.error);
    }

    logger.debug('----------------------------------------');

  } catch (error) {
    logger.error('❌ 请求失败: ' + error.message);
    if (error.response) {
      logger.error(`   状态码: ${error.response.status}`);
    }
    logger.debug('----------------------------------------');
  }
}

// 处理程序退出
function handleExit() {
  logger.info('\n👋 监控程序已停止');
  process.exit(0);
}

process.on('SIGINT', handleExit);
process.on('SIGTERM', handleExit);

// 启动监控
init();
