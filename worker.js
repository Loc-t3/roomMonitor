// Cloudflare Workers 兼容代码

// 配置信息
const config = {
  // API请求配置
  api: {
    url: 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6',
    method: 'GET',
    headers: {
      'Host': 'sz.inboyu.com',
      'Sec-Fetch-Site': 'same-origin',
      'Accept-Encoding': 'gzip, deflate, br',
      'Cookie': 'a079f784704ff034_gr_session_id_b0829d03-04b6-47c5-9722-73beace8d298=true; _identity=6c4d9d67b5344a4ba882ceeb2120b6cb5075c8d2438f8f6e880c7fd39d30fae2a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A49%3A%22%5B%22BDCCD928-E8DF-308A-5892-6FB80F841602%22%2C%22%22%2C86400%5D%22%3B%7D; HMACCOUNT=5616864F546EB701; Hm_lpvt_eb3a04775ee04174fb328fa239cd9f3c=1776934103; Hm_lvt_eb3a04775ee04174fb328fa239cd9f3c=1776837362,1776846464,1776847239,1776934103; a079f784704ff034_gr_cs1=BDCCD928-E8DF-308A-5892-6FB80F841602; a079f784704ff034_gr_session_id=b0829d03-04b6-47c5-9722-73beace8d298; PHPSESSID=3eqp5q5m1sg2hrk1jl7eq605r4; _csrf=4f5a8e35963e1fd94e3828def8c1c94525da88e58da2bdf931255f11a3b35faca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pbxkGhWzbFLicWoVRChPXnedI1lM2-i6%22%3B%7D; acw_tc=2f6a1f9b17769340998906540ed2beec4ec13e014e0344c75276c20076b694; gr_user_id=b9f7c428-ddbb-4731-b2ef-be5b572ab0a2',
      'Connection': 'keep-alive',
      'Sec-Fetch-Mode': 'cors',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/WIFI Language/zh_CN miniProgram/wx4e093affadd67bb1',
      'Referer': 'https://sz.inboyu.com/activity/graduate?id=8248ec76-016d-11f0-aa1d-a088c260cfb6&code=051oENll2sHnzh4zLjll2yO1rw1oENl4&state=OpenId',
      'Sec-Fetch-Dest': 'empty',
      'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
  },

  // 监控地址配置
  addresses: {
    morning: '深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)',
    afternoon: '深圳市南山区南头街道中山南街34号（12号线南头古城站C出口）'
  },

  // 时间段配置（24小时制）
  timeRanges: {
    morning: { start: 12, end: 13.5 }, // 12:00 - 13:30
    afternoon: { start: 13.55, end: 17.5 } // 13:55 - 14:30
  }
};

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
    const targetAddress = getTargetAddressByTime();
    
    // 准备请求配置
    const requestConfig = {
      method: config.api.method,
      headers: config.api.headers
    };

    // 发送HTTP请求
    const response = await fetch(config.api.url, requestConfig);
    const originalHtml = await response.json();

    // 计算总的房间数
    let totalRoomNum = 0;
    let targetProjectInfo = null;

    if (originalHtml && originalHtml.data && originalHtml.data.projects) {
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

        // 查找目标地址的项目
        if (targetAddress && !targetProjectInfo) {
          if (project.address.includes(targetAddress) || targetAddress.includes(project.address)) {
            targetProjectInfo = {
              name: project.name,
              address: project.address,
              houseType: project.houseType
            };
          }
        }
      });
    }

    // 返回结果
    return {
      success: true,
      data: {
        currentTime: new Date().toLocaleString(),
        targetAddress: targetAddress,
        totalRoomNum: totalRoomNum,
        targetProject: targetProjectInfo,
        isMonitoringTime: !!targetAddress
      }
    };

  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

// Cloudflare Workers 入口函数
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  // 处理CORS
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };

  // 处理OPTIONS请求
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders
    });
  }

  // 执行房间检查
  const result = await checkRooms();

  // 返回JSON响应
  return new Response(JSON.stringify(result, null, 2), {
    headers: {
      ...corsHeaders,
      'Content-Type': 'application/json'
    }
  });
}
