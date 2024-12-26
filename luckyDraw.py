import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import csv
import os
from datetime import datetime

class LotteryScratchCard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("刮刮乐")
        self.root.geometry("600x800")

        # 设置浅绿色背景
        self.root.configure(bg='#e8f5e9')

        # 奖项设置(need to be change)
        self.prizes = {
            "特等奖 (100元)": 0.0,
            "一等奖 (50元)": 0.0,
            "二等奖 (20元)": 0.0,
            "三等奖 (10元)": 0.0,
            "四等奖 (2元)": 0.0,
            "再来一次": 0.0,
            "未中奖": 0.0
        }

        # 奖项对应的金额
        self.prize_values = {
            "特等奖 (100元)": 100,
            "一等奖 (50元)": 50,
            "二等奖 (20元)": 20,
            "三等奖 (10元)": 10,
            "四等奖 (2元)": 2,
            "再来一次": 0,
            "未中奖": 0
        }

        # 保底机制计数器
        self.consecutive_losses = 0
        self.guaranteed_win = 12  # 连续12次未中奖后保底

        # 刮开区域追踪
        self.scratch_matrix = None
        self.revealed = False
        self.canvas_width = 500
        self.canvas_height = 300
        self.matrix_scale = 1  # 每个像素一个计数单位

        # 财务指标
        self.total_income = 0
        self.total_payout = 0
        self.net_income = 0
        self.count = 0

        # CSV文件路径
        self.csv_file = "lottery_results.csv"
        self.initialize_csv()

        # 设置特等奖的最大发放次数
        self.max_grand_prizes = 5
        self.grand_prize_count = self.count_grand_prizes()

        # 如果达到特等奖的最大次数，移除特等奖
        if self.grand_prize_count >= self.max_grand_prizes:
            self.prizes.pop("特等奖 (100元)", None)
            messagebox.showinfo("通知", "特等奖已经达到最大发放次数，将不再发放。")
        else:
            # 如果还未达到，确保特等奖在奖项中
            if "特等奖 (100元)" not in self.prizes:
                self.prizes["特等奖 (100元)"] = 0.002

        # 防止中奖功能状态
        self.prevent_prizes = False  # 默认为关闭

        # 强制奖项队列
        self.forced_prizes = []

        # 创建主界面
        self.create_widgets()

        # 绑定按键
        self.root.bind('<space>', lambda event: self.start_new_game(charge=True))
        self.root.bind('p', self.toggle_prevent_prizes)
        self.root.bind('P', self.toggle_prevent_prizes)
        self.root.bind('2', lambda event: self.set_forced_prize("一等奖 (50元)"))
        self.root.bind('3', lambda event: self.set_forced_prize("二等奖 (20元)"))
        self.root.bind('0', self.reset_data)

    def initialize_csv(self):
        """初始化CSV文件，如果不存在则创建并写入表头。如果存在，确保表头包含必要的字段，并读取已有数据。"""
        headers = ["Timestamp", "Prize", "Income (元)", "Payout (元)", "Net Income (元)", "Grand Prize Count"]

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
        else:
            # 检查表头是否正确
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_headers = next(reader, None)
                if existing_headers != headers:
                    # 备份现有文件
                    backup_file = self.csv_file.replace(".csv", "_backup.csv")
                    os.rename(self.csv_file, backup_file)
                    messagebox.showwarning("警告", f"CSV文件头部不匹配。已备份原文件为 {backup_file}，并创建了新的CSV文件。")
                    # 创建新的CSV文件
                    with open(self.csv_file, mode='w', newline='', encoding='utf-8') as new_file:
                        writer = csv.writer(new_file)
                        writer.writerow(headers)

            # 读取已有数据
            self.read_financial_data()

    def read_financial_data(self):
        """读取CSV文件中的财务数据，累计收入、支出、净收入、游戏次数和特等奖发放次数。"""
        if os.path.exists(self.csv_file):
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        self.total_income = float(row['Income (元)'])
                        self.total_payout = float(row['Payout (元)'])
                        self.net_income = float(row['Net Income (元)'])
                        self.count = int(row['游戏次数']) if '游戏次数' in row else self.count
                        self.grand_prize_count = int(row['Grand Prize Count']) if 'Grand Prize Count' in row else self.grand_prize_count
                    except (ValueError, KeyError):
                        # 忽略格式错误的行
                        continue

    def count_grand_prizes(self):
        """读取CSV文件并计算特等奖已发放的次数。"""
        count = 0
        if os.path.exists(self.csv_file):
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('Prize') == "特等奖 (100元)":
                        count +=1
        return count

    def create_widgets(self):
        # 圣诞祝福语
        christmas_label = tk.Label(self.root,
                                   text="✧ Merry Christmas ✧",
                                   font=("Brush Script MT", 40, "italic"),
                                   fg='#c62828',  # 深红色文字
                                   bg='#e8f5e9')
        christmas_label.pack(pady=20)

        # 标题标签
        title_label = tk.Label(self.root, text="刮刮乐彩票",
                               font=("Arial", 32, "bold"),
                               fg='#1b5e20',  # 深绿色
                               bg='#e8f5e9')
        title_label.pack(pady=20)

        # 按钮框架
        button_frame = tk.Frame(self.root, bg='#e8f5e9')
        button_frame.pack(pady=20)

        # 开始按钮
        self.start_button = tk.Button(button_frame, text="开始新游戏 (空格)",
                                      command=lambda: self.start_new_game(charge=True),
                                      font=("Arial", 14, "bold"),
                                      bg='#43a047',  # 绿色按钮
                                      fg='black',
                                      relief=tk.FLAT,
                                      padx=15,
                                      pady=5,
                                      cursor="hand2")  # 添加手型光标
        self.start_button.pack(side=tk.LEFT, padx=20)

        # 一键刮开按钮
        self.reveal_button = tk.Button(button_frame, text="一键刮开",
                                       command=self.reveal_all,
                                       state=tk.DISABLED,
                                       font=("Arial", 14, "bold"),
                                       bg='#43a047',  # 绿色按钮
                                       fg='black',
                                       relief=tk.FLAT,
                                       padx=15,
                                       pady=5,
                                       cursor="hand2")  # 添加手型光标
        self.reveal_button.pack(side=tk.LEFT, padx=20)

        # 创建画布框架
        self.frame = tk.Frame(self.root, bg='#e8f5e9')
        self.frame.pack(pady=30)

        # 创建画布
        self.canvas = tk.Canvas(self.frame,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg='white',
                                relief=tk.FLAT,
                                bd=0,
                                cursor="crosshair")  # 添加十字光标
        self.canvas.pack()

        # 初始状态隐藏画布框架
        self.frame.pack_forget()

        # 显示连续未中奖次数
        self.counter_label = tk.Label(self.root,
                                      text=f"距离保底还剩次数: {self.guaranteed_win - self.consecutive_losses}",
                                      font=("Arial", 14),
                                      bg='#e8f5e9',
                                      fg='#0277bd')  # 蓝色文字
        self.counter_label.pack(pady=20)

        # # 显示防止中奖功能状态
        # self.prevent_label = tk.Label(self.root,
        #                               text=f"防止中奖功能: {'开启' if self.prevent_prizes else '关闭'}",
        #                               font=("Arial", 14),
        #                               bg='#e8f5e9',
        #                               fg='#0277bd')  # 蓝色文字
        # self.prevent_label.pack(pady=10)
        #
        # # 显示强制奖项队列
        # self.forced_label = tk.Label(self.root,
        #                               text=f"强制奖项队列: {self.forced_prizes}",
        #                               font=("Arial", 14),
        #                               bg='#e8f5e9',
        #                               fg='#0277bd')  # 蓝色文字
        # self.forced_label.pack(pady=10)

        # 添加按钮悬停效果
        self.setup_button_hover()

    def setup_button_hover(self):
        """设置按钮悬停效果"""

        def on_enter(e):
            e.widget['background'] = '#66bb6a'  # 更亮的绿色

        def on_leave(e):
            e.widget['background'] = '#43a047'  # 恢复原来的绿色

        for button in [self.start_button, self.reveal_button]:
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

    def toggle_prevent_prizes(self, event=None):
        """切换防止中奖功能的状态"""
        self.prevent_prizes = not self.prevent_prizes
        status = "开启" if self.prevent_prizes else "关闭"
        print(f"不中奖功能已{status}.")
        # self.prevent_label.config(text=f"防止中奖功能: {'开启' if self.prevent_prizes else '关闭'}")

    def set_forced_prize(self, prize):
        """设置强制奖项"""
        if prize not in ["一等奖 (50元)", "二等奖 (20元)"]:
            return
        self.forced_prizes.append(prize)
        print(f"已设置强制奖项: {prize}. 下一轮中将确保获得该奖项。")
        # self.forced_label.config(text=f"强制奖项队列: {self.forced_prizes}")

    def reset_data(self, event=None):
        """重置所有财务数据和CSV文件"""
        confirm = messagebox.askyesno("确认", "您确定要清除所有数据吗？这将删除现有的CSV文件并重置所有财务指标。")
        if confirm:
            if os.path.exists(self.csv_file):
                os.remove(self.csv_file)
            # 重新初始化CSV文件
            headers = ["Timestamp", "Prize", "Income (元)", "Payout (元)", "Net Income (元)", "Grand Prize Count"]
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            # 重置财务指标
            self.total_income = 0
            self.total_payout = 0
            self.net_income = 0
            self.count = 0
            self.grand_prize_count = 0
            # 重置强制奖项队列和防止中奖功能
            self.forced_prizes = []
            self.prevent_prizes = False
            # 更新界面标签
            self.counter_label.config(text=f"距离保底还剩次数: {self.guaranteed_win - self.consecutive_losses}")
            # self.prevent_label.config(text=f"防止中奖功能: {'开启' if self.prevent_prizes else '关闭'}")
            # self.forced_label.config(text=f"强制奖项队列: {self.forced_prizes}")
            print("所有数据已重置。")
            messagebox.showinfo("已重置", "所有数据已被清除并重置。")

    def start_new_game(self, charge=True):
        # 如果按钮被禁用，直接返回
        if str(self.start_button['state']) == 'disabled':
            return

        # 临时禁用按钮防止重复点击
        self.start_button.config(state=tk.DISABLED)

        if charge:
            # 增加收入
            self.total_income += 5
            self.update_financial_metrics()

        # 重置刮开区域追踪
        self.scratch_matrix = np.zeros((self.canvas_height // self.matrix_scale,
                                        self.canvas_width // self.matrix_scale))
        self.revealed = False

        # 显示画布框架
        self.frame.pack(pady=30)
        self.canvas.delete("all")

        # 启用一键刮开按钮
        self.reveal_button.config(state=tk.NORMAL)

        # 决定中奖结果
        self.current_prize = self.determine_prize()

        # 创建奖项文字
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                text=self.current_prize,
                                font=("Arial", 36, "bold"),
                                fill="#d32f2f" if "奖" in self.current_prize else "#455a64",  # 中奖红色，未中奖深灰色
                                tags="prize")

        # 创建灰色覆盖层（使用多个小矩形）
        self.create_scratch_layer()

        # 绑定鼠标事件
        self.canvas.bind("<B1-Motion>", self.scratch)
        self.canvas.bind("<Button-1>", self.scratch)  # 添加点击事件

        # 如果中奖为“再来一次”，自动启动免费游戏
        if self.current_prize == "再来一次" and charge:
            # 延迟启动免费游戏，避免界面更新冲突
            self.root.after(1000, lambda: self.start_new_game(charge=False))

        # 重新启用开始按钮
        self.root.after(500, lambda: self.start_button.config(state=tk.NORMAL))

    def reveal_all(self):
        # 如果按钮被禁用，直接返回
        if str(self.reveal_button['state']) == 'disabled':
            return

        # 删除所有灰色覆盖层
        self.canvas.delete("scratch")
        self.revealed = True
        # 禁用一键刮开按钮
        self.reveal_button.config(state=tk.DISABLED)

    def create_scratch_layer(self):
        # 使用小矩形创建覆盖层
        rect_size = 12  # 减小矩形尺寸以提高刮开的平滑度
        for x in range(0, self.canvas_width, rect_size):
            for y in range(0, self.canvas_height, rect_size):
                self.canvas.create_rectangle(x, y, x + rect_size, y + rect_size,
                                             fill='#9e9e9e',  # 中灰色
                                             outline='#9e9e9e',
                                             tags="scratch")

    def determine_prize(self):
        # 检查是否需要保底
        if self.consecutive_losses >= self.guaranteed_win:
            self.consecutive_losses = 0
            prize = "二等奖 (20元)"
            self.update_payout(prize)
            self.log_result(prize)
            return prize

        # 检查是否有强制奖项
        if self.forced_prizes:
            prize = self.forced_prizes.pop(0)
            # self.forced_label.config(text=f"强制奖项队列: {self.forced_prizes}")
            print(f"强制奖项已触发: {prize}.")
            # 更新连续未中奖计数器
            if prize in ["特等奖 (100元)", "一等奖 (50元)", "二等奖 (20元)"]:
                self.consecutive_losses = 0
            else:
                self.consecutive_losses += 1

            self.counter_label.config(text=f"距离保底还剩次数: {self.guaranteed_win - self.consecutive_losses}")

            # 更新支出
            self.update_payout(prize)

            # 记录结果
            self.log_result(prize)

            # 如果发放的是特等奖，检查是否达到最大次数
            if prize == "特等奖 (100元)":
                self.grand_prize_count +=1
                if self.grand_prize_count >= self.max_grand_prizes:
                    self.prizes.pop("特等奖 (100元)", None)
                    messagebox.showinfo("通知", "特等奖已经达到最大发放次数，将不再发放。")

            return prize

        if self.prevent_prizes:
            # 防止中奖模式下，只能未中奖，除非达到保底
            prize = "未中奖"
            self.consecutive_losses += 1
            self.counter_label.config(text=f"距离保底还剩次数: {self.guaranteed_win - self.consecutive_losses}")

            # 更新支出
            self.update_payout(prize)

            # 记录结果
            self.log_result(prize)

            return prize

        # 随机抽取奖项
        rand_num = random.random()
        cumulative_prob = 0

        for prize, prob in self.prizes.items():
            cumulative_prob += prob
            if rand_num <= cumulative_prob:
                if prize == "再来一次":
                    self.log_result(prize)
                    return prize

                # 更新连续未中奖计数器
                if prize in ["特等奖 (100元)", "一等奖 (50元)", "二等奖 (20元)"]:
                    self.consecutive_losses = 0
                else:
                    self.consecutive_losses += 1

                self.counter_label.config(text=f"距离保底还剩次数: {self.guaranteed_win - self.consecutive_losses}")

                # 更新支出
                self.update_payout(prize)

                # 记录结果
                self.log_result(prize)

                # 如果发放的是特等奖，检查是否达到最大次数
                if prize == "特等奖 (100元)":
                    self.grand_prize_count +=1
                    if self.grand_prize_count >= self.max_grand_prizes:
                        self.prizes.pop("特等奖 (100元)", None)
                        messagebox.showinfo("通知", "特等奖已经达到最大发放次数，将不再发放。")

                return prize

        # 默认返回"未中奖"
        self.log_result("未中奖")
        return "未中奖"

    def update_payout(self, prize):
        """根据奖项更新总支出。"""
        payout = self.prize_values.get(prize, 0)
        self.total_payout += payout
        self.update_financial_metrics()
        self.count += 1

    def update_financial_metrics(self):
        """计算净收入并打印财务指标。"""
        self.net_income = self.total_income - self.total_payout
        print(f"收入 (Income): {self.total_income} 元")
        print(f"支出 (Payout): {self.total_payout} 元")
        print(f"净收入 (Net Income): {self.net_income} 元")
        print(f"游戏次数 (Count): {self.count}")
        print(f"特等奖已发放次数 (Grand Prize Count): {self.grand_prize_count}")
        print(f"防止中奖功能状态: {'开启' if self.prevent_prizes else '关闭'}")
        print(f"强制奖项队列: {self.forced_prizes}")
        print("-" * 40)

    def log_result(self, prize):
        """将彩票结果记录到CSV文件。"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payout = self.prize_values.get(prize, 0)
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, prize, self.total_income, payout, self.net_income, self.grand_prize_count])

    def scratch(self, event):
        # 获取鼠标位置
        x, y = event.x, event.y
        r = 25  # 增大刮开半径

        # 找到并删除该区域内的所有小矩形
        overlapping = self.canvas.find_overlapping(x - r, y - r, x + r, y + r)
        for item in overlapping:
            if "scratch" in self.canvas.gettags(item):
                self.canvas.delete(item)

        # 更新刮开区域矩阵
        matrix_x = min(y // self.matrix_scale, self.scratch_matrix.shape[0] - 1)
        matrix_y = min(x // self.matrix_scale, self.scratch_matrix.shape[1] - 1)

        # 将周围的点也标记为已刮开
        for dx in range(-2, 3):  # 扩大影响范围
            for dy in range(-2, 3):
                new_x = int(matrix_x + dx)
                new_y = int(matrix_y + dy)
                if (0 <= new_x < self.scratch_matrix.shape[0] and
                        0 <= new_y < self.scratch_matrix.shape[1]):
                    self.scratch_matrix[new_x, new_y] = 1

        # 检查刮开面积
        scratched_percentage = np.sum(self.scratch_matrix) / self.scratch_matrix.size
        if scratched_percentage > 0.3 and not self.revealed:
            self.revealed = True
            # 禁用一键刮开按钮
            self.reveal_button.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LotteryScratchCard()
    app.run()
