@echo off
echo 启动房间监控系统 - 智能版本
echo.
echo 正在安装依赖（如果尚未安装）...
call npm install
echo.
echo 启动智能程序...
echo [TRACE] 标记将显示智能过滤过程，避免误判用户代理字符串等干扰
echo.
node index-smart.js
pause