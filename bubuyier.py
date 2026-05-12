# ===================== 版权声明 =====================
# 桌宠软件：布布一二桌面宠物
# 开发者：[抖音昵称：布布一二特效大王]
# 邮箱：[2524507105@qq.com]
# 抖音ID：[38739236249]
# 版权所有 © 2026 [@Duang]，保留所有权利
# 许可协议：非商业使用免费，转载/分发需保留完整版权信息
# 禁止未经授权的修改、破解和商业用途
# =====================================================

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import random
import os
import time
import sys

# ===================== 加密打包资源路径 =====================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

RES = resource_path("pet_res")
# 自定义图标路径（替换根目录的 icon.png 即可）
ICON_PATH = resource_path("icon.png")

# ===================== 全局配置 =====================
WIN_TOPMOST = True
TRANSPARENT_COLOR = "white"
PET_W = 120
PET_H = 120
GIF_INTERVAL = 100
MIN_DISPLAY_TIME = 5
SLEEP_IMAGE_INTERVAL = 5000  # 睡觉图片5秒切换

# 三大皮肤
SKIN_LIST = ["bubu", "yier", "both"]
SKIN_CN = {"bubu":"布布", "yier":"一二", "both":"布布&一二"}
current_skin = "bubu"

# 状态配置
MOOD_LIST = ["joy", "calm", "sad", "angry"]
MOOD_CN = {"joy":"喜悦", "calm":"平静", "sad":"悲伤", "angry":"生气"}
WALK_DIR_LIST = ["left", "right"]
DIR_CN = {"left":"向左", "right":"向右"}

auto_mode = True
APP_RUNNING = True
is_sleep_lock = False

# 音效配置
VOLUME = 0.3
MUTE = False

# 屏幕边缘隐藏配置
HIDE_MARGIN = 20
IS_HIDDEN = False
ORIGINAL_X = 0

# 初始化音效
pygame.mixer.init()

# ===================== 窗口鼠标穿透修复 =====================
def set_window_click_through(root):
    try:
        import ctypes
        hwnd = root.winfo_id()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        style &= ~0x00200000
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
    except:
        pass

# ===================== 设置自定义窗口图标 =====================
def set_window_icon(window):
    try:
        icon = Image.open(ICON_PATH)
        icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(icon)
        window.iconphoto(True, photo)
    except:
        pass

# ===================== 工具函数 =====================
def get_gif_path(skin, main_st, sub_name):
    if main_st == "static":
        path = os.path.join(RES, "skins", skin, "静止", MOOD_CN[sub_name])
    elif main_st == "walk":
        path = os.path.join(RES, "skins", skin, "走路", DIR_CN[sub_name])
    else:
        path = os.path.join(RES, "skins", skin, "睡觉")
    return path

def load_single_gif(gif_path):
    frames = []
    try:
        img = Image.open(gif_path)
        for i in range(img.n_frames):
            img.seek(i)
            frame = img.convert("RGBA").resize((PET_W, PET_H), Image.Resampling.NEAREST)
            frames.append(ImageTk.PhotoImage(frame))
        return frames
    except:
        return []

def load_current_state_frames(main_st, sub_name):
    path = get_gif_path(current_skin, main_st, sub_name)
    if not os.path.exists(path):
        return []
    files = [f for f in os.listdir(path) if f.lower().endswith(".gif")]
    if not files:
        return []
    return load_single_gif(os.path.join(path, random.choice(files)))

def get_all_sleep_gif_paths():
    path = get_gif_path(current_skin, "sleep", "")
    if not os.path.exists(path):
        return []
    return [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(".gif")]

def play_sound(skin, s_name):
    if MUTE:
        return
    try:
        path = os.path.join(RES, "sound", skin, f"{s_name}.wav")
        s = pygame.mixer.Sound(path)
        s.set_volume(VOLUME)
        s.play()
    except:
        pass

# ===================== 桌宠主类 =====================
class BubuPet:
    def __init__(self, root):
        self.root = root
        set_window_icon(self.root)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", WIN_TOPMOST)
        self.root.attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.root.geometry(f"{PET_W}x{PET_H}+500+300")
        set_window_click_through(self.root)

        self.drag = False
        self.main_state = "static"
        self.cur_mood = "calm"
        self.cur_dir = random.choice(WALK_DIR_LIST)
        self.cur_frames = []
        self.frame_idx = 0
        self.state_start_time = time.time()
        
        self.sleep_gif_paths = []
        self.current_sleep_gif_idx = 0
        self.sleep_switch_timer = None
        
        self.volume_win = None
        self.size_win = None

        self.label = tk.Label(root, bg=TRANSPARENT_COLOR)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.label.bind("<ButtonPress-1>", self.on_press)
        self.label.bind("<B1-Motion>", self.on_move)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<Button-3>", self.show_menu)
        self.label.bind("<Enter>", self.show_pet)
        self.label.bind("<Leave>", self.check_edge_hide)

        # 右键菜单
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="🔄 切换皮肤", command=self.change_skin)
        self.menu.add_separator()
        self.menu.add_command(label="🔊 音量调节", command=self.open_volume_win)
        self.menu.add_command(label="📏 大小调节", command=self.open_size_win)
        self.menu.add_command(label="🔇 静音/取消静音", command=self.toggle_mute)
        self.menu.add_separator()
        self.menu.add_command(label="🤖 开启自动", command=self.open_auto)
        self.menu.add_command(label="🛑 关闭自动", command=self.close_auto)
        self.menu.add_separator()
        self.menu.add_command(label="😴 睡觉", command=self.set_sleep)
        self.menu.add_command(label="☀️ 叫醒", command=self.wake_up)
        self.menu.add_command(label="😊 随机情绪", command=self.random_mood)
        self.menu.add_separator()
        # ===================== 新增：作者信息菜单选项 =====================
        self.menu.add_command(label="📝 作者信息", command=self.show_author_info)
        # ================================================================
        self.menu.add_command(label="❌ 退出", command=self.quit_app)

        self.switch_to_mood("calm", force=True)
        self.anim_loop()
        self.ai_logic_loop()

    # ===================== 新增：作者信息弹窗函数 =====================
    def show_author_info(self):
        """点击弹出作者信息弹窗（替换成你自己的信息即可）"""
        author_win = tk.Toplevel(self.root)
        author_win.title("作者信息")
        author_win.geometry("350x220")
        author_win.resizable(False, False)
        author_win.attributes("-topmost", True)
        set_window_icon(author_win)

        # 窗口背景色
        author_win.configure(bg="#f8f9fa")

        # 标题
        tk.Label(
            author_win, text="布布一二桌宠", 
            font=("微软雅黑", 16, "bold"), bg="#f8f9fa", fg="#2c3e50"
        ).pack(pady=10)

        # 作者信息（在这里修改你的名字、抖音ID、简介）
        tk.Label(
            author_win, text="开发者（抖音昵称）：布布一二特效大王", 
            font=("微软雅黑", 12), bg="#f8f9fa"
        ).pack()
        tk.Label(
            author_win, text="抖音ID：38739236249", 
            font=("微软雅黑", 12), bg="#f8f9fa", fg="#c0392b"
        ).pack(pady=5)
        tk.Label(
            author_win, text="原创免费分享 · 禁止篡改搬运", 
            font=("微软雅黑", 10, "italic"), bg="#f8f9fa", fg="#7f8c8d"
        ).pack(pady=2)
        tk.Label(
            author_win, text="© 2025 版权所有 · 保留所有权利", 
            font=("微软雅黑", 9), bg="#f8f9fa", fg="#7f8c8d"
        ).pack(pady=5)

        # 关闭按钮
        tk.Button(
            author_win, text="确定", command=author_win.destroy,
            font=("微软雅黑", 10), width=10, bg="#3498db", fg="white"
        ).pack(pady=5)
    # ================================================================

    def can_switch_state(self, force=False):
        if force:
            return True
        elapsed_time = time.time() - self.state_start_time
        return elapsed_time >= MIN_DISPLAY_TIME

    def switch_to_mood(self, mood, force=False):
        if not self.can_switch_state(force):
            return
        old_mood = self.cur_mood
        self.main_state = "static"
        self.cur_mood = mood
        if old_mood != mood:
            play_sound(current_skin, mood)
        self.state_start_time = time.time()
        self.cur_frames = load_current_state_frames("static", mood)
        self.frame_idx = 0

    def switch_to_walk(self, direction, force=False):
        if not self.can_switch_state(force):
            return
        self.main_state = "walk"
        self.cur_dir = direction
        self.state_start_time = time.time()
        self.cur_frames = load_current_state_frames("walk", direction)
        self.frame_idx = 0

    def switch_to_sleep(self, force=False):
        if not self.can_switch_state(force):
            return
        self.main_state = "sleep"
        self.state_start_time = time.time()
        
        self.sleep_gif_paths = get_all_sleep_gif_paths()
        if not self.sleep_gif_paths:
            return
            
        self.current_sleep_gif_idx = 0
        self.cur_frames = load_single_gif(self.sleep_gif_paths[self.current_sleep_gif_idx])
        self.frame_idx = 0
        
        self.start_sleep_switch_timer()

    def start_sleep_switch_timer(self):
        if self.sleep_switch_timer:
            self.root.after_cancel(self.sleep_switch_timer)
        
        if self.main_state == "sleep" and len(self.sleep_gif_paths) > 1:
            self.sleep_switch_timer = self.root.after(SLEEP_IMAGE_INTERVAL, self.next_sleep_gif)

    def next_sleep_gif(self):
        if self.main_state != "sleep" or not self.sleep_gif_paths:
            return
            
        self.current_sleep_gif_idx = (self.current_sleep_gif_idx + 1) % len(self.sleep_gif_paths)
        self.cur_frames = load_single_gif(self.sleep_gif_paths[self.current_sleep_gif_idx])
        self.frame_idx = 0
        
        self.start_sleep_switch_timer()

    def stop_sleep_switch_timer(self):
        if self.sleep_switch_timer:
            self.root.after_cancel(self.sleep_switch_timer)
            self.sleep_switch_timer = None

    def anim_loop(self):
        if not APP_RUNNING:
            return
        try:
            if self.cur_frames:
                self.frame_idx = (self.frame_idx + 1) % len(self.cur_frames)
                self.label.config(image=self.cur_frames[self.frame_idx])
        except:
            pass
        self.root.after(GIF_INTERVAL, self.anim_loop)

    def on_press(self, e):
        self.drag = False
        self.click_x = e.x
        self.click_y = e.y
        self.show_pet()

    def on_move(self, e):
        dx = abs(e.x - self.click_x)
        dy = abs(e.y - self.click_y)
        if dx > 5 or dy > 5:
            self.drag = True
        if self.drag:
            x = self.root.winfo_x() + e.x - self.click_x
            y = self.root.winfo_y() + e.y - self.click_y
            sw = self.root.winfo_screenwidth()
            x = max(0, min(x, sw-PET_W))
            self.root.geometry(f"{PET_W}x{PET_H}+{x}+{y}")

    def on_release(self, e):
        if not self.drag:
            play_sound(current_skin, "click")
        self.check_edge_hide()

    def show_menu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def check_edge_hide(self, event=None):
        global IS_HIDDEN, ORIGINAL_X
        if self.main_state == "walk" or self.drag:
            return
        sw = self.root.winfo_screenwidth()
        x = self.root.winfo_x()
        if x <= HIDE_MARGIN:
            ORIGINAL_X = x
            self.root.geometry(f"{PET_W}x{PET_H}-{PET_W-5}+{self.root.winfo_y()}")
            IS_HIDDEN = True
        elif x >= sw - PET_W - 10:
            ORIGINAL_X = x
            self.root.geometry(f"{PET_W}x{PET_H}{sw-5}+{self.root.winfo_y()}")
            IS_HIDDEN = True

    def show_pet(self, event=None):
        global IS_HIDDEN, ORIGINAL_X
        if IS_HIDDEN:
            self.root.geometry(f"{PET_W}x{PET_H}+{ORIGINAL_X}+{self.root.winfo_y()}")
            IS_HIDDEN = False

    # ===================== 修复：音量调节窗口（点击外部自动关闭） =====================
    def open_volume_win(self):
        if self.volume_win and tk.Toplevel.winfo_exists(self.volume_win):
            self.volume_win.lift()
            return
        # 计算窗口位置（居中显示，不贴边）
        x = self.root.winfo_x() + (PET_W - 260) // 2
        y = self.root.winfo_y() - 90
        self.volume_win = tk.Toplevel(self.root)
        set_window_icon(self.volume_win)
        self.volume_win.overrideredirect(True)
        self.volume_win.attributes("-topmost", True)
        self.volume_win.geometry(f"260x70+{x}+{y}")
        self.volume_win.configure(bg="#e8e8e8")
        # 绑定：失去焦点（点击外部）自动关闭
        self.volume_win.bind("<FocusOut>", lambda e: self.volume_win.destroy())
        
        tk.Label(self.volume_win, text="音量调节", bg="#e8e8e8").pack(pady=2)
        self.vol_scale = tk.Scale(self.volume_win, from_=0, to=100, orient=tk.HORIZONTAL, length=200, showvalue=0)
        self.vol_scale.set(int(VOLUME*100))
        self.vol_scale.pack()
        self.vol_scale.config(command=lambda v: self.update_volume(v))
        tk.Button(self.volume_win, text="关闭", command=self.volume_win.destroy).place(x=210, y=35)
        # 自动获取焦点，保证点击外部能触发关闭
        self.volume_win.focus_set()

    # ===================== 修复：大小调节窗口（点击外部自动关闭） =====================
    def open_size_win(self):
        if self.size_win and tk.Toplevel.winfo_exists(self.size_win):
            self.size_win.lift()
            return
        # 计算窗口位置（居中显示，不贴边）
        x = self.root.winfo_x() + (PET_W - 260) // 2
        y = self.root.winfo_y() - 110
        self.size_win = tk.Toplevel(self.root)
        set_window_icon(self.size_win)
        self.size_win.overrideredirect(True)
        self.size_win.attributes("-topmost", True)
        self.size_win.geometry(f"260x90+{x}+{y}")
        self.size_win.configure(bg="#e8e8e8")
        # 绑定：失去焦点（点击外部）自动关闭
        self.size_win.bind("<FocusOut>", lambda e: self.size_win.destroy())
        
        tk.Label(self.size_win, text="大小调节", bg="#e8e8e8").pack(pady=2)
        self.size_scale = tk.Scale(self.size_win, from_=60, to=200, orient=tk.HORIZONTAL, length=200, showvalue=0)
        self.size_scale.set(PET_W)
        self.size_scale.pack()
        self.size_scale.bind("<ButtonRelease-1>", self.update_size_release)
        tk.Button(self.size_win, text="默认", command=self.reset_size).place(x=150, y=50)
        tk.Button(self.size_win, text="关闭", command=self.size_win.destroy).place(x=210, y=50)
        # 自动获取焦点，保证点击外部能触发关闭
        self.size_win.focus_set()

    def update_volume(self, val):
        global VOLUME
        VOLUME = int(val)/100

    def update_size_release(self, event):
        global PET_W, PET_H
        PET_W = int(self.size_scale.get())
        PET_H = PET_W
        self.refresh_size()

    def reset_size(self):
        global PET_W, PET_H
        PET_W, PET_H = 120, 120
        self.size_scale.set(PET_W)
        self.refresh_size()

    def refresh_size(self):
        try:
            if self.main_state == "static":
                self.cur_frames = load_current_state_frames("static", self.cur_mood)
            elif self.main_state == "walk":
                self.cur_frames = load_current_state_frames("walk", self.cur_dir)
            elif self.main_state == "sleep":
                if self.sleep_gif_paths and self.current_sleep_gif_idx < len(self.sleep_gif_paths):
                    self.cur_frames = load_single_gif(self.sleep_gif_paths[self.current_sleep_gif_idx])
            self.root.geometry(f"{PET_W}x{PET_H}+{self.root.winfo_x()}+{self.root.winfo_y()}")
        except:
            pass

    def change_skin(self):
        global current_skin
        idx = (SKIN_LIST.index(current_skin) + 1) % 3
        current_skin = SKIN_LIST[idx]
        play_sound(current_skin, "change_skin")
        if self.main_state == "sleep":
            self.stop_sleep_switch_timer()
            self.switch_to_sleep(force=True)
        else:
            self.switch_to_mood(self.cur_mood, force=True)

    def toggle_mute(self):
        global MUTE
        MUTE = not MUTE

    def open_auto(self):
        global auto_mode
        auto_mode = True

    def close_auto(self):
        global auto_mode
        auto_mode = False
        self.switch_to_mood("calm", force=True)

    def set_sleep(self):
        global is_sleep_lock, MUTE
        self.switch_to_sleep(force=True)
        MUTE = True
        is_sleep_lock = True

    def wake_up(self):
        global is_sleep_lock, MUTE
        is_sleep_lock = False
        MUTE = False
        self.stop_sleep_switch_timer()
        self.switch_to_mood("calm", force=True)

    def random_mood(self):
        if is_sleep_lock:
            return
        self.switch_to_mood(random.choice(MOOD_LIST), force=True)

    def ai_logic_loop(self):
        if not APP_RUNNING:
            return
        try:
            if is_sleep_lock:
                self.root.after(3000, self.ai_logic_loop)
                return

            if auto_mode and self.can_switch_state():
                r = random.random()
                if r < 0.35:
                    self.switch_to_mood(random.choice(MOOD_LIST))
                elif r < 0.7:
                    self.walk_move()
                else:
                    self.switch_to_sleep()
        except:
            pass
        self.root.after(3000, self.ai_logic_loop)

    def walk_move(self):
        try:
            if self.main_state != "walk" or not APP_RUNNING or is_sleep_lock:
                return
            sw = self.root.winfo_screenwidth()
            current_y = self.root.winfo_y()
            x = self.root.winfo_x()
            step = 3

            if self.cur_dir == "left":
                x -= step
            else:
                x += step

            if x < 10:
                self.cur_dir = "right"
                x = 10
            if x > sw - PET_W - 10:
                self.cur_dir = "left"
                x = sw - PET_W - 10

            self.root.geometry(f"{PET_W}x{PET_H}+{x}+{current_y}")

            if random.random() < 0.06 and self.can_switch_state():
                self.switch_to_mood(self.cur_mood)
        except:
            pass
        self.root.after(80, self.walk_move)

    def quit_app(self):
        global APP_RUNNING
        APP_RUNNING = False
        self.stop_sleep_switch_timer()
        self.root.destroy()
        self.root.master.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    set_window_icon(root)
    root.withdraw()
    app = BubuPet(tk.Toplevel(root))
    root.mainloop()