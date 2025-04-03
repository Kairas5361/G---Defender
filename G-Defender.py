import webbrowser
import keyboard
import customtkinter as ctk
from threading import Thread
import time
import pystray
from PIL import Image
import sys
import os
import win10toast

DEFAULT_SITE = "RickRoll"
URLS = {
    "RickRoll": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "JumpScare": "https://www.youtube.com/watch?v=HidGsjl-3jI"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("G")
        self.geometry("350x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self.show_in_tray = True
        self.show_notifications = True
        self.toaster = win10toast.ToastNotifier()
        
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            icon_path = os.path.join(script_dir, "ikon.png")
            self.tray_image = Image.open(icon_path)
        except:
            self.tray_image = Image.new('RGB', (64, 64), color='black')
        
        try:
            self.iconbitmap(icon_path)
        except:
            pass
        
        self.main_frame = ctk.CTkFrame(self)
        self.settings_frame = ctk.CTkFrame(self)
        
        self.create_main_widgets()
        self.create_settings_widgets()
        
        self.show_main_frame()
        
        self.listener_thread = Thread(target=self.check_g_press, daemon=True)
        self.listener_thread.start()
        
        self.tray_icon = None
        if self.show_in_tray:
            self.create_tray_icon()
        
        if self.show_notifications:
            self.show_windows_notification("G - Defender", "Now Application is Worked!")

    def show_windows_notification(self, title, message):
        try:
            self.toaster.show_toast(
                title,
                message,
                icon_path=None,
                duration=3,
                threaded=True
            )
        except:
            self.show_fallback_notification(message)

    def show_fallback_notification(self, message):
        notification = tk.Toplevel(self)
        notification.title("Notification")
        notification.geometry("300x80")
        notification.resizable(False, False)
        notification.attributes('-topmost', True)
        notification.after(3000, notification.destroy)
        
        label = ctk.CTkLabel(notification, text=message, font=("Arial", 12))
        label.pack(pady=20)
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        notification.update_idletasks()
        width = notification.winfo_width()
        height = notification.winfo_height()
        x = screen_width - width - 20
        y = screen_height - height - 50
        notification.geometry(f"+{x}+{y}")

    def create_main_widgets(self):
        self.main_frame.pack(fill="both", expand=True)
        
        self.settings_btn = ctk.CTkButton(
            self.main_frame,
            text="⚙",
            width=25,
            height=25,
            command=self.show_settings_frame,
            fg_color="transparent",
            hover_color="#333333",
            text_color=("gray", "lightgray"),
            font=("Arial", 14)
        )
        self.settings_btn.place(relx=0.95, rely=0.05, anchor="ne")
        
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="G - Defender",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=15)

        self.combo = ctk.CTkComboBox(
            self.main_frame,
            values=list(URLS.keys()),
            font=("Arial", 14),
            state="readonly",
            dropdown_fg_color="#2b2b2b",
            button_color="#3b3b3b",
            command=self.on_site_change,
            text_color=("black", "white"),
            dropdown_text_color=("black", "white")
        )
        self.combo.set(DEFAULT_SITE)
        self.combo.pack(pady=10)

        self.site_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Now Selected: {self.combo.get()}",
            font=("Arial", 12, "italic"),
            text_color="#5dade2"
        )
        self.site_label.pack(pady=5)

        copyright_label = ctk.CTkLabel(
            self.main_frame,
            text="© 2025 G - Defender - All Rights Reserved.",
            font=("Arial", 10),
            text_color="gray"
        )
        copyright_label.pack(side="bottom", pady=5)

    def on_site_change(self, event=None):
        current_site = self.combo.get()
        self.site_label.configure(text=f"Şu an seçili: {current_site}")
        
        if self.show_notifications:
            self.show_windows_notification(
                "Site Modification",
                f"The Application Has Now Switched to {current_site}"
            )

    def create_settings_widgets(self):
        self.settings_frame.pack(fill="both", expand=True)
        
        self.back_btn = ctk.CTkButton(
            self.settings_frame,
            text="←",
            width=25,
            height=25,
            command=self.show_main_frame,
            fg_color="transparent",
            hover_color="#333333",
            text_color=("gray", "lightgray"),
            font=("Arial", 14)
        )
        self.back_btn.place(relx=0.05, rely=0.05, anchor="nw")
        
        settings_label = ctk.CTkLabel(
            self.settings_frame,
            text="Settin'",
            font=("Arial", 20, "bold")
        )
        settings_label.pack(pady=10)
        
        self.dark_mode_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Dark Theme",
            command=self.toggle_dark_mode
        )
        self.dark_mode_switch.pack(pady=5)
        self.dark_mode_switch.select()
        
        self.tray_icon_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Show in System Tray",
            command=self.toggle_tray_icon
        )
        self.tray_icon_switch.pack(pady=5)
        self.tray_icon_switch.select()
        
        self.notification_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Show Notifications",
            command=self.toggle_notifications
        )
        self.notification_switch.pack(pady=5)
        self.notification_switch.select()
   
        info_label = ctk.CTkLabel(
            self.settings_frame,
            text="This Application Developed by Kairas5361.",
            font=("Arial", 12),
            text_color="gray"
        )
        info_label.pack(pady=10)

        copyright_label = ctk.CTkLabel(
            self.settings_frame,
            text="© 2025 G - Defender - All Rights Reserved.",
            font=("Arial", 10),
            text_color="gray"
        )
        copyright_label.pack(side="bottom", pady=5)

    def toggle_notifications(self):
        self.show_notifications = self.notification_switch.get() == 1

    def toggle_tray_icon(self):
        self.show_in_tray = self.tray_icon_switch.get() == 1
        if self.show_in_tray:
            if not self.tray_icon:
                self.create_tray_icon()
        else:
            if self.tray_icon:
                self.tray_icon.stop()
                self.tray_icon = None

    def toggle_dark_mode(self):
        if self.dark_mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def show_main_frame(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.title("G - Defender")
        self.update_site_label()

    def show_settings_frame(self):
        self.main_frame.pack_forget()
        self.settings_frame.pack(fill="both", expand=True)
        self.title("Settin'")

    def update_site_label(self, event=None):
        current_site = self.combo.get()
        self.site_label.configure(text=f"Şu an seçili: {current_site}")

    def open_selected_site(self):
        webbrowser.open(URLS[self.combo.get()])

    def check_g_press(self):
        while True:
            if keyboard.is_pressed('g'):
                self.open_selected_site()
                time.sleep(0.3)
            time.sleep(0.01)

    def create_tray_icon(self):
        menu = (
            pystray.MenuItem('Open Application', self.show_from_tray),
            pystray.MenuItem('Quit', self.quit_app)
        )
        self.tray_icon = pystray.Icon("g_shortcut", self.tray_image, "G - Defender", menu)
        Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_to_tray(self):
        if self.show_in_tray:
            self.withdraw()
        else:
            self.quit_app()

    def show_from_tray(self):
        self.deiconify()
        self.lift()

    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()