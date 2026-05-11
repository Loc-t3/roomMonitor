module.exports = {
  // API请求配置
  api: {
    url: 'https://sz.inboyu.com/activity/graduate-info?id=8248ec76-016d-11f0-aa1d-a088c260cfb6', // 请替换为实际的API地址
    method: 'GET',
    timeout: 10000, // 10秒超时
    headers: {
      'Host': 'sz.inboyu.com',
      'Sec-Fetch-Site': 'same-origin',
      'Accept-Encoding': 'gzip, deflate, br',
      'Cookie': 'Hm_lpvt_eb3a04775ee04174fb328fa239cd9f3c=1777781522; Hm_lvt_eb3a04775ee04174fb328fa239cd9f3c=1776846464,1776847239,1776934103,1777781507; a079f784704ff034_gr_cs1=BDCCD928-E8DF-308A-5892-6FB80F841602; a079f784704ff034_gr_session_id_3d22bdb0-f583-4c4e-b65b-329fd5fbec47=true; _identity=6c4d9d67b5344a4ba882ceeb2120b6cb5075c8d2438f8f6e880c7fd39d30fae2a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A49%3A%22%5B%22BDCCD928-E8DF-308A-5892-6FB80F841602%22%2C%22%22%2C86400%5D%22%3B%7D; a079f784704ff034_gr_session_id=3d22bdb0-f583-4c4e-b65b-329fd5fbec47; HMACCOUNT=12EDEC443EB433F8; PHPSESSID=joj0a9frkbi313m8nf7ldu71d4; _csrf=2bcdae5b14f83f2192bcd169e61b74bc7b4d8504f619add5e792e87662198b23a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22eCAdEeU1OY9wjM5plF2pwz6rTVDKn_4O%22%3B%7D; acw_tc=2f6a1fb217777815030945978e524318fec71f16d5f7caa0ae2063205f099c; gr_user_id=b9f7c428-ddbb-4731-b2ef-be5b572ab0a2',
      'Connection': 'keep-alive',
      'Sec-Fetch-Mode': 'cors',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.70(0x1800463a) NetType/WIFI Language/zh_CN miniProgram/wx4e093affadd67bb1',
      'Referer': 'https://sz.inboyu.com/activity/graduate?id=8248ec76-016d-11f0-aa1d-a088c260cfb6&code=051oENll2sHnzh4zLjll2yO1rw1oENl4&state=OpenId',
      'Sec-Fetch-Dest': 'empty',
      'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
      // 'Content-Type': 'application/json',
      // 'X-Requested-With': 'XMLHttpRequest'
    },
    // 如果需要POST请求，可以添加以下配置
    // data: {
    //   param1: 'value1',
    //   param2: 'value2'
    // }
  },

  // 监控地址配置
  addresses: {
    morning: '深圳市南山区桃源街道平山村353号楼  (5号线大学城C出口)',
    afternoon: '深圳市南山区南头街道中山南街34号（12号线南头古城站C出口）'
  },

  // 时间段配置（24小时制）
  timeRanges: {
    morning: { start: 12, end: 13.5 }, // 12:00 - 13:30
    afternoon: { start: 13.55, end: 15.5 } // 13:55 - 14:30
  },

  // 提醒配置
  alert: {
    enableConsole: true, // 启用控制台提醒
    enableNotification: true, // 启用系统通知弹窗
    // 可以扩展其他提醒方式
    // enableSound: false,
    // soundFile: 'alert.mp3',
    // enableEmail: false,
    // email: {
    //   to: 'your-email@example.com',
    //   service: 'gmail',
    //   auth: {
    //     user: 'your-email@gmail.com',
    //     pass: 'your-password'
    //   }
    // }
  },

  // 日志配置
  log: {
    enableTimestamp: true,
    minLogLevel: 'info', // 'debug', 'info', 'warn', 'error'
    enableDebugAll: false, // 启用详细调试输出
    enableTrace: true // 启用智能追踪模式
  }
};