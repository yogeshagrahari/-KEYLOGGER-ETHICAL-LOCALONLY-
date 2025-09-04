import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
# Mock EthicalKeylogger for testing if advanced_keylogger is unavailable
class EthicalKeylogger:
    def __init__(self):
        self.config = {
            'capture': {
                'enable_keystrokes': True,
                'enable_mouse': True,
                'enable_clipboard': True,
                'enable_screenshots': True
            }
        }
        self._running = False
        self._paused = False
        self._statistics = {
            'keystrokes': 0,
            'mouse_clicks': 0,
            'clipboard_changes': 0,
            'screenshots_taken': 0
        }
        self._session_id = "TEST123"
        self._start_time = None

    def start_logging(self):
        self._running = True
        self._paused = False

    def pause_logging(self):
        self._paused = True

    def resume_logging(self):
        self._paused = False

    def stop_logging(self):
        self._running = False

    def take_screenshot(self, manual=False):
        self._statistics['screenshots_taken'] += 1

    def get_status(self):
        import time
        uptime = "0s"
        if self._start_time:
            uptime = f"{int(time.time() - self._start_time)}s"
        return {
            'session_id': self._session_id,
            'running': self._running,
            'paused': self._paused,
            'uptime': uptime,
            'statistics': self._statistics
        }

class KeyloggerGUI:
    """GUI interface for the ethical keylogger"""
    
    def __init__(self):
        self.keylogger = EthicalKeylogger()
        self.root = tk.Tk()
        self.setup_ui()
        self.update_status()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("🔒 Advanced Ethical Keylogger - Research Tool")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Ethical warning
        self.show_ethical_warning()
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🔒 Advanced Ethical Keylogger",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="🟢 Start Logging", command=self.start_logging)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(control_frame, text="⏸️ Pause", command=self.pause_logging)
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.resume_btn = ttk.Button(control_frame, text="▶️ Resume", command=self.resume_logging)
        self.resume_btn.grid(row=0, column=2, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="🔴 Stop", command=self.stop_logging)
        self.stop_btn.grid(row=0, column=3, padx=5)
        
        self.screenshot_btn = ttk.Button(control_frame, text="📸 Screenshot", command=self.take_screenshot)
        self.screenshot_btn.grid(row=0, column=4, padx=5)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, width=80, state='disabled')
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkboxes for features
        self.keystroke_var = tk.BooleanVar(value=self.keylogger.config['capture']['enable_keystrokes'])
        self.mouse_var = tk.BooleanVar(value=self.keylogger.config['capture']['enable_mouse'])
        self.clipboard_var = tk.BooleanVar(value=self.keylogger.config['capture']['enable_clipboard'])
        self.screenshot_var = tk.BooleanVar(value=self.keylogger.config['capture']['enable_screenshots'])
        
        ttk.Checkbutton(config_frame, text="Keystrokes", variable=self.keystroke_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(config_frame, text="Mouse Events", variable=self.mouse_var).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(config_frame, text="Clipboard", variable=self.clipboard_var).grid(row=0, column=2, sticky=tk.W)
        ttk.Checkbutton(config_frame, text="Screenshots", variable=self.screenshot_var).grid(row=0, column=3, sticky=tk.W)
        
        # Statistics
        stats_frame = ttk.LabelFrame(main_frame, text="Session Statistics", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=6, width=80, state='disabled')
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def show_ethical_warning(self):
        """Show ethical use warning dialog"""
        warning = """
⚠️ ETHICAL USE AGREEMENT ⚠️

This software is for AUTHORIZED research and educational purposes ONLY.

By proceeding, you agree to:
✅ Use only on authorized devices with explicit consent
✅ Comply with all applicable laws and regulations  
✅ Protect collected data according to privacy standards
✅ Use for legitimate research purposes only

❌ PROHIBITED: Unauthorized surveillance, malicious use, 
    or any illegal activities

Do you accept these terms and confirm authorized use?
        """
        
        result = messagebox.askyesno("Ethical Use Agreement", warning)
        if not result:
            self.root.destroy()
            exit()
    
    def start_logging(self):
        """Start the keylogger"""
        try:
            # Update configuration
            self.keylogger.config['capture']['enable_keystrokes'] = self.keystroke_var.get()
            self.keylogger.config['capture']['enable_mouse'] = self.mouse_var.get()
            self.keylogger.config['capture']['enable_clipboard'] = self.clipboard_var.get()
            self.keylogger.config['capture']['enable_screenshots'] = self.screenshot_var.get()
            
            # Start in separate thread
            threading.Thread(target=self.keylogger.start_logging, daemon=True).start()
            
            self.log_message("✅ Keylogger started successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start keylogger: {e}")
    
    def pause_logging(self):
        """Pause logging"""
        self.keylogger.pause_logging()
        self.log_message("⏸️ Logging paused")
    
    def resume_logging(self):
        """Resume logging"""
        self.keylogger.resume_logging() 
        self.log_message("▶️ Logging resumed")
    
    def stop_logging(self):
        """Stop the keylogger"""
        self.keylogger.stop_logging()
        self.log_message("🔴 Keylogger stopped")
    
    def take_screenshot(self):
        """Take manual screenshot"""
        self.keylogger.take_screenshot(manual=True)
        self.log_message("📸 Manual screenshot taken")
    
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
    
    def update_status(self):
        """Update status display"""
        try:
            status = self.keylogger.get_status()
            
            # Update statistics display
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            
            stats_info = f"""Session ID: {status['session_id']}
Status: {'🟢 Running' if status['running'] else '🔴 Stopped'} {'(⏸️ Paused)' if status['paused'] else ''}
Uptime: {status['uptime']}

Statistics:
• Keystrokes: {status['statistics']['keystrokes']:,}
• Mouse Clicks: {status['statistics']['mouse_clicks']:,}
• Clipboard Changes: {status['statistics']['clipboard_changes']:,}
• Screenshots: {status['statistics']['screenshots_taken']:,}
"""
            
            self.stats_text.insert(tk.END, stats_info)
            self.stats_text.config(state='disabled')
            
        except Exception as e:
            pass  # Silent fail for status updates
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyloggerGUI()
    app.run()
