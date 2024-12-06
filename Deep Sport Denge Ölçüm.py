import tkinter as tk
from tkinter import ttk
import time  

class UserStopwatch:
    def __init__(self, master, user_number):
        self.master = master
        self.user_number = user_number
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.update_job = None
        self.time_counter = 0
        self.user_name = ""

        self.create_widgets()  

    def create_widgets(self):
        frame = ttk.Frame(self.master, width=450, height=600, padding="10")
        frame.grid(row=0, column=self.user_number-1, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.grid_propagate(False)

        ttk.Label(frame, text=f"Öğrenci {self.user_number}", font=("Arial", 16),).grid(column=0, row=0, columnspan=2)

        self.entry_name = ttk.Entry(frame, font=("Arial", 14))
        self.entry_name.grid(column=0, row=1, pady=5)

        ttk.Button(frame, text="İsmi Ayarla", command=self.set_name).grid(column=1, row=1, pady=5)

        self.label_name = ttk.Label(frame, text="İsim GİRİLMEDİ...", font=("Arial", 16))
        self.label_name.grid(column=0, row=2, columnspan=2, pady=5)

        self.label_timer = ttk.Label(frame, text="00:00.00", font=("Arial", 24))
        self.label_timer.grid(column=0, row=3, columnspan=2, pady=5)

        self.button_stop = ttk.Button(frame, text="Durdur", command=self.stop_timer, state=tk.DISABLED)
        self.button_stop.grid(column=0, row=4, columnspan=2, pady=5, ipadx=15, ipady=15)

        self.label_status = ttk.Label(frame, text="", font=("Arial", 12))
        self.label_status.grid(column=0, row=6, columnspan=2, pady=5)

    def set_name(self):
        self.user_name = self.entry_name.get()
        self.label_name.config(text=self.user_name)

    def start_timer(self):
        if not self.running:  
            self.start_time = time.time() - self.elapsed_time  
            self.update_timer()  
            self.running = True 
            self.button_stop.config(state=tk.NORMAL)  

    def stop_timer(self):
        if self.running:  
            self.master.after_cancel(self.update_job)  
            self.running = False  
            self.button_stop.config(state=tk.DISABLED) 

    def reset_timer(self):
        self.stop_timer() 
        self.elapsed_time = 0  
        self.label_timer.config(text="00:00.00")
        self.label_name.config(text="İsim GİRİLMEDİ...")


    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time  
        minutes = int(self.elapsed_time // 60)  
        seconds = int(self.elapsed_time % 60) 
        milliseconds = int((self.elapsed_time % 1) * 100)  
        self.label_timer.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:02}")  
        self.update_job = self.master.after(10, self.update_timer)  

class DualStopwatchApp:
    def __init__(self, master):
        self.master = master
        master.title("Deep Sport")

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14))  

        self.create_users()  
        self.create_common_controls()  

    def create_users(self):
        users_frame = ttk.Frame(self.master, padding="10")
        users_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.user1 = UserStopwatch(users_frame, 1)
        self.user2 = UserStopwatch(users_frame, 2)
        self.user3 = UserStopwatch(users_frame, 3) 

    def create_common_controls(self):
        controls_frame = ttk.Frame(self.master, padding="10")
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        start_button = ttk.Button(controls_frame, text="Başlat", command=self.start_timers, style='TButton')
        start_button.grid(column=0, row=0, padx=10, pady=10, ipadx=20, ipady=10)

        reset_button = ttk.Button(controls_frame, text="Sıfırla", command=self.reset_timers, style='TButton')
        reset_button.grid(column=1, row=0, padx=10, pady=10, ipadx=20, ipady=10)
    
        
        save_left_button = ttk.Button(controls_frame, text="Kaydet Sol", command=lambda: self.save_time("Sol"), style='TButton')
        save_left_button.grid(column=2, row=0, padx=10, pady=10, ipadx=20, ipady=10)

    
        save_right_button = ttk.Button(controls_frame, text="Kaydet Sağ", command=lambda: self.save_time("Sağ"), style='TButton')
        save_right_button.grid(column=3, row=0, padx=10, pady=10, ipadx=20, ipady=10)

    def start_timers(self):
        self.user1.start_timer()
        self.user2.start_timer()
        self.user3.start_timer()

    def reset_timers(self):
        self.user1.reset_timer()
        self.user2.reset_timer()
        self.user3.reset_timer()

    def save_time(self, button_side):
        with open("times.txt", "a") as file:
            for user in [self.user1, self.user2, self.user3]:
                current_time = user.label_timer.cget("text")  
                current_name = user.user_name if user.user_name else f"Kullanıcı {user.user_number}"
                file.write(f"{current_name} - {button_side}: {current_time}\n")  
        self.user1.label_status.config(text=f"Zamanlar kaydedildi.")  
        self.user2.label_status.config(text=f"Zamanlar kaydedildi.")  
        self.user3.label_status.config(text=f"Zamanlar kaydedildi.")  

if __name__ == "__main__":
    root = tk.Tk()
    app = DualStopwatchApp(root)  
    root.mainloop()  
