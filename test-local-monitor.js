const axios = require('axios');
const { setInterval } = require('timers');

// 模拟配置
const config = {
  alert: {
    enableConsole: true,
    enableNotification: true
  },
  log: {
    minLogLevel: 'info',
    enableTimestamp: true,
    enableTrace: true
  },
  timeRanges: {
    morning: { start: 0, end: 24 }, // 设置为全天监控
    afternoon: { start: 0, end: 24 }
  },
  addresses: {
    morning: '测试地址',
    afternoon: '测试地址'
  }
};

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

// 模拟Cloudflare Worker响应
function mockWorkerResponse(roomNum) {
  return {
    success: true,
    data: {
      currentTime: new Date().toLocaleString(),
      targetAddress: '测试地址',
      totalRoomNum: roomNum,
      targetProject: {
        name: '测试项目',
        address: '测试地址',
        houseType: [
          {
            name: '测试房型1',
            roomNum: roomNum
          }
        ]
      },
      isMonitoringTime: true
    }
  };
}

// 测试函数
async function testRoomAlert() {
  console.log('🧪 开始测试房间数量提示功能\n');

  // 测试场景1：房间数量为0（无提示）
  console.log('📋 测试场景1：房间数量为0');
  const response1 = mockWorkerResponse(0);
  await processWorkerResponse(response1);
  console.log('');

  // 测试场景2：房间数量为1（仅控制台提示）
  console.log('📋 测试场景2：房间数量为1');
  const response2 = mockWorkerResponse(1);
  await processWorkerResponse(response2);
  console.log('');

  // 测试场景3：房间数量为5（控制台提示+系统通知）
  console.log('📋 测试场景3：房间数量为5');
  const response3 = mockWorkerResponse(5);
  await processWorkerResponse(response3);
  console.log('');

  console.log('🧪 测试完成');
}

// 处理Worker响应
async function processWorkerResponse(response) {
  try {
    const result = response;

    if (result.success) {
      const data = result.data;
      
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

  } catch (error) {
    logger.error('❌ 处理响应失败: ' + error.message);
  }
}

// 运行测试
testRoomAlert();
