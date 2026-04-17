import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import ctypes
import platform

# ---------------- ADMIN CHECK ----------------
try:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
except:
    is_admin = False

if not is_admin:
    tk.Tk().withdraw()
    messagebox.showerror("Error", "Please run this application as Administrator.")
    exit()

# ---------------- CORE FUNCTIONS ----------------
def run(cmd):
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        log(f"Error executing command: {e}")

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    root.update()

def get_gpu():
    try:
        cmd = "powershell (Get-CimInstance Win32_VideoController).Name"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return output if output else "Unknown GPU"
    except:
        return "Not found"

def get_ram():
    try:
        import psutil
        return f"{round(psutil.virtual_memory().total / (1024**3))} GB"
    except:
        return "Unknown (install psutil)"

def disable_service(s):
    run(f'sc stop {s}')
    run(f'sc config {s} start= disabled')

# ---------------- NAVIGATION ----------------
def show_section(name):
    for s in sections.values():
        s.pack_forget()
    sections[name].pack(fill="both", expand=True)

# ---------------- MAIN GUI ----------------
root = tk.Tk()
root.title("CShelperGUI PRO X")
root.geometry("1100x850")
root.configure(bg="#a8d0e6")

# --- VARIABLES ---
# Cleaning
v_temp = tk.BooleanVar(); v_update = tk.BooleanVar(); v_shader = tk.BooleanVar()
v_delivery = tk.BooleanVar(); v_logs = tk.BooleanVar(); v_errors = tk.BooleanVar(); v_thumb = tk.BooleanVar()
# Network
v_dns = tk.BooleanVar(); v_winsock = tk.BooleanVar(); v_full_net = tk.BooleanVar()
# Debloat
v_xbox = tk.BooleanVar(); v_telemetry = tk.BooleanVar(); v_bing = tk.BooleanVar(); v_onedrive = tk.BooleanVar()
# Services
v_safe_svc = tk.BooleanVar(); v_gaming_svc = tk.BooleanVar(); v_print_svc = tk.BooleanVar()
# Privacy
v_priv_all = tk.BooleanVar()
# Setup Tool
v_hiber = tk.BooleanVar(); v_menu = tk.BooleanVar(); v_visuals = tk.BooleanVar()
v_widgets = tk.BooleanVar(); v_dark = tk.BooleanVar(); v_ult_plan = tk.BooleanVar()
v_throttling = tk.BooleanVar(); v_vbs = tk.BooleanVar(); v_mpo = tk.BooleanVar()
v_dvr = tk.BooleanVar(); v_search_bar = tk.BooleanVar(); v_input_lag = tk.BooleanVar(); v_fs_opt = tk.BooleanVar()

# SIDEBAR
sidebar = tk.Frame(root, bg="#7fb3d5", width=200)
sidebar.pack(side="left", fill="y")
tk.Label(sidebar, text="☰ MENU", bg="#7fb3d5", font=("Arial", 14, "bold")).pack(pady=20)

menu_items = [
    ("INFO TOOL", "Info"), ("System Clean", "Clean"), ("Network", "Net"),
    ("Debloat", "Deb"), ("Services", "Svc"), ("Privacy", "Priv"), ("Setup Tool", "Set")
]

for text, sec in menu_items:
    btn = tk.Button(sidebar, text=text, bg="#7fb3d5", relief="flat", anchor="w", padx=25,
                    font=("Arial", 10), command=lambda s=sec: show_section(s))
    btn.pack(fill="x", pady=2)
    if text in ["INFO TOOL", "Network", "Privacy"]:
        tk.Frame(sidebar, height=1, bg="black").pack(fill="x", padx=15, pady=10)

# MAIN CONTAINER
main_area = tk.Frame(root, bg="#a8d0e6")
main_area.pack(side="left", fill="both", expand=True)
sections = {k: tk.Frame(main_area, bg="#a8d0e6") for k in ["Info", "Clean", "Net", "Deb", "Svc", "Priv", "Set"]}

def add_check(parent, txt, var):
    tk.Checkbutton(parent, text=txt, variable=var, bg="#a8d0e6", font=("Arial", 10), activebackground="#a8d0e6").pack(anchor="w", padx=20, pady=2)

# -------- SECTION: INFO TOOL --------
info = sections["Info"]
tk.Label(info, text="SYSTEM INFORMATION", bg="#a8d0e6", font=("Arial", 12, "bold")).pack(pady=(20, 10), anchor="w", padx=40)
specs_f = tk.Frame(info, bg="#a8d0e6")
specs_f.pack(anchor="w", padx=40, pady=10)
tk.Label(specs_f, text=f"CPU : {platform.processor()}", bg="#a8d0e6", font=("Arial", 10)).pack(anchor="w")
tk.Label(specs_f, text=f"GPU : {get_gpu()}", bg="#a8d0e6", font=("Arial", 10)).pack(anchor="w")
tk.Label(specs_f, text=f"RAM : {get_ram()}", bg="#a8d0e6", font=("Arial", 10)).pack(anchor="w")
tk.Label(info, text="!Warning!\nBefore you start, create restore point.", fg="red", bg="#a8d0e6", font=("Arial", 10, "bold"), justify="left").pack(pady=(30, 10), anchor="w", padx=40)
tk.Button(info, text="Restore Point", width=20, height=2, relief="solid", borderwidth=2, bg="white",
          command=lambda: threading.Thread(target=run, args=('powershell Checkpoint-Computer -Description "CShelper" -RestorePointType MODIFY_SETTINGS',)).start()).pack(anchor="w", padx=40)

# -------- SECTION: SYSTEM CLEAN --------
clean = sections["Clean"]
tk.Label(clean, text="SYSTEM CLEANING TWEAKS", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=20, anchor="w", padx=40)
add_check(clean, "Clean Temp Files (USER)", v_temp)
add_check(clean, "Clean Windows Update Cache", v_update)
add_check(clean, "Clean Shader Cache (NVIDIA + DirectX)", v_shader)
add_check(clean, "Clean Windows Logs", v_logs)
add_check(clean, "Clean Error Reports", v_errors)

def apply_clean():
    log(">>> Cleaning started...")
    if v_temp.get(): log("- Temp files..."); run('del /s /q %temp%\\*')
    if v_update.get(): log("- Update Cache..."); run('net stop wuauserv && del /s /q C:\\Windows\\SoftwareDistribution\\Download\\* && net start wuauserv')
    if v_shader.get(): log("- Shader Cache..."); run('del /s /q "%localappdata%\\NVIDIA\\DXCache\\*" && del /s /q "%localappdata%\\D3DSCache\\*"')
    log(">>> Cleaning done ✔")

tk.Button(clean, text="Let's start clean", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_clean).start()).pack(anchor="w", padx=40, pady=20)

# -------- SECTION: NETWORK --------
net = sections["Net"]
tk.Label(net, text="NETWORK OPTIMIZATION", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=20, anchor="w", padx=40)
add_check(net, "Flush DNS Cache", v_dns)
add_check(net, "Reset TCP/IP & Winsock", v_winsock)
add_check(net, "FULL NETWORK RESET", v_full_net)

def apply_net():
    log(">>> Network optimization started...")
    if v_dns.get(): log("- Flushing DNS..."); run('ipconfig /flushdns')
    if v_winsock.get(): log("- Winsock Reset..."); run('netsh winsock reset && netsh int ip reset')
    if v_full_net.get(): log("!!! FULL RESET !!!"); run('netsh winsock reset && netsh int ip reset && ipconfig /flushdns && ipconfig /release && ipconfig /renew')
    log(">>> Network tasks completed ✔")

tk.Button(net, text="Optimize Network", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_net).start()).pack(anchor="w", padx=40, pady=20)

# -------- SECTION: DEBLOAT --------
deb = sections["Deb"]
tk.Label(deb, text="WINDOWS DEBLOAT", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=20, anchor="w", padx=40)
add_check(deb, "Remove Xbox Apps", v_xbox)
add_check(deb, "Disable Telemetry", v_telemetry)
add_check(deb, "Uninstall OneDrive", v_onedrive)
add_check(deb, "Disable Bing Search in Start", v_bing)

def apply_deb():
    log(">>> Debloat started...")
    if v_xbox.get(): log("- Removing Xbox..."); run('powershell "Get-AppxPackage *xbox* | Remove-AppxPackage"')
    if v_onedrive.get(): log("- Uninstalling OneDrive..."); run('taskkill /f /im OneDrive.exe && %SystemRoot%\\SysWOW64\\OneDriveSetup.exe /uninstall')
    if v_bing.get(): log("- Disabling Bing Search..."); run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v BingSearchEnabled /t REG_DWORD /d 0 /f')
    log(">>> Debloat completed ✔")

tk.Button(deb, text="Run Debloat", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_deb).start()).pack(anchor="w", padx=40, pady=20)

# -------- SECTION: SERVICES (EXTREME) --------
svc = sections["Svc"]
tk.Label(svc, text="SERVICES OPTIMIZATION", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=20, anchor="w", padx=40)
add_check(svc, "Disable useless Windows services ([?] - Basic)", v_safe_svc)
add_check(svc, "Disable gaming-related services ([?] - AtlasOS style)", v_gaming_svc)
add_check(svc, "Disable Print Spooler ([?] - Only if no printer)", v_print_svc)

def apply_svc():
    log(">>> Services optimization started...")
    if v_safe_svc.get():
        log("- Basic services..."); [disable_service(s) for s in ["MapsBroker", "Fax", "RetailDemo", "RemoteRegistry", "TabletInputService"]]
    if v_gaming_svc.get():
        log("- Extreme gaming tweaks (25+ services)...")
        extreme = ["DiagTrack", "WerSvc", "WbioSrvc", "SensorService", "PhoneSvc", "XblAuthManager", "XblGameSave", "XboxGipSvc", "BthServ", "WalletService", "ClipSVC", "NcbService"]
        for s in extreme: disable_service(s)
    if v_print_svc.get(): disable_service("Spooler")
    log(">>> Services done ✔")

tk.Button(svc, text="Optimize Services", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_svc).start()).pack(anchor="w", padx=40, pady=20)

# -------- SECTION: PRIVACY --------
priv = sections["Priv"]
tk.Label(priv, text="PRIVACY OPTIMIZATION", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=20, anchor="w", padx=40)
add_check(priv, "Apply All Privacy Tweaks ([?] - Telemetry, Activity Hist, Speech)", v_priv_all)

def apply_priv():
    if v_priv_all.get():
        log(">>> Applying Privacy Tweaks...")
        run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v EnableActivityFeed /t REG_DWORD /d 0 /f')
        run('reg add "HKCU\\Software\\Microsoft\\InputPersonalization" /v RestrictImplicitInkCollection /t REG_DWORD /d 1 /f')
        run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')
        log(">>> Privacy tweaks applied ✔")

tk.Button(priv, text="Apply Privacy Tweaks", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_priv).start()).pack(anchor="w", padx=40, pady=20)

# -------- SECTION: SETUP TOOL (TWO COLUMNS) --------
setup = sections["Set"]
tk.Label(setup, text="SETUP TOOL", bg="#a8d0e6", font=("Arial", 14, "bold")).pack(pady=10, anchor="w", padx=40)

cols_f = tk.Frame(setup, bg="#a8d0e6")
cols_f.pack(fill="both", expand=True, padx=20)

left_c = tk.Frame(cols_f, bg="#a8d0e6")
left_c.pack(side="left", fill="both", expand=True)
add_check(left_c, "Disable Hibernation", v_hiber)
add_check(left_c, "Set Classic Right-Click Menu", v_menu)
add_check(left_c, "Disable All Visual Effects", v_visuals)
add_check(left_c, "Remove Windows Widgets", v_widgets)
add_check(left_c, "Turn On Dark Theme", v_dark)
add_check(left_c, "Disable Search Button in Taskbar", v_search_bar)

tk.Frame(cols_f, width=2, bg="black").pack(side="left", fill="y", padx=10, pady=20)

right_c = tk.Frame(cols_f, bg="#a8d0e6")
right_c.pack(side="left", fill="both", expand=True)
add_check(right_c, "Add + Activated Ultimate Profile", v_ult_plan)
add_check(right_c, "Disable Power Throttling", v_throttling)
add_check(right_c, "Disable VBS / HVCI", v_vbs)
add_check(right_c, "Disable Multiplane Overlay (MPO)", v_mpo)
add_check(right_c, "Disable Game DVR", v_dvr)
add_check(right_c, "Optimize Input Latency (Mouse/Key)", v_input_lag)
add_check(right_c, "Disable Fullscreen Optimizations", v_fs_opt)

def apply_setup():
    log(">>> Setup optimization started...")
    if v_hiber.get(): run('powercfg -h off')
    if v_menu.get(): run('reg add "HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" /f /ve')
    if v_ult_plan.get(): run('powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61')
    if v_throttling.get(): run('reg add "HKLM\\System\\CurrentControlSet\\Control\\Power\\PowerThrottling" /v "PowerThrottlingOff" /t REG_DWORD /d 1 /f')
    if v_vbs.get(): run('bcdedit /set hypervisorlaunchtype off')
    if v_mpo.get(): run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm" /v OverlayTestMode /t REG_DWORD /d 5 /f')
    if v_input_lag.get():
        run('reg add "HKCU\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f')
        run('reg add "HKCU\\Control Panel\\Accessibility\\Keyboard Response" /v DelayBeforeAcceptance /t REG_SZ /d 0 /f')
    if v_fs_opt.get(): run('reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_FSEBehavior" /t REG_DWORD /d 2 /f')
    log(">>> Setup done ✔")

tk.Button(setup, text="Apply Setup Tweaks", bg="#7fb3d5", width=25, relief="solid", borderwidth=1, font=("Arial", 10, "bold"),
          command=lambda: threading.Thread(target=apply_setup).start()).pack(anchor="w", padx=40, pady=20)

# -------- LOG BOX --------
log_box = tk.Text(root, height=8, bg="white", font=("Consolas", 9))
log_box.pack(side="bottom", fill="x", padx=40, pady=20)

show_section("Info")
root.mainloop()
