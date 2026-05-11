import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    build_dir = Path('build')
    dist_dir = Path('dist')
    
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
            print(f'✅ 清理目录: {build_dir}')
        except Exception as e:
            print(f'⚠️ 清理目录失败 {build_dir}: {e}')
    
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
            print(f'✅ 清理目录: {dist_dir}')
        except Exception as e:
            print(f'⚠️ 清理目录失败 {dist_dir}: {e}')

def run_pyinstaller():
    cmd = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--name=room-monitor',
        '--icon=NONE',
        'room_monitor.py'
    ]
    
    print(f'📦 执行打包命令: {" ".join(cmd)}')
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk', errors='replace')
    
    print('\n📝 PyInstaller 输出:')
    if result.stdout:
        print('STDOUT:')
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    
    if result.stderr:
        print('\nSTDERR:')
        print(result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
    
    return result.returncode == 0

def verify_build():
    dist_path = Path('dist/room-monitor.exe')
    
    if dist_path.exists():
        file_size = dist_path.stat().st_size / (1024 * 1024)
        print(f'\n✅ 打包成功！')
        print(f'📁 产物路径: {dist_path.resolve()}')
        print(f'📊 文件大小: {file_size:.2f} MB')
        return True
    else:
        print('\n❌ 打包失败：未找到产物文件')
        return False

def main():
    print('🚀 开始打包房间监控程序...')
    print('=' * 50)
    
    try:
        clean_build_dirs()
        
        if not run_pyinstaller():
            print('\n❌ PyInstaller 执行失败')
            sys.exit(1)
        
        if not verify_build():
            sys.exit(1)
        
        print('=' * 50)
        print('🎉 打包完成！')
        print(f'📌 可执行文件位于: {Path("dist/room-monitor.exe").resolve()}')
        
    except Exception as e:
        print(f'\n❌ 打包过程发生错误: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()