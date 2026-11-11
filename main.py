import win32api
from time import sleep
from win32con import VK_MEDIA_PLAY_PAUSE, KEYEVENTF_EXTENDEDKEY
import psutil
import ctypes
from ctypes import wintypes
import win32com.client as comclt
import pyautogui
import pygetwindow as gw
import win32process
import win32api
import win32con
wsh= comclt.Dispatch("WScript.Shell")

user32 = ctypes.windll.user32

def getSpotifySong():
    windows = pyautogui.getAllWindows()

    for window in windows:
        if (" - " in window.title):
            try:
                hwnd = gw.getWindowsWithTitle(window.title)
                hwnd = int(str(hwnd)[18:len(str(hwnd))-2])
                pid = win32process.GetWindowThreadProcessId(hwnd)
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
                proc_name = win32process.GetModuleFileNameEx(handle, 0)
                if ("Spotify.exe" in proc_name):
                    return str(window.title)
            except:
                pass
    return str('-')

print('Spotify sollte nun nicht mehr pausiert werden. Während du andere Medien benutzt (z.B. Videos im Browser anguckst), kann es sein, dass diese statt Spotify pausiert werden. Damit Spotify weiter pausiert wird, stelle sicher, dass die Musik von Spotify immer als letztes gestartet wurde.')
sleep(2)
seconds=0
while(True):
    seconds=seconds+1
    sleep(1)
    if getSpotifySong()=='-':
        seconds=0
        print('Spotify spielt keine Musik')
    else:
        print('Spotify spielt Musik und wird in '+str(25-seconds)+'s pausiert')
    if seconds>24:

        h_wnd = user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))

        if str(psutil.Process(pid.value).name())=='Spotify.exe':
            print('Leertaste benutzt.')
            wsh.SendKeys(" ")
            sleep(0.01)
            wsh.SendKeys(" ")
        else:
            print('Mediataste benutzt, da das Spotify-Fenster nicht aktiv ist.')
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
            sleep(0.3)
            win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
        seconds=0

    