import os
import sys
import subprocess
import shutil
import platform

def run_command(cmd, cwd=None):
    print(f'执行命令: {cmd}')
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f'命令执行失败: {result.stderr}')
            return False
        print(f'命令执行成功: {result.stdout}')
        return True
    except Exception as e:
        print(f'执行命令时出错: {e}')
        return False

def build():
    print('🏗️ 开始构建房间监控系统...')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(current_dir, 'dist')
    build_dir = os.path.join(current_dir, 'build')
    
    if os.path.exists(dist_dir):
        print('🧹 清理旧的dist目录...')
        shutil.rmtree(dist_dir)
    
    if os.path.exists(build_dir):
        print('🧹 清理旧的build目录...')
        shutil.rmtree(build_dir)
    
    print('📦 安装依赖...')
    if not run_command('pip install -r requirements.txt', cwd=current_dir):
        print('❌ 依赖安装失败')
        return
    
    print('📦 安装PyInstaller...')
    if not run_command('pip install pyinstaller', cwd=current_dir):
        print('❌ PyInstaller安装失败')
        return
    
    print('🔧 开始打包...')
    cmd = f'pyinstaller --onefile --name room-monitor room_monitor.py'
    
    if not run_command(cmd, cwd=current_dir):
        print('❌ 打包失败')
        return
    
    print('✅ 构建完成！')
    print(f'📦 可执行文件位置: {dist_dir}')
    
    if platform.system() == 'Windows':
        exe_path = os.path.join(dist_dir, 'room-monitor.exe')
        print(f'🚀 运行方式: 双击 {exe_path} 或在命令行运行')
    else:
        exe_path = os.path.join(dist_dir, 'room-monitor')
        print(f'🚀 运行方式: chmod +x {exe_path} && {exe_path}')

if __name__ == '__main__':
    build()