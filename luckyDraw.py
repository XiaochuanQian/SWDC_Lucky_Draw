import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import csv
import os
from datetime import datetime

class CyberLuckyDraw:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber Lucky Draw")
        self.root.geometry("700x900")
        self.root.configure(bg='#e8f5e9')  # Light green Christmas background

        # ==================== Pools Definition ====================
        # 5-yuan Pool
        self.prizes_5 = {
            "🎁 Special Prize (100 RMB)": 0.0,
            "🎄 First Prize (50 RMB)": 0.0,
            "🎅 Second Prize (20 RMB)": 0.0,
            "❄️ Third Prize (10 RMB)": 0.0,
            "☃️ Fourth Prize (0 RMB)": 0.0,
            "🎉 Try Again": 0.0,
            "🔔 No Prize": 0.0
        }

        # 20-yuan Pool - Updated as per user request
        self.prizes_20 = {
            "🎁 Special Prize (500 RMB)": 0.0,
            "🎄 First Prize (200 RMB)": 0.0,
            "🎅 Second Prize (50 RMB)": 0.0,
            "❄️ Third Prize (30 RMB)": 0.0,
            "☃️ Fourth Prize (Coke 2 RMB)": 0.0,
            "🎉 Try Again": 0.0,
            "🔔 No Prize": 0.0
        }

        # ==================== Tracking Variables ====================
        self.canvas_width = 500
        self.canvas_height = 300
        self.matrix_scale = 1

        self.scratch_matrix = None
        self.revealed = False

        # Current pool info
        self.current_pool = None   # "5-yuan" or "20-yuan"
        self.current_prizes_dict = {}  # Will hold the dictionary of the chosen pool

        # Financial Stats
        self.total_income_5 = 0   # Total income from 5-yuan
        self.total_payout_5 = 0   # Total payout from 5-yuan (excluding "Fourth Prize")
        self.net_income_5 = 0      # Net income from 5-yuan

        self.total_income_20 = 0  # Total income from 20-yuan
        self.total_payout_20 = 0  # Total payout from 20-yuan (excluding "Fourth Prize")
        self.net_income_20 = 0     # Net income from 20-yuan

        # Overall
        self.game_count = 0  # Total draws across both pools

        # Allowed plays for each pool
        self.allowed_plays_5 = 0
        self.allowed_plays_20 = 0

        # "Try Again" free plays counter
        self.free_games = 0

        # Prize counts for each pool
        self.prize_counts_5 = {
            "🎁 Special Prize (100 RMB)": 0,
            "🎄 First Prize (50 RMB)": 0,
            "🎅 Second Prize (20 RMB)": 0,
            "❄️ Third Prize (10 RMB)": 0,
            "☃️ Fourth Prize (0 RMB)": 0,
            "🎉 Try Again": 0,
            "🔔 No Prize": 0
        }

        self.prize_counts_20 = {
            "🎁 Special Prize (500 RMB)": 0,
            "🎄 First Prize (200 RMB)": 0,
            "🎅 Second Prize (50 RMB)": 0,
            "❄️ Third Prize (30 RMB)": 0,
            "☃️ Fourth Prize (Coke 2 RMB)": 0,
            "🎉 Try Again": 0,
            "🔔 No Prize": 0
        }

        # CSV file for logging all results
        self.csv_file = "cyber_lucky_draw_results.csv"
        self.initialize_csv()

        # ==================== Create UI ====================
        self.create_widgets()

        # Key bindings
        self.root.bind('<space>', lambda event: self.start_new_game())
        self.root.bind('<r>', lambda event: self.reveal_all())

    def initialize_csv(self):
        """Create CSV if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Adding a "PoolType" column to differentiate 5-yuan or 20-yuan
                writer.writerow(["Timestamp", "PoolType", "Prize", "Income (RMB)", "Payout (RMB)", "Net Income (RMB)"])

    def create_widgets(self):
        """
        Create Tkinter UI layout
        """
        # ==================== Christmas Greeting ====================
        greeting = tk.Label(self.root,
                            text="🎄❄️ Merry Christmas! ❄️🎄\n🎅🎁 Wishing You Good Luck! 🎁🎅",
                            font=("Brush Script MT", 24, "italic"),
                            fg='#c62828',
                            bg='#e8f5e9')
        greeting.pack(pady=15)

        # ===================== Title =====================
        title = tk.Label(self.root,
                         text="Cyber Lucky Draw",
                         font=("Arial", 24, "bold"),
                         fg='#1b5e20',
                         bg='#e8f5e9')
        title.pack(pady=10)

        # ===================== Pool Selection Buttons =====================
        pool_selection_frame = tk.Frame(self.root, bg='#e8f5e9')
        pool_selection_frame.pack(pady=10)

        self.select_5_button = tk.Button(pool_selection_frame,
                                         text="Choose 5-yuan Pool",
                                         font=("Arial", 14, "bold"),
                                         bg='#fdd835',
                                         fg='black',
                                         relief=tk.FLAT,
                                         padx=15,
                                         pady=5,
                                         cursor="hand2",
                                         command=lambda: self.select_pool("5-yuan"))
        self.select_5_button.pack(side=tk.LEFT, padx=10)

        self.select_20_button = tk.Button(pool_selection_frame,
                                          text="Choose 20-yuan Pool",
                                          font=("Arial", 14, "bold"),
                                          bg='#fdd835',
                                          fg='black',
                                          relief=tk.FLAT,
                                          padx=15,
                                          pady=5,
                                          cursor="hand2",
                                          command=lambda: self.select_pool("20-yuan"))
        self.select_20_button.pack(side=tk.LEFT, padx=10)

        # ===================== Set Plays Buttons =====================
        self.set_play_frame = tk.Frame(self.root, bg='#e8f5e9')
        self.set_play_frame.pack(pady=10)
        self.set_play_frame.pack_forget()  # Hide initially

        self.set_play_label = tk.Label(self.set_play_frame, text="Number of Plays:", font=("Arial", 12), bg='#e8f5e9')
        self.set_play_label.pack(side=tk.LEFT, padx=10)

        self.set_play_entry = tk.Entry(self.set_play_frame, font=("Arial", 14))
        self.set_play_entry.pack(side=tk.LEFT, padx=10)

        self.set_play_confirm_btn = tk.Button(self.set_play_frame,
                                              text="Confirm",
                                              font=("Arial", 12, "bold"),
                                              bg='#43a047',
                                              fg='black',
                                              relief=tk.FLAT,
                                              padx=10,
                                              pady=5,
                                              cursor="hand2",
                                              command=self.confirm_set_plays)
        self.set_play_confirm_btn.pack(side=tk.LEFT, padx=10)

        # ===================== Action Buttons =====================
        self.action_frame = tk.Frame(self.root, bg='#e8f5e9')
        self.action_frame.pack(pady=10)
        self.action_frame.pack_forget()  # Hide initially

        self.start_button = tk.Button(self.action_frame,
                                      text="Start New Game (Space)",
                                      font=("Arial", 14, "bold"),
                                      bg='#43a047',
                                      fg='black',
                                      relief=tk.FLAT,
                                      padx=15,
                                      pady=5,
                                      cursor="hand2",
                                      state=tk.DISABLED,
                                      command=self.start_new_game)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reveal_button = tk.Button(self.action_frame,
                                       text="Reveal All (R)",
                                       font=("Arial", 14, "bold"),
                                       bg='#43a047',
                                       fg='black',
                                       relief=tk.FLAT,
                                       padx=15,
                                       pady=5,
                                       cursor="hand2",
                                       state=tk.DISABLED,
                                       command=self.reveal_all)
        self.reveal_button.pack(side=tk.LEFT, padx=10)

        # ===================== Canvas =====================
        self.frame = tk.Frame(self.root, bg='#e8f5e9')
        self.frame.pack(pady=10)
        self.canvas = tk.Canvas(self.frame,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg='white',
                                relief=tk.FLAT,
                                bd=0,
                                cursor="crosshair")
        self.canvas.pack()
        self.frame.pack_forget()  # Hide initially

        # ===================== Information Area =====================
        info_frame = tk.Frame(self.root, bg='#e8f5e9')
        info_frame.pack(pady=10)

        self.game_count_label = tk.Label(info_frame,
                                         text="Total Draws: 0",
                                         font=("Arial", 14),
                                         bg='#e8f5e9',
                                         fg='#0277bd')
        self.game_count_label.pack(side=tk.LEFT, padx=10)

        # Shows current pool if selected
        self.current_pool_label = tk.Label(self.root,
                                           text="No Pool Selected",
                                           font=("Arial", 14),
                                           bg='#e8f5e9',
                                           fg='#0277bd')
        self.current_pool_label.pack(pady=5)

        # ===================== Admin Button =====================
        self.admin_button = tk.Button(self.root,
                                      text="Admin Panel",
                                      font=("Arial", 12, "bold"),
                                      bg='#f9a825',
                                      fg='black',
                                      relief=tk.FLAT,
                                      padx=10,
                                      pady=5,
                                      cursor="hand2",
                                      command=self.show_admin_login_dialog)
        self.admin_button.place(x=600, y=10)

        # ===================== Hover Effects =====================
        self.setup_button_hover()

        # ===================== Initialize Button States =====================
        self.update_start_button_state()

    def setup_button_hover(self):
        """Set hover colors for buttons"""
        def on_enter(e):
            e.widget['background'] = '#66bb6a'

        def on_leave(e):
            # Distinguish by original color
            w = e.widget
            if w in [self.select_5_button, self.select_20_button]:
                w['background'] = '#fdd835'
            elif w in [self.start_button, self.reveal_button, self.set_play_confirm_btn]:
                w['background'] = '#43a047'
            elif w == self.admin_button:
                w['background'] = '#f9a825'

        all_buttons = [
            self.select_5_button, self.select_20_button,
            self.start_button, self.reveal_button,
            self.set_play_confirm_btn,
            self.admin_button
        ]
        for b in all_buttons:
            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)

    # ==================== Pool Selection ====================
    def select_pool(self, pool_type):
        """Choose which pool to use next."""
        if pool_type == "5-yuan":
            self.current_pool = "5-yuan"
            self.current_prizes_dict = self.prizes_5
            self.current_pool_label.config(text="Current Pool: 5-yuan")
        else:
            self.current_pool = "20-yuan"
            self.current_prizes_dict = self.prizes_20
            self.current_pool_label.config(text="Current Pool: 20-yuan")

        # Show set plays frame
        self.set_play_frame.pack(pady=10)

        # Hide other frames
        self.action_frame.pack_forget()
        self.frame.pack_forget()

        # Clear previous set plays entry
        self.set_play_entry.delete(0, tk.END)

    def confirm_set_plays(self):
        """Confirm the number of plays set by the user."""
        val = self.set_play_entry.get()
        try:
            val = int(val)
        except ValueError:
            messagebox.showerror("Error", "Please input a valid number!")
            return
        if val <= 0:
            messagebox.showerror("Error", "Number of plays must be positive!")
        else:
            if self.current_pool == "5-yuan":
                self.allowed_plays_5 = val
            else:
                self.allowed_plays_20 = val
            # Hide set plays frame
            self.set_play_frame.pack_forget()
            # Show action buttons
            self.action_frame.pack(pady=10)
            # Enable start button
            self.update_start_button_state()

    def update_start_button_state(self):
        """Enable 'Start' if the selected pool has available plays or free games."""
        if self.current_pool == "5-yuan":
            if self.allowed_plays_5 > 0 or self.free_games > 0:
                self.start_button.config(state=tk.NORMAL)
                self.current_pool_label.config(text=f"Current Pool: 5-yuan")
            else:
                self.start_button.config(state=tk.DISABLED)
        elif self.current_pool == "20-yuan":
            if self.allowed_plays_20 > 0 or self.free_games > 0:
                self.start_button.config(state=tk.NORMAL)
                self.current_pool_label.config(text=f"Current Pool: 20-yuan")
            else:
                self.start_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.DISABLED)

    # ==================== Start Game & Reveal ====================
    def start_new_game(self):
        """Start a new draw from the selected pool, if possible."""
        if not self.current_pool:
            messagebox.showwarning("Warning", "Please select a pool first!")
            return

        # Determine if the game is free
        if self.free_games > 0:
            charge = False
            self.free_games -= 1
        else:
            charge = True

        # Check plays
        if self.current_pool == "5-yuan":
            if self.allowed_plays_5 <= 0 and charge:
                messagebox.showwarning("Warning", "No remaining plays for 5-yuan pool!")
                return
        else:
            if self.allowed_plays_20 <= 0 and charge:
                messagebox.showwarning("Warning", "No remaining plays for 20-yuan pool!")
                return

        # Temporarily disable start button to prevent multiple clicks
        if str(self.start_button['state']) == 'disabled':
            return
        self.start_button.config(state=tk.DISABLED)

        # Charge
        if charge:
            if self.current_pool == "5-yuan":
                self.total_income_5 += 5
                self.allowed_plays_5 -= 1
            else:
                self.total_income_20 += 20
                self.allowed_plays_20 -= 1

        # Reset scratch tracking
        self.scratch_matrix = np.zeros((self.canvas_height // self.matrix_scale,
                                        self.canvas_width // self.matrix_scale))
        self.revealed = False

        # Show canvas
        self.frame.pack(pady=10)
        self.canvas.delete("all")

        # Enable reveal button
        self.reveal_button.config(state=tk.NORMAL)

        # Determine prize
        self.current_prize = self.determine_prize()

        # Draw prize text
        self.canvas.create_text(self.canvas_width // 2,
                                self.canvas_height // 2,
                                text=self.current_prize,
                                font=("Arial", 36, "bold"),
                                fill="#d32f2f" if ("Prize" in self.current_prize) else "#455a64",
                                tags="prize")

        # Create scratch layer
        self.create_scratch_layer()

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.scratch)
        self.canvas.bind("<Button-1>", self.scratch)

        # If out of plays after this game, show summary
        if self.current_pool == "5-yuan":
            if self.allowed_plays_5 == 0 and self.free_games == 0:
                self.show_session_summary_popup(pool="5-yuan")
        else:
            if self.allowed_plays_20 == 0 and self.free_games == 0:
                self.show_session_summary_popup(pool="20-yuan")

        # Re-enable start button after short delay
        self.root.after(500, self.update_start_button_state)

    def reveal_all(self):
        """Reveal all scratch area."""
        if str(self.reveal_button['state']) == 'disabled':
            return

        # Delete all scratch overlays
        self.canvas.delete("scratch")
        self.revealed = True
        self.reveal_button.config(state=tk.DISABLED)

    def create_scratch_layer(self):
        """Use small rectangles to create scratch effect."""
        rect_size = 12
        for x in range(0, self.canvas_width, rect_size):
            for y in range(0, self.canvas_height, rect_size):
                self.canvas.create_rectangle(x, y, x + rect_size, y + rect_size,
                                             fill='#9e9e9e',
                                             outline='#9e9e9e',
                                             tags="scratch")

    def scratch(self, event):
        """Handle mouse scratching."""
        x, y = event.x, event.y
        r = 25
        overlapping = self.canvas.find_overlapping(x - r, y - r, x + r, y + r)
        for item in overlapping:
            if "scratch" in self.canvas.gettags(item):
                self.canvas.delete(item)

        # Update scratch matrix
        mx = min(y // self.matrix_scale, self.scratch_matrix.shape[0] - 1)
        my = min(x // self.matrix_scale, self.scratch_matrix.shape[1] - 1)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx = mx + dx
                ny = my + dy
                if 0 <= nx < self.scratch_matrix.shape[0] and 0 <= ny < self.scratch_matrix.shape[1]:
                    self.scratch_matrix[nx, ny] = 1

        # Calculate scratched percentage
        scratched_percentage = np.sum(self.scratch_matrix) / self.scratch_matrix.size
        if scratched_percentage > 0.3 and not self.revealed:
            self.revealed = True
            self.reveal_button.config(state=tk.DISABLED)

    # ==================== Determine Prize ====================
    def determine_prize(self):
        """
        Randomly select a prize from the current pool (5-yuan or 20-yuan).
        If the prize is "Try Again", grant a free game.
        """
        rand_num = random.random()
        cumulative = 0
        for prize, prob in self.current_prizes_dict.items():
            cumulative += prob
            if rand_num <= cumulative:
                if prize == "🎉 Try Again":
                    self.free_games += 1
                self.update_financials(prize)
                self.log_result(prize)
                self.game_count += 1
                self.game_count_label.config(text=f"Total Draws: {self.game_count}")
                return prize
        return "🔔 No Prize"

    # ==================== Update Payout & Net ====================
    def update_financials(self, prize):
        """
        Update total payout & net for the chosen pool.
        The 'Fourth Prize', 'Try Again', and 'No Prize' have no payout.
        """
        payout = 0

        # Determine payout based on prize and pool
        if self.current_pool == "5-yuan":
            if "100 RMB" in prize:
                payout = 100
            elif "50 RMB" in prize:
                payout = 50
            elif "20 RMB" in prize:
                payout = 20
            elif "10 RMB" in prize:
                payout = 10
            # 'Fourth Prize (0 RMB)', 'Try Again', 'No Prize' have no payout
            self.total_payout_5 += payout
            self.net_income_5 = self.total_income_5 - self.total_payout_5
        else:
            # 20-yuan pool with English prize names
            if "500 RMB" in prize:
                payout = 500
            elif "200 RMB" in prize:
                payout = 200
            elif "50 RMB" in prize:
                payout = 50
            elif "30 RMB" in prize:
                payout = 30
            # 'Fourth Prize (Coke 2 RMB)', 'Try Again', 'No Prize' have no payout
            self.total_payout_20 += payout
            self.net_income_20 = self.total_income_20 - self.total_payout_20

    # ==================== CSV Logging ====================
    def log_result(self, prize):
        """
        Record the draw result into CSV with PoolType, Prize, Income, Payout, Net
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine income & net based on pool
        if self.current_pool == "5-yuan":
            income = self.total_income_5
            net = self.net_income_5
            # Determine payout for this prize
            if "100 RMB" in prize:
                payout = 100
            elif "50 RMB" in prize:
                payout = 50
            elif "20 RMB" in prize:
                payout = 20
            elif "10 RMB" in prize:
                payout = 10
            else:
                payout = 0
        else:
            income = self.total_income_20
            net = self.net_income_20
            if "500 RMB" in prize:
                payout = 500
            elif "200 RMB" in prize:
                payout = 200
            elif "50 RMB" in prize:
                payout = 50
            elif "30 RMB" in prize:
                payout = 30
            else:
                payout = 0

        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                self.current_pool,
                prize,
                income,
                payout,
                net
            ])

        # Update prize counts
        if self.current_pool == "5-yuan":
            if prize in self.prize_counts_5:
                self.prize_counts_5[prize] += 1
        else:
            if prize in self.prize_counts_20:
                self.prize_counts_20[prize] += 1

    # ==================== Session Summary Popup ====================
    def show_session_summary_popup(self, pool):
        """
        Show popup when the chosen pool's plays are finished.
        Display the count of each prize won in that session.
        """
        popup = tk.Toplevel(self.root)
        popup.title(f"{pool} Session Summary")
        popup.geometry("350x500")
        popup.config(bg="#fafafa")

        # Christmas Decoration
        decoration_label = tk.Label(popup,
                                    text=f"🎄🎉 {pool} Session Results 🎉🎄",
                                    font=("Arial", 16, "bold"),
                                    bg="#fafafa",
                                    fg='#d32f2f')
        decoration_label.pack(pady=10)

        # Retrieve the appropriate prize counts
        if pool == "5-yuan":
            prize_counts = self.prize_counts_5
        else:
            prize_counts = self.prize_counts_20

        # Construct summary string
        summary_text = ""
        for prize, count in prize_counts.items():
            summary_text += f"{prize}: {count}\n"

        # Display the summary
        text_label = tk.Label(popup,
                              text=summary_text.strip(),
                              font=("Arial", 12),
                              bg="#fafafa",
                              justify=tk.LEFT)
        text_label.pack(pady=10)

        # Add Christmas Snowflakes or Symbols
        snow_label = tk.Label(popup,
                              text="❄️❄️❄️",
                              font=("Arial", 24),
                              bg="#fafafa")
        snow_label.pack(pady=10)

        # Close Button
        close_btn = tk.Button(popup,
                              text="Close",
                              font=("Arial", 12, "bold"),
                              bg='#43a047',
                              fg='black',
                              relief=tk.FLAT,
                              padx=10,
                              pady=5,
                              cursor="hand2",
                              command=lambda: self.close_session_summary(popup, pool))
        close_btn.pack(pady=20)

    def close_session_summary(self, popup, pool):
        """Close the summary popup and reset prize counts for the session."""
        popup.destroy()
        if pool == "5-yuan":
            for k in self.prize_counts_5:
                self.prize_counts_5[k] = 0
        else:
            for k in self.prize_counts_20:
                self.prize_counts_20[k] = 0

    # ==================== Admin Panel ====================
    def show_admin_login_dialog(self):
        """Admin entry: enter password to access admin panel"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("300x200")
        dialog.config(bg="#fff8e1")

        label = tk.Label(dialog, text="Enter admin password:", bg="#fff8e1", font=("Arial", 12))
        label.pack(pady=20)

        password_entry = tk.Entry(dialog, show="*", font=("Arial", 14))
        password_entry.pack(pady=10)

        confirm_button = tk.Button(dialog,
                                   text="Confirm",
                                   font=("Arial", 12, "bold"),
                                   bg='#43a047',
                                   fg='black',
                                   relief=tk.FLAT,
                                   padx=10,
                                   pady=5,
                                   cursor="hand2",
                                   command=lambda: self.check_password(dialog, password_entry))
        confirm_button.pack(pady=10)

    def check_password(self, dialog, entry):
        """Verify admin password"""
        pwd = entry.get()
        # Default admin password
        if pwd == "admin":
            dialog.destroy()
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def show_admin_panel(self):
        """Admin panel: display financial stats & history (CSV)"""
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("800x600")
        admin_window.config(bg="#fafafa")

        # Title
        title_label = tk.Label(admin_window,
                               text="Admin Panel",
                               font=("Arial", 18, "bold"),
                               bg="#fafafa",
                               fg='#d32f2f')
        title_label.pack(pady=10)

        # Financial Stats
        stats_frame = tk.LabelFrame(admin_window,
                                    text="Financial Stats",
                                    font=("Arial", 14, "bold"),
                                    bg="#fafafa",
                                    fg='#1b5e20')
        stats_frame.pack(fill="x", padx=20, pady=10)

        # 5-yuan Pool Stats
        inc_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Income: {self.total_income_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        inc_5.pack(anchor="w", padx=10, pady=2)

        pay_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Payout: {self.total_payout_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        pay_5.pack(anchor="w", padx=10, pady=2)

        net_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Net Income: {self.net_income_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        net_5.pack(anchor="w", padx=10, pady=2)

        # 20-yuan Pool Stats
        inc_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Income: {self.total_income_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        inc_20.pack(anchor="w", padx=10, pady=2)

        pay_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Payout: {self.total_payout_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        pay_20.pack(anchor="w", padx=10, pady=2)

        net_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Net Income: {self.net_income_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        net_20.pack(anchor="w", padx=10, pady=2)

        # Combined Stats
        total_inc = self.total_income_5 + self.total_income_20
        total_pay = self.total_payout_5 + self.total_payout_20
        total_net = self.net_income_5 + self.net_income_20

        inc_total_label = tk.Label(stats_frame,
                                   text=f"Total Income (Both Pools): {total_inc} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        inc_total_label.pack(anchor="w", padx=10, pady=2)

        pay_total_label = tk.Label(stats_frame,
                                   text=f"Total Payout (Both Pools): {total_pay} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        pay_total_label.pack(anchor="w", padx=10, pady=2)

        net_total_label = tk.Label(stats_frame,
                                   text=f"Total Net Income: {total_net} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        net_total_label.pack(anchor="w", padx=10, pady=2)

        count_label = tk.Label(stats_frame,
                               text=f"Total Draws: {self.game_count}",
                               font=("Arial", 12),
                               bg="#fafafa")
        count_label.pack(anchor="w", padx=10, pady=2)

        # ===================== History Section =====================
        history_frame = tk.LabelFrame(admin_window,
                                      text="History (CSV)",
                                      font=("Arial", 14, "bold"),
                                      bg="#fafafa",
                                      fg='#1b5e20')
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_area = tk.Text(history_frame, wrap="none", font=("Courier New", 10))
        text_area.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar
        scroll_y = tk.Scrollbar(history_frame, orient="vertical", command=text_area.yview)
        scroll_y.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scroll_y.set)

        # Read and display CSV content
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    text_area.insert(tk.END, line)
        else:
            text_area.insert(tk.END, "No history record yet.")

        text_area.config(state="disabled")  # Make history read-only

    # ==================== Determine Prize ====================
    def determine_prize(self):
        """
        Randomly select a prize from the current pool (5-yuan or 20-yuan).
        If the prize is "Try Again", grant a free game.
        """
        rand_num = random.random()
        cumulative = 0
        for prize, prob in self.current_prizes_dict.items():
            cumulative += prob
            if rand_num <= cumulative:
                if prize == "🎉 Try Again":
                    self.free_games += 1
                self.update_financials(prize)
                self.log_result(prize)
                self.game_count += 1
                self.game_count_label.config(text=f"Total Draws: {self.game_count}")
                return prize
        return "🔔 No Prize"

    # ==================== Update Payout & Net ====================
    def update_financials(self, prize):
        """
        Update total payout & net for the chosen pool.
        The 'Fourth Prize', 'Try Again', and 'No Prize' have no payout.
        """
        payout = 0

        # Determine payout based on prize and pool
        if self.current_pool == "5-yuan":
            if "100 RMB" in prize:
                payout = 100
            elif "50 RMB" in prize:
                payout = 50
            elif "20 RMB" in prize:
                payout = 20
            elif "10 RMB" in prize:
                payout = 10
            # 'Fourth Prize (0 RMB)', 'Try Again', 'No Prize' have no payout
            self.total_payout_5 += payout
            self.net_income_5 = self.total_income_5 - self.total_payout_5
        else:
            # 20-yuan pool with English prize names
            if "500 RMB" in prize:
                payout = 500
            elif "200 RMB" in prize:
                payout = 200
            elif "50 RMB" in prize:
                payout = 50
            elif "30 RMB" in prize:
                payout = 30
            # 'Fourth Prize (Coke 2 RMB)', 'Try Again', 'No Prize' have no payout
            self.total_payout_20 += payout
            self.net_income_20 = self.total_income_20 - self.total_payout_20

    # ==================== CSV Logging ====================
    def log_result(self, prize):
        """
        Record the draw result into CSV with PoolType, Prize, Income, Payout, Net
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine income & net based on pool
        if self.current_pool == "5-yuan":
            income = self.total_income_5
            net = self.net_income_5
            # Determine payout for this prize
            if "100 RMB" in prize:
                payout = 100
            elif "50 RMB" in prize:
                payout = 50
            elif "20 RMB" in prize:
                payout = 20
            elif "10 RMB" in prize:
                payout = 10
            else:
                payout = 0
        else:
            income = self.total_income_20
            net = self.net_income_20
            if "500 RMB" in prize:
                payout = 500
            elif "200 RMB" in prize:
                payout = 200
            elif "50 RMB" in prize:
                payout = 50
            elif "30 RMB" in prize:
                payout = 30
            else:
                payout = 0

        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                self.current_pool,
                prize,
                income,
                payout,
                net
            ])

        # Update prize counts
        if self.current_pool == "5-yuan":
            if prize in self.prize_counts_5:
                self.prize_counts_5[prize] += 1
        else:
            if prize in self.prize_counts_20:
                self.prize_counts_20[prize] += 1

    # ==================== Session Summary Popup ====================
    def show_session_summary_popup(self, pool):
        """
        Show popup when the chosen pool's plays are finished.
        Display the count of each prize won in that session.
        """
        popup = tk.Toplevel(self.root)
        popup.title(f"{pool} Session Summary")
        popup.geometry("350x500")
        popup.config(bg="#fafafa")

        # Christmas Decoration
        decoration_label = tk.Label(popup,
                                    text=f"🎄🎉 {pool} Session Results 🎉🎄",
                                    font=("Arial", 16, "bold"),
                                    bg="#fafafa",
                                    fg='#d32f2f')
        decoration_label.pack(pady=10)

        # Retrieve the appropriate prize counts
        if pool == "5-yuan":
            prize_counts = self.prize_counts_5
        else:
            prize_counts = self.prize_counts_20

        # Construct summary string
        summary_text = ""
        for prize, count in prize_counts.items():
            summary_text += f"{prize}: {count}\n"

        # Display the summary
        text_label = tk.Label(popup,
                              text=summary_text.strip(),
                              font=("Arial", 12),
                              bg="#fafafa",
                              justify=tk.LEFT)
        text_label.pack(pady=10)

        # Add Christmas Snowflakes or Symbols
        snow_label = tk.Label(popup,
                              text="❄️❄️❄️",
                              font=("Arial", 24),
                              bg="#fafafa")
        snow_label.pack(pady=10)

        # Close Button
        close_btn = tk.Button(popup,
                              text="Close",
                              font=("Arial", 12, "bold"),
                              bg='#43a047',
                              fg='black',
                              relief=tk.FLAT,
                              padx=10,
                              pady=5,
                              cursor="hand2",
                              command=lambda: self.close_session_summary(popup, pool))
        close_btn.pack(pady=20)

    def close_session_summary(self, popup, pool):
        """Close the summary popup and reset prize counts for the session."""
        popup.destroy()
        if pool == "5-yuan":
            for k in self.prize_counts_5:
                self.prize_counts_5[k] = 0
        else:
            for k in self.prize_counts_20:
                self.prize_counts_20[k] = 0

    # ==================== Admin Panel ====================
    def show_admin_login_dialog(self):
        """Admin entry: enter password to access admin panel"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("300x200")
        dialog.config(bg="#fff8e1")

        label = tk.Label(dialog, text="Enter admin password:", bg="#fff8e1", font=("Arial", 12))
        label.pack(pady=20)

        password_entry = tk.Entry(dialog, show="*", font=("Arial", 14))
        password_entry.pack(pady=10)

        confirm_button = tk.Button(dialog,
                                   text="Confirm",
                                   font=("Arial", 12, "bold"),
                                   bg='#43a047',
                                   fg='black',
                                   relief=tk.FLAT,
                                   padx=10,
                                   pady=5,
                                   cursor="hand2",
                                   command=lambda: self.check_password(dialog, password_entry))
        confirm_button.pack(pady=10)

    def check_password(self, dialog, entry):
        """Verify admin password"""
        pwd = entry.get()
        # Default admin password
        if pwd == "admin":
            dialog.destroy()
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def show_admin_panel(self):
        """Admin panel: display financial stats & history (CSV)"""
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Panel")
        admin_window.geometry("800x600")
        admin_window.config(bg="#fafafa")

        # Title
        title_label = tk.Label(admin_window,
                               text="Admin Panel",
                               font=("Arial", 18, "bold"),
                               bg="#fafafa",
                               fg='#d32f2f')
        title_label.pack(pady=10)

        # Financial Stats
        stats_frame = tk.LabelFrame(admin_window,
                                    text="Financial Stats",
                                    font=("Arial", 14, "bold"),
                                    bg="#fafafa",
                                    fg='#1b5e20')
        stats_frame.pack(fill="x", padx=20, pady=10)

        # 5-yuan Pool Stats
        inc_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Income: {self.total_income_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        inc_5.pack(anchor="w", padx=10, pady=2)

        pay_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Payout: {self.total_payout_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        pay_5.pack(anchor="w", padx=10, pady=2)

        net_5 = tk.Label(stats_frame,
                         text=f"5-yuan Pool Net Income: {self.net_income_5} RMB",
                         font=("Arial", 12),
                         bg="#fafafa")
        net_5.pack(anchor="w", padx=10, pady=2)

        # 20-yuan Pool Stats
        inc_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Income: {self.total_income_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        inc_20.pack(anchor="w", padx=10, pady=2)

        pay_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Payout: {self.total_payout_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        pay_20.pack(anchor="w", padx=10, pady=2)

        net_20 = tk.Label(stats_frame,
                          text=f"20-yuan Pool Net Income: {self.net_income_20} RMB",
                          font=("Arial", 12),
                          bg="#fafafa")
        net_20.pack(anchor="w", padx=10, pady=2)

        # Combined Stats
        total_inc = self.total_income_5 + self.total_income_20
        total_pay = self.total_payout_5 + self.total_payout_20
        total_net = self.net_income_5 + self.net_income_20

        inc_total_label = tk.Label(stats_frame,
                                   text=f"Total Income (Both Pools): {total_inc} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        inc_total_label.pack(anchor="w", padx=10, pady=2)

        pay_total_label = tk.Label(stats_frame,
                                   text=f"Total Payout (Both Pools): {total_pay} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        pay_total_label.pack(anchor="w", padx=10, pady=2)

        net_total_label = tk.Label(stats_frame,
                                   text=f"Total Net Income: {total_net} RMB",
                                   font=("Arial", 12),
                                   bg="#fafafa")
        net_total_label.pack(anchor="w", padx=10, pady=2)

        count_label = tk.Label(stats_frame,
                               text=f"Total Draws: {self.game_count}",
                               font=("Arial", 12),
                               bg="#fafafa")
        count_label.pack(anchor="w", padx=10, pady=2)

        # ===================== History Section =====================
        history_frame = tk.LabelFrame(admin_window,
                                      text="History (CSV)",
                                      font=("Arial", 14, "bold"),
                                      bg="#fafafa",
                                      fg='#1b5e20')
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_area = tk.Text(history_frame, wrap="none", font=("Courier New", 10))
        text_area.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar
        scroll_y = tk.Scrollbar(history_frame, orient="vertical", command=text_area.yview)
        scroll_y.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scroll_y.set)

        # Read and display CSV content
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    text_area.insert(tk.END, line)
        else:
            text_area.insert(tk.END, "No history record yet.")

        text_area.config(state="disabled")  # Make history read-only

    # ==================== Run the Application ====================
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CyberLuckyDraw()
    app.run()