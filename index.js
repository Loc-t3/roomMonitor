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
let weixinBlocked = false;

// 初始化
function init() {
  logger.info('🏠 房间监控系统启动');
  logger.info('📍 监控配置：');
  logger.info(`   - 上午时段 (${formatTime(config.timeRanges.morning.start)}-${formatTime(config.timeRanges.morning.end)}): ${config.addresses.morning}`);
  logger.info(`   - 下午时段 (${formatTime(config.timeRanges.afternoon.start)}-${formatTime(config.timeRanges.afternoon.end)}): ${config.addresses.afternoon}`);
  logger.info(`⏱️  请求间隔：15秒`);
  logger.info(`🌐 API地址：${config.api.url}`);
  logger.info(`📊 日志级别：${config.log.minLogLevel}`);
  logger.info('----------------------------------------');

  // 立即执行一次
  checkRooms();

  // 设置定时器，每15秒执行一次
  setInterval(checkRooms, 15000);
}

// 格式化时间显示
function formatTime(time) {
  const hours = Math.floor(time);
  const minutes = Math.round((time - hours) * 60);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

// 获取当前时间并返回目标地址
function getTargetAddressByTime() {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const currentTime = hours + minutes / 60;

  // 判断当前时间段
  if (currentTime >= config.timeRanges.morning.start && currentTime <= config.timeRanges.morning.end) {
    return config.addresses.morning;
  } else if (currentTime >= config.timeRanges.afternoon.start && currentTime <= config.timeRanges.afternoon.end) {
    return config.addresses.afternoon;
  }

  return '';
}



// 检查房间数量
async function checkRooms() {
  try {
    // 获取当前时间对应的目标地址
    const newTargetAddress = getTargetAddressByTime();

    // 如果目标地址发生变化
    if (currentTargetAddress !== newTargetAddress) {
      currentTargetAddress = newTargetAddress;
      if (currentTargetAddress) {
        logger.info(`⏰ 监控时间段切换，当前关注地址：${currentTargetAddress}`);
      } else {
        logger.info('⏰ 当前非监控时段，跳过检查');
        return;
      }
    }

    const timestamp = config.log.enableTimestamp ? new Date().toLocaleTimeString() : '';
    logger.debug(`🕐 ${timestamp} - 正在检查房间数据...`);

    // 准备请求配置
    let requestConfig = { ...config.api };

    // 如果检测到微信屏蔽，确保使用正确的微信User-Agent
    if (weixinBlocked) {
      logger.info('🔄 检测到微信屏蔽，使用微信环境配置');
    }

    logger.info(`📊 请求参数:`);
    logger.info(`   URL: ${requestConfig.url}`);
    logger.info(`   Method: ${requestConfig.method}`);
    logger.info(`   Headers: ${JSON.stringify(requestConfig.headers)}`);
    // 发送HTTP请求
    const response = await axios(requestConfig);
    const originalHtml = response.data;
    logger.info('📡 响应头:');
    logger.info(JSON.stringify(response.headers));
    logger.info('📡 响应体:');
    
    // 只显示houseType中的name和roomNum，并根据时间段只关注对应房源
    if (typeof originalHtml === 'object' && originalHtml !== null && originalHtml.data && originalHtml.data.projects) {
      const projects = originalHtml.data.projects;

      // 获取当前时间段对应的目标地址
      const targetAddress = getTargetAddressByTime();

      if (targetAddress) {
        logger.info(`当前关注地址: ${targetAddress}`);

        // 查找对应项目
        const targetProject = projects.find(project =>
          project.address.includes(targetAddress) ||
          targetAddress.includes(project.address)
        );

        if (targetProject) {
          logger.info(`项目: ${targetProject.name}`);
          if (targetProject.houseType) {
            targetProject.houseType.forEach((house) => {
              logger.info(`  - ${house.name}: ${house.roomNum}间`);

              // 系统提示 - 如果存在房间数信息
              if (house.roomNum) {
                logger.info(`系统提示: ${targetProject.name} - ${house.name} 已有房间数信息: ${house.roomNum}间`);
              }
            });
          }
        } else {
          logger.info('未找到对应项目');
        }
      } else {
        logger.info('当前非监控时段，跳过检查');
      }
    } else {
      logger.info(JSON.stringify(originalHtml));
    }

    // 计算总的房间数
    let totalRoomNum = 0;

    if (typeof originalHtml === 'object' && originalHtml !== null && originalHtml.data && originalHtml.data.projects) {
      originalHtml.data.projects.forEach(project => {
        if (project.houseType) {
          project.houseType.forEach(house => {
            if (house.roomNum) {
              totalRoomNum += Array.isArray(house.roomNum) ?
                house.roomNum.reduce((sum, num) => sum + (num || 0), 0) :
                (house.roomNum || 0);
            }
          });
        }
      });
    }

    // 打印当前的总房间数
    logger.info(`📊 当前房间数 (totalRoomNum): ${totalRoomNum}`);

    // 检查总房间数是否大于0
    if (totalRoomNum > 0) {
      alertManager.alert(currentTargetAddress, totalRoomNum);
    } else {
      logger.info(`✅ 当前没有可用房间`);
    }

    logger.debug('----------------------------------------');

  } catch (error) {
    logger.error('❌ 请求失败: ' + error.message);
    if (error.response) {
      logger.error(`   状态码: ${error.response.status}`);
      logger.error(`   响应头: ${JSON.stringify(error.response.headers)}`);
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