import tkinter as tk
import configparser
from datetime import datetime, timedelta
import threading
import platform
import time
import logging
from labelsmith.shyft.constants import CONFIG_FILE

logger = logging.getLogger("labelsmith")

class TimerWindow:
    def __init__(self, root, time_color="#A78C7B", bg_color="#FFBE98", btn_text_color="#A78C7B"):
        self.root = root
        self.time_color = time_color
        self.bg_color = bg_color
        self.btn_text_color = btn_text_color
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)
        self.width = self.config["Window"]["width"]
        self.height = self.config["Window"]["height"]
        self.root.geometry(f"{self.width}x{self.height}")

        self.setup_ui()
        self.setup_timer()
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)

    def do_nothing(self):
        pass

    def setup_ui(self):
        self.root.title("Timer")
        self.root.configure(bg=self.bg_color)

        # Rest of your UI setup
        self.timer_label = tk.Label(
            self.root,
            text="00:00:00",
            font=("Helvetica Neue", 32, "bold"),
            fg=self.time_color,
            bg=self.bg_color,
        )
        self.timer_label.pack(expand=True, padx=0, pady=(5, 0))

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 5))

        button_font = ("Helvetica", 10)
        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.start,
            bg=self.bg_color,
            fg=self.btn_text_color,
            highlightbackground=self.bg_color,
            highlightthickness=0,
            bd=0,
            font=button_font,
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=2)

        self.stop_button = tk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop,
            bg=self.bg_color,
            fg=self.btn_text_color,
            highlightbackground=self.bg_color,
            highlightthickness=0,
            bd=0,
            font=button_font,
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=2)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset,
            bg=self.bg_color,
            fg=self.btn_text_color,
            highlightbackground=self.bg_color,
            highlightthickness=0,
            bd=0,
            font=button_font,
        )
        self.reset_button.grid(row=0, column=2, sticky="ew", padx=2)

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

    def setup_timer(self):
        self.elapsed_time = timedelta(0)
        self.running = False
        self.last_time = None

        self.update_timer_thread = threading.Thread(
            target=self.update_timer, daemon=True
        )
        self.update_timer_thread.start()

    def start(self):
        if not self.running:
            self.running = True
            self.last_time = datetime.now()
            logger.debug("Timer started.")

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time += datetime.now() - self.last_time
            logger.debug("Timer stopped.")

    def reset(self):
        self.stop()
        self.elapsed_time = timedelta(0)
        self.update_label("00:00:00")
        logger.debug("Timer reset.")

    def update_label(self, text):
        if self.timer_label.winfo_exists():
            self.timer_label.config(text=text)

    def update_timer(self):
        while True:
            if self.running:
                current_time = datetime.now()
                delta = current_time - self.last_time
                elapsed = self.elapsed_time + delta
                self.root.after(
                    0, self.update_label, str(elapsed).split(".")[0].rjust(8, "0")
                )
            time.sleep(0.1)

    def update_colors(self, time_color, bg_color, btn_text_color):
        self.time_color = time_color
        self.bg_color = bg_color
        self.btn_text_color = btn_text_color

        self.root.configure(bg=self.bg_color)
        self.timer_label.configure(fg=self.time_color, bg=self.bg_color)
        self.button_frame.configure(bg=self.bg_color)

        for button in [self.start_button, self.stop_button, self.reset_button]:
            button.configure(
                bg=self.bg_color,
                fg=self.btn_text_color,
                highlightbackground=self.bg_color
            )

        logger.debug(f"Timer window colors updated: time={time_color}, bg={bg_color}, btn={btn_text_color}")

    def on_close(self):
        self.running = False
        self.config.set("Window", "width", str(self.root.winfo_width()))
        self.config.set("Window", "height", str(self.root.winfo_height()))
        with open(CONFIG_FILE, "w") as config_file:
            self.config.write(config_file)
        logger.debug(
            f"Timer window dimensions saved: width={self.root.winfo_width()}, height={self.root.winfo_height()}"
        )
        self.root.destroy()
        logger.debug("Timer window closed.")