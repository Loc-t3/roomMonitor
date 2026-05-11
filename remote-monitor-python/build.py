import subprocess
import os

def build():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print('📦 开始安装依赖...')
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
    
    print('🔨 开始打包...')
    subprocess.run(['pyinstaller', 'remote-monitor.spec'], check=True)
    
    print('✅ 打包完成！')

if __name__ == '__main__':
    build()