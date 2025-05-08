#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading, time, random, os
import requests

BASE_URL        = "http://localhost:5000"      
ENDPOINT_USER   = f"{BASE_URL}/user"           
ENDPOINT_ECG    = f"{BASE_URL}/ecg"            
ENDPOINT_RUN    = f"{BASE_URL}/run"            
USER_ID         = "user123"                    
SIM_INTERVAL    = 1.0                          
ECG_OPTIONS     = ["normal", "abnormal", "unknown"]


class WatchSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watch Simulator")
        self.geometry("500x400")

        ttk.Label(self, text="Select ECG to send to similarity service:").pack(pady=5)
        self.ecg_var = tk.StringVar(value=ECG_OPTIONS[0])
        self.ecg_menu = ttk.Combobox(self, textvariable=self.ecg_var, values=ECG_OPTIONS, state="readonly")
        self.ecg_menu.pack()

        self.start_btn = ttk.Button(self, text="Start Run", command=self.on_start)
        self.start_btn.pack(pady=10)

        ttk.Label(self, text="Logs:").pack(anchor="w", padx=5)
        self.log_win = scrolledtext.ScrolledText(self, height=12, state="disabled")
        self.log_win.pack(fill="both", expand=True, padx=5, pady=5)

        self.running = False

    def log(self, msg):
        self.log_win.configure(state="normal")
        self.log_win.insert("end", f"{time.strftime('%H:%M:%S')}  {msg}\n")
        self.log_win.see("end")
        self.log_win.configure(state="disabled")

    def on_start(self):
        if self.running:
            return
        self.running = True
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.run_sequence, daemon=True).start()

    def run_sequence(self):
        try:
            self.log("Sending user details...")
            resp = requests.post(ENDPOINT_USER, json={"user_id": USER_ID})
            resp.raise_for_status()
            self.log("✔ User details saved.")

            selection = self.ecg_var.get()
            hea_file = f"{selection}.hea"
            dat_file = f"{selection}.dat"
            if not (os.path.exists(hea_file) and os.path.exists(dat_file)):
                raise FileNotFoundError(f"ECG files for '{selection}' not found.")
            self.log(f"Sending ECG ({selection}) for similarity search...")
            files = {
                "ecg_hea": open(hea_file, "r"),
                "ecg_dat": open(dat_file, "rb"),
            }
            resp = requests.post(ENDPOINT_ECG, files=files)
            resp.raise_for_status()
            sim_result = resp.json().get("result", "<no result>")
            self.log(f"✔ ECG similarity result: {sim_result}")

            distance = 0.0
            start_ts = time.time()
            self.log("Starting run data stream...")
            while True:
                elapsed = time.time() - start_ts
                hr    = random.randint(90, 150)
                pace  = round(random.uniform(5.0, 7.0), 2)  
                speed = 60.0 / pace                     
                distance += speed * (SIM_INTERVAL / 3600)

                payload = {
                    "user_id": USER_ID,
                    "heart_rate": hr,
                    "pace": pace,
                    "distance": round(distance, 3),
                    "timestamp": int(time.time())
                }
                self.log(f"Sending run data ➔ HR: {hr}  Pace: {pace}  Dist: {payload['distance']} km")
                resp = requests.post(ENDPOINT_RUN, json=payload)
                resp.raise_for_status()

                time.sleep(SIM_INTERVAL)

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.running = False
            self.start_btn.configure(state="normal")

if __name__ == "__main__":
    app = WatchSimulator()
    app.mainloop()
