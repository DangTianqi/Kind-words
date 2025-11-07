import tkinter as tk
from tkinter import ttk, filedialog
import random
import time
import sys
import os
import pygame

messages = [
    "我想你了保持好心情", "梦想成真",
    "早点休息", "今天过得开心嘛", "好想见到你",
    "记得想我", "多喝水哦～", "好好爱自己",
    "记得吃水果", "顺顺利利", "期待下一次见面",
    "午饭要吃热乎的", "你超棒的！", "保持微笑呀",
    "别熬夜", "你已经做的很好啦", "天冷，多穿衣服",
    "愿今晚有个好梦", "明天见", "其实，我喜欢你",
    # 新增的消息内容
    "你是最特别的", "每一天都值得珍惜", "相信自己无限可能",
    "小小的幸福就在身边", "记得给自己一个拥抱", "世界因你而美丽",
    "保持那份纯真", "微笑是最好的语言", "心中有光，脚下有路",
    "累了就歇一歇", "你的努力会被看见", "简单生活，快乐自在",
    "每一天都是新的开始", "感恩遇见你", "做自己的太阳",
    "温柔对待这个世界", "坚持就是胜利", "爱笑的人运气不会差",
    "平凡日子里也有星光", "你是独一无二的存在", "慢慢来，比较快",
    "生活需要一点甜", "保持热爱奔赴山海", "一切都会越来越好",
    "小小的确幸大大的幸福", "记得对自己好一点", "阳光总在风雨后",
    "今天也要加油哦", "善良的人最美丽", "享受当下的美好",
    "你的存在让世界更美好", "坚持做自己喜欢的事", "简单就是幸福",
    "每一天都充满希望", "你是别人的一道光", "保持初心方得始终",
    "生活明朗万物可爱", "心怀感恩所遇皆美", "慢慢沉淀静静成长",
    "所有的美好都在路上", "愿你被温柔以待", "做最真实的自己",
    "今天也要开心呀", "未来可期不负韶华", "你值得所有的美好",
    "保持好奇探索世界", "小小的进步也是成长", "生活需要仪式感",
    "愿你眼里有光心里有爱", "平凡的日子也闪光", "做自己的英雄",
    "每一天都是礼物", "保持善良温暖他人", "简单的快乐最珍贵",
    "你是生活的艺术家", "慢慢来，你会更好的", "今天也要微笑呀",
    "坚持梦想终会实现", "生活因你而精彩", "小小的坚持大大的改变",
    "愿你心中有景花香满径", "做自己喜欢的样子", "每一天都是奇迹"
]


def resource_path(relative_path):
    """ 获取打包后资源的绝对路径 """
    try:
        # 当程序被打包后，PyInstaller会设置这个临时目录
        base_path = sys._MEIPASS
    except Exception:
        # 如果没有打包，就使用当前文件的目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class FloatingMessageApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.windows = []
        self.is_running = False
        self.control_win = None
        self.music_playing = False
        music_path = resource_path('阿冗 - 与我无关_[cut_68sec].mp3')
        self.current_music_file = music_path

        # 初始化音乐播放器
        self.init_music()

        # 创建控制窗口
        self.create_control_window()

        # 如果音乐可用且默认音乐文件存在，则自动播放
        if self.music_available and os.path.exists(self.current_music_file):
            self.play_selected_music()
    def init_music(self):
        """初始化音乐播放器"""
        try:
            pygame.mixer.init()
            self.music_available = True
        except:
            self.music_available = False
            print("警告：无法初始化音乐播放器")

    def select_music_file(self):
        """选择音乐文件"""
        if not self.music_available:
            self.status_var.set("❌ 音乐播放器不可用")
            return

        file_path = filedialog.askopenfilename(
            title="选择音乐文件",
            filetypes=[
                ("音乐文件", "*.mp3 *.wav *.ogg"),
                ("MP3文件", "*.mp3"),
                ("WAV文件", "*.wav"),
                ("OGG文件", "*.ogg"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            self.current_music_file = file_path
            self.status_var.set(f"🎵 已选择: {os.path.basename(file_path)}")

            # 自动播放选择的音乐
            self.play_selected_music()

    def play_selected_music(self):
        """播放选中的音乐文件"""
        if not self.music_available or not self.current_music_file:
            return

        try:
            pygame.mixer.music.load(self.current_music_file)
            pygame.mixer.music.play(loops=-1)  # 循环播放
            self.music_playing = True
            self.music_btn.config(text="⏸️ 暂停音乐")
            self.status_var.set("🎵 正在播放选择的音乐")
            print(f"正在播放: {os.path.basename(self.current_music_file)}")
        except Exception as e:
            print(f"无法播放音乐文件: {e}")
            self.status_var.set("❌ 无法播放选择的音乐文件")

    def stop_music(self):
        """停止音乐"""
        if self.music_available and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def get_random_color(self):
        colors = ['#FFB6C1', '#87CEFA', '#98FB98', '#FFFACD',
                  '#E6E6FA', '#FFE4E1', '#AFEEEE', '#FFDAB9',
                  '#FFEFD5', '#D8BFD8', '#F0FFF0', '#FFF0F5',
                  '#F5F5DC', '#FFE4B5', '#DDA0DD', '#B0E0E6',
                  '#FFD700', '#98F5FF', '#FFEC8B', '#FFBBFF']
        return random.choice(colors)

    def get_darker_color(self, color):
        """生成比原颜色稍暗的颜色"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # 生成稍暗的颜色
            darker_r = max(0, r - 30)
            darker_g = max(0, g - 30)
            darker_b = max(0, b - 30)

            return f'#{darker_r:02x}{darker_g:02x}{darker_b:02x}'
        else:
            return color

    def get_random_font(self):
        fonts = ['楷体', '微软雅黑', '宋体', '黑体', '华文行楷', '华文细黑', '仿宋']
        return random.choice(fonts)

    def on_control_window_close(self):
        """控制窗口关闭时的处理"""
        self.is_running = False  # 停止发送消息
        self.clear_all_windows()  # 清空所有消息窗口
        self.stop_music()  # 停止音乐

        # 销毁控制窗口和主窗口
        if self.control_win:
            self.control_win.destroy()
        self.root.destroy()

        # 完全退出程序
        sys.exit(0)

    def create_control_window(self):
        """创建控制窗口"""
        self.control_win = tk.Toplevel(self.root)
        self.control_win.title("💌 暖心消息小助手 💌")
        self.control_win.geometry("350x500")
        self.control_win.configure(bg='#FFF0F5')
        self.control_win.resizable(False, False)

        # 设置关闭窗口事件
        self.control_win.protocol("WM_DELETE_WINDOW", self.on_control_window_close)

        # 添加图标和标题
        header_frame = tk.Frame(self.control_win, bg='#FFF0F5')
        header_frame.pack(pady=15)

        title_label = tk.Label(header_frame, text="💌 暖心消息小助手 💌",
                               font=('微软雅黑', 18, 'bold'),
                               bg='#FFF0F5', fg='#FF1493')
        title_label.pack()

        subtitle_label = tk.Label(header_frame, text="让温暖的消息充满你的屏幕",
                                  font=('微软雅黑', 10),
                                  bg='#FFF0F5', fg='#888888')
        subtitle_label.pack(pady=(5, 0))

        # 控制按钮框架
        btn_frame = tk.Frame(self.control_win, bg='#FFF0F5')
        btn_frame.pack(pady=10)

        # 使用更漂亮的按钮样式
        button_style = {
            'font': ('微软雅黑', 12),
            'width': 15,
            'height': 1,
            'relief': 'raised',
            'bd': 2
        }

        start_btn = tk.Button(btn_frame, text="✨ 开始发送消息",
                              bg='#98FB98', fg='#2E8B57',
                              command=self.start_messages,
                              **button_style)
        start_btn.pack(pady=5)

        stop_btn = tk.Button(btn_frame, text="⏹️ 停止发送",
                             bg='#FFB6C1', fg='#8B4513',
                             command=self.stop_messages,
                             **button_style)
        stop_btn.pack(pady=5)

        clear_btn = tk.Button(btn_frame, text="🧹 清空所有消息",
                              bg='#87CEFA', fg='#1E90FF',
                              command=self.clear_all_windows_with_final_message,
                              **button_style)
        clear_btn.pack(pady=5)

        # 音乐控制按钮框架
        music_frame = tk.Frame(self.control_win, bg='#FFF0F5')
        music_frame.pack(pady=5)

        # 音乐控制按钮
        music_button_style = {
            'font': ('微软雅黑', 10),
            'width': 12,
            'height': 1,
            'relief': 'raised',
            'bd': 2
        }

        select_music_btn = tk.Button(music_frame, text="🎵 选择音乐",
                                     bg='#DDA0DD', fg='#4B0082',
                                     command=self.select_music_file,
                                     **music_button_style)
        select_music_btn.pack(side='left', padx=5)

        self.music_btn = tk.Button(music_frame, text="⏸️ 暂停音乐",
                                   bg='#FFD700', fg='#8B4513',
                                   command=self.toggle_music,
                                   **music_button_style)
        self.music_btn.pack(side='left', padx=5)

        # 设置框架
        settings_frame = tk.LabelFrame(self.control_win, text="⚙️ 设置",
                                       font=('微软雅黑', 11, 'bold'),
                                       bg='#FFF0F5', fg='#FF69B4')
        settings_frame.pack(pady=10, padx=25, fill='x')

        # 消息数量设置
        count_frame = tk.Frame(settings_frame, bg='#FFF0F5')
        count_frame.pack(pady=8, fill='x', padx=10)
        tk.Label(count_frame, text="消息数量:",
                 font=('微软雅黑', 10), bg='#FFF0F5', fg='#555555').pack(side='left')
        self.count_var = tk.StringVar(value="520")  # 改为520
        count_entry = tk.Entry(count_frame, textvariable=self.count_var,
                               width=8, font=('微软雅黑', 10),
                               justify='center', relief='sunken', bd=2)
        count_entry.pack(side='right')

        # 延迟设置
        delay_frame = tk.Frame(settings_frame, bg='#FFF0F5')
        delay_frame.pack(pady=8, fill='x', padx=10)
        tk.Label(delay_frame, text="延迟(ms):",
                 font=('微软雅黑', 10), bg='#FFF0F5', fg='#555555').pack(side='left')
        self.delay_var = tk.StringVar(value="72")  # 改为72
        delay_entry = tk.Entry(delay_frame, textvariable=self.delay_var,
                               width=8, font=('微软雅黑', 10),
                               justify='center', relief='sunken', bd=2)
        delay_entry.pack(side='right')

        # 消息预览
        preview_frame = tk.LabelFrame(self.control_win, text="📝 消息预览",
                                      font=('微软雅黑', 11, 'bold'),
                                      bg='#FFF0F5', fg='#FF69B4')
        preview_frame.pack(pady=10, padx=25, fill='both', expand=True)

        preview_text = tk.Text(preview_frame, height=6, width=35,
                               font=('微软雅黑', 9), wrap='word',
                               bg='#FFFFFF', fg='#333333',
                               relief='sunken', bd=2)
        scrollbar = tk.Scrollbar(preview_frame, orient='vertical', command=preview_text.yview)
        preview_text.configure(yscrollcommand=scrollbar.set)

        preview_text.pack(side='left', pady=5, padx=5, fill='both', expand=True)
        scrollbar.pack(side='right', fill='y', pady=5)

        # 添加示例消息到预览
        sample_messages = random.sample(messages, min(10, len(messages)))
        for msg in sample_messages:
            preview_text.insert('end', f"💫 {msg}\n")
        preview_text.config(state='disabled')

        # 状态显示
        self.status_var = tk.StringVar(value="🎯 准备就绪，点击开始发送温暖消息")
        status_label = tk.Label(self.control_win, textvariable=self.status_var,
                                font=('微软雅黑', 9), bg='#FFF0F5', fg='#FF69B4')
        status_label.pack(pady=10)

        # 底部信息
        info_label = tk.Label(self.control_win, text="💝 让每一天都充满温暖和惊喜",
                              font=('微软雅黑', 8), bg='#FFF0F5', fg='#888888')
        info_label.pack(side='bottom', pady=8)

    def toggle_music(self):
        """切换音乐播放状态"""
        if not self.music_available or not self.current_music_file:
            self.status_var.set("❌ 请先选择音乐文件")
            return

        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
            self.music_btn.config(text="▶️ 播放音乐")
            self.status_var.set("⏸️ 音乐已暂停")
        else:
            pygame.mixer.music.unpause()
            self.music_playing = True
            self.music_btn.config(text="⏸️ 暂停音乐")
            self.status_var.set("🎵 音乐播放中")

    def create_float_window(self):
        """创建浮动消息窗口"""
        if not self.is_running:
            return

        window = tk.Toplevel(self.root)
        window.overrideredirect(True)  # 无边框
        window.attributes('-topmost', True)  # 置顶
        window.attributes('-alpha', 0.0)  # 初始透明

        # 随机位置
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        x = random.randrange(0, width - 200)
        y = random.randrange(0, height - 100)
        window.geometry(f"+{x}+{y}")

        message = random.choice(messages)
        bg_color = self.get_random_color()
        darker_color = self.get_darker_color(bg_color)
        font_name = self.get_random_font()

        # 创建主框架 - 无边框
        main_frame = tk.Frame(window,
                              bg=bg_color,
                              relief='flat',
                              bd=0)
        main_frame.pack(fill='both', expand=True)

        # 创建菜单栏
        menu_bar = tk.Frame(main_frame,
                            bg=darker_color,
                            height=20)
        menu_bar.pack(fill='x', side='top')
        menu_bar.pack_propagate(False)  # 防止菜单栏被内容压缩

        # 添加菜单栏标题
        menu_title = tk.Label(menu_bar,
                              text="💌 暖心消息",
                              bg=darker_color,
                              fg='white',
                              font=('微软雅黑', 9))
        menu_title.pack(side='left', padx=5)

        # 添加关闭按钮
        close_btn = tk.Label(menu_bar,
                             text="✕",
                             bg=darker_color,
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             cursor='hand2')
        close_btn.pack(side='right', padx=5)
        close_btn.bind('<Button-1>', lambda e: self.fade_out(window))

        # 添加最小化按钮
        minimize_btn = tk.Label(menu_bar,
                                text="−",
                                bg=darker_color,
                                fg='white',
                                font=('Arial', 12, 'bold'),
                                cursor='hand2')
        minimize_btn.pack(side='right', padx=2)
        minimize_btn.bind('<Button-1>', lambda e: window.withdraw())

        # 添加菜单栏拖动功能
        def start_move(event):
            window.x = event.x
            window.y = event.y

        def do_move(event):
            deltax = event.x - window.x
            deltay = event.y - window.y
            x = window.winfo_x() + deltax
            y = window.winfo_y() + deltay
            window.geometry(f"+{x}+{y}")

        menu_bar.bind("<ButtonPress-1>", start_move)
        menu_bar.bind("<B1-Motion>", do_move)
        menu_title.bind("<ButtonPress-1>", start_move)
        menu_title.bind("<B1-Motion>", do_move)

        # 创建消息内容区域
        content_frame = tk.Frame(main_frame,
                                 bg=bg_color)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 创建标签 - 保持原始大小
        label = tk.Label(content_frame,
                         text=message,
                         bg=bg_color,
                         font=(font_name, 18),
                         width=15,
                         height=2)
        label.pack(expand=True)

        # 绑定点击事件关闭窗口
        label.bind('<Button-1>', lambda e: self.fade_out(window))
        content_frame.bind('<Button-1>', lambda e: self.fade_out(window))

        self.windows.append(window)

        # 动画效果
        self.fade_in(window)

        # 恢复原始消失时间 (8-12秒)
        auto_close_time = random.randint(8000, 12000)
        window.after(auto_close_time, lambda: self.fade_out(window))

    def create_final_message(self):
        """创建最终祝福消息"""
        window = tk.Toplevel(self.root)
        window.overrideredirect(True)  # 无边框
        window.attributes('-topmost', True)  # 置顶

        # 居中显示
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        window_width = 1600
        window_height = 800
        x = (width - window_width) // 2
        y = (height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 使用温馨的颜色
        bg_color = '#FFB6C1'  # 粉红色
        darker_color = self.get_darker_color(bg_color)

        # 创建主框架
        main_frame = tk.Frame(window,
                              bg=bg_color,
                              relief='flat',
                              bd=0)
        main_frame.pack(fill='both', expand=True)

        # 创建菜单栏
        menu_bar = tk.Frame(main_frame,
                            bg=darker_color,
                            height=25)
        menu_bar.pack(fill='x', side='top')
        menu_bar.pack_propagate(False)

        # 添加菜单栏标题
        menu_title = tk.Label(menu_bar,
                              text="💝 最后的话",
                              bg=darker_color,
                              fg='white',
                              font=('微软雅黑', 10, 'bold'))
        menu_title.pack(side='left', padx=8)

        # 创建消息内容区域
        content_frame = tk.Frame(main_frame,
                                 bg=bg_color)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 创建标签 - 大字体显示祝福语
        label = tk.Label(content_frame,
                         text="祝愿你天天开心！",
                         bg=bg_color,
                         font=('华文行楷', 72, 'bold'),
                         fg='#8B0000',  # 深红色
                         wraplength=800,
                         justify='center')
        label.pack(expand=True)

        # 添加一个装饰性边框
        decoration_frame = tk.Frame(content_frame,
                                    bg='#FF69B4',
                                    height=3)
        decoration_frame.pack(fill='x', side='bottom', pady=5)

        # 添加到窗口列表
        self.windows.append(window)

        # 直接显示，不需要淡入
        window.attributes('-alpha', 1.0)

        # 3秒后关闭程序
        window.after(3000, self.exit_program)

    def exit_program(self):
        """退出程序"""
        self.is_running = False
        self.clear_all_windows()
        self.stop_music()  # 停止音乐

        # 销毁控制窗口和主窗口
        if self.control_win:
            self.control_win.destroy()
        self.root.destroy()

        # 完全退出程序
        sys.exit(0)

    def fade_in(self, window):
        """淡入动画"""
        alpha = window.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            window.attributes('-alpha', alpha)
            window.after(30, lambda: self.fade_in(window))

    def fade_out(self, window):
        """淡出动画并关闭"""
        if window.winfo_exists():
            alpha = window.attributes('-alpha')
            if alpha > 0:
                alpha -= 0.1
                window.attributes('-alpha', alpha)
                window.after(30, lambda: self.fade_out(window))
            else:
                if window in self.windows:
                    self.windows.remove(window)
                window.destroy()

    def start_messages(self):
        """开始发送消息"""
        if self.is_running:
            return

        self.is_running = True
        self.status_var.set("🌟 正在发送暖心消息...")

        try:
            count = int(self.count_var.get())
            delay = int(self.delay_var.get())
        except ValueError:
            count = 520  # 默认值改为520
            delay = 72  # 默认值改为72

        self.create_windows_periodically(count, delay)

    def stop_messages(self):
        """停止发送消息"""
        self.is_running = False
        self.status_var.set("⏸️ 已停止发送消息")

    def clear_all_windows(self):
        """清空所有消息窗口"""
        for window in self.windows[:]:
            if window.winfo_exists():
                window.destroy()
        self.windows.clear()
        self.status_var.set("🧹 已清空所有消息")

    def clear_all_windows_with_final_message(self):
        """清空所有消息并显示最终祝福"""
        self.is_running = False  # 停止发送新消息
        self.clear_all_windows()  # 清空现有窗口
        self.status_var.set("💝 显示最终祝福...")

        # 创建最终祝福消息
        self.create_final_message()

    def create_windows_periodically(self, count, delay):
        """定期创建窗口"""
        if count > 0 and self.is_running:
            self.create_float_window()
            self.root.after(delay,
                            lambda: self.create_windows_periodically(count - 1, delay))
        elif count <= 0:
            self.status_var.set("✅ 消息发送完成")
            self.is_running = False

    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == '__main__':
    app = FloatingMessageApp()
    app.run()