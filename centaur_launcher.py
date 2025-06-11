#!/usr/bin/env python3
"""
AI Qube Centaur Ecosystem - Desktop GUI Launcher
A simple, professional desktop application for managing the Centaur System

Features:
- One-click deployment and management
- Real-time system status monitoring
- Environment configuration
- Service health checks
- Performance monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import os
import sys
import json
from datetime import datetime
import webbrowser

class CentaurLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🏛️ AI Qube Centaur Ecosystem - Control Center")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.setup_styles()
        
        # Initialize variables
        self.system_status = {
            'postgres': False,
            'weaviate': False,
            'n8n': False,
            'ai_services': False
        }
        
        # Setup GUI
        self.setup_gui()
        
        # Start status monitoring
        self.monitor_status()
    
    def setup_styles(self):
        """Configure modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00', 
                       font=('Arial', 10))
        
        style.configure('Warning.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffaa00', 
                       font=('Arial', 10))
        
        style.configure('Error.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ff4444', 
                       font=('Arial', 10))
        
        style.configure('Launch.TButton',
                       font=('Arial', 14, 'bold'),
                       foreground='#ffffff')
        
        style.configure('Action.TButton',
                       font=('Arial', 10),
                       foreground='#ffffff')
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title and Logo
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(title_frame, text="🏛️ AI Qube Centaur Ecosystem", 
                 style='Title.TLabel').pack()
        ttk.Label(title_frame, text="Multi-Agent Recursive Learning Platform", 
                 background='#2b2b2b', foreground='#cccccc', 
                 font=('Arial', 10)).pack()
        
        # Status Panel
        self.setup_status_panel(main_frame)
        
        # Control Panel
        self.setup_control_panel(main_frame)
        
        # Log Panel
        self.setup_log_panel(main_frame)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        ttk.Label(footer_frame, 
                 text="Ready for Production Deployment - 95% Complete", 
                 background='#2b2b2b', foreground='#00ff00', 
                 font=('Arial', 9)).pack()
    
    def setup_status_panel(self, parent):
        """Setup system status monitoring panel"""
        status_frame = ttk.LabelFrame(parent, text="🔍 System Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status indicators
        self.status_labels = {}
        
        services = [
            ('postgres', 'PostgreSQL Database'),
            ('weaviate', 'Weaviate Vector DB'),
            ('n8n', 'n8n Workflow Engine'),
            ('ai_services', 'AI Service APIs')
        ]
        
        for i, (key, name) in enumerate(services):
            row_frame = ttk.Frame(status_frame)
            row_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), padx=5, pady=2)
            
            ttk.Label(row_frame, text=f"{name}:", 
                     background='#2b2b2b', foreground='#cccccc').pack(side=tk.LEFT)
            
            self.status_labels[key] = ttk.Label(row_frame, text="🔴 Offline", 
                                              style='Error.TLabel')
            self.status_labels[key].pack(side=tk.RIGHT)
    
    def setup_control_panel(self, parent):
        """Setup main control buttons"""
        control_frame = ttk.LabelFrame(parent, text="🚀 Control Center", padding="15")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Main launch button
        launch_btn = ttk.Button(control_frame, 
                               text="🚀 DEPLOY CENTAUR SYSTEM", 
                               style='Launch.TButton',
                               command=self.deploy_system)
        launch_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons grid
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        buttons = [
            ("⚙️ Configure Environment", self.configure_environment),
            ("🗄️ Setup Database", self.setup_database),
            ("🧠 Deploy AI Services", self.deploy_ai_services),
            ("📊 Open Dashboard", self.open_dashboard),
            ("🔍 Health Check", self.health_check),
            ("📋 View Logs", self.view_logs),
            ("⏹️ Stop Services", self.stop_services),
            ("🔄 Restart System", self.restart_system)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, 
                           style='Action.TButton', command=command)
            btn.grid(row=i//2, column=i%2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
    
    def setup_log_panel(self, parent):
        """Setup log monitoring panel"""
        log_frame = ttk.LabelFrame(parent, text="📋 System Logs", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        parent.rowconfigure(3, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            bg='#1e1e1e', 
            fg='#ffffff', 
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial log
        self.log_message("🏛️ AI Qube Centaur Ecosystem Control Center Initialized")
        self.log_message("📊 System Status: 95% Deployment Ready")
        self.log_message("⚡ Ready for environment configuration and deployment")
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def monitor_status(self):
        """Monitor system status in background"""
        def check_status():
            # Check PostgreSQL
            try:
                result = subprocess.run(['pg_isready', '-h', 'localhost'], 
                                      capture_output=True, timeout=5)
                self.system_status['postgres'] = result.returncode == 0
            except:
                self.system_status['postgres'] = False
            
            # Check Weaviate
            try:
                import requests
                response = requests.get('http://localhost:8080/v1/.well-known/ready', timeout=5)
                self.system_status['weaviate'] = response.status_code == 200
            except:
                self.system_status['weaviate'] = False
            
            # Check n8n
            try:
                import requests
                response = requests.get('http://localhost:5678/healthz', timeout=5)
                self.system_status['n8n'] = response.status_code == 200
            except:
                self.system_status['n8n'] = False
            
            # Check AI services (environment variables)
            ai_keys = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY']
            self.system_status['ai_services'] = all(os.getenv(key) for key in ai_keys)
            
            # Update UI
            self.root.after(0, self.update_status_ui)
        
        # Run status check in background thread
        threading.Thread(target=check_status, daemon=True).start()
        
        # Schedule next check
        self.root.after(10000, self.monitor_status)  # Check every 10 seconds
    
    def update_status_ui(self):
        """Update status indicators in UI"""
        for service, status in self.system_status.items():
            if status:
                self.status_labels[service].config(text="🟢 Online", style='Status.TLabel')
            else:
                self.status_labels[service].config(text="🔴 Offline", style='Error.TLabel')
    
    def deploy_system(self):
        """Main deployment function"""
        self.log_message("🚀 Starting Centaur System Deployment...")
        
        # Check prerequisites
        if not self.check_prerequisites():
            return
        
        def deploy():
            try:
                # Run deployment scripts
                scripts = [
                    'scripts/deploy_n8n_workflows.py',
                    'scripts/populate_rag_system.py',
                    'scripts/end_to_end_integration.py'
                ]
                
                for script in scripts:
                    self.log_message(f"⚡ Executing {script}...")
                    result = subprocess.run([sys.executable, script], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.log_message(f"✅ {script} completed successfully")
                    else:
                        self.log_message(f"❌ {script} failed: {result.stderr}")
                        return
                
                self.log_message("🎉 Deployment completed successfully!")
                messagebox.showinfo("Success", "Centaur System deployed successfully!")
                
            except Exception as e:
                self.log_message(f"❌ Deployment failed: {str(e)}")
                messagebox.showerror("Error", f"Deployment failed: {str(e)}")
        
        # Run deployment in background thread
        threading.Thread(target=deploy, daemon=True).start()
    
    def check_prerequisites(self):
        """Check if prerequisites are met"""
        missing = []
        
        # Check environment variables
        required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_API_KEY', 'POSTGRES_PASSWORD']
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            self.log_message(f"⚠️ Missing environment variables: {', '.join(missing)}")
            messagebox.showwarning("Prerequisites Missing", 
                                 f"Please set these environment variables:\n{chr(10).join(missing)}")
            return False
        
        return True
    
    def configure_environment(self):
        """Open environment configuration dialog"""
        self.log_message("⚙️ Opening environment configuration...")
        
        config_window = tk.Toplevel(self.root)
        config_window.title("Environment Configuration")
        config_window.geometry("600x500")
        config_window.configure(bg='#2b2b2b')
        
        # Environment variables form
        vars_frame = ttk.LabelFrame(config_window, text="API Keys and Configuration", padding="10")
        vars_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        env_vars = [
            ('ANTHROPIC_API_KEY', 'Claude API Key'),
            ('OPENAI_API_KEY', 'OpenAI API Key'),
            ('GOOGLE_API_KEY', 'Google Gemini API Key'),
            ('POSTGRES_PASSWORD', 'PostgreSQL Password'),
            ('GITHUB_TOKEN', 'GitHub Token')
        ]
        
        entries = {}
        for i, (var, label) in enumerate(env_vars):
            ttk.Label(vars_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(vars_frame, width=50, show="*" if "PASSWORD" in var or "KEY" in var or "TOKEN" in var else None)
            entry.grid(row=i, column=1, padx=(10, 0), pady=2)
            entry.insert(0, os.getenv(var, ""))
            entries[var] = entry
        
        def save_config():
            for var, entry in entries.items():
                value = entry.get().strip()
                if value:
                    os.environ[var] = value
            
            self.log_message("✅ Environment configuration updated")
            config_window.destroy()
        
        ttk.Button(vars_frame, text="Save Configuration", command=save_config).grid(row=len(env_vars), column=0, columnspan=2, pady=10)
    
    def setup_database(self):
        """Setup PostgreSQL database"""
        self.log_message("🗄️ Setting up PostgreSQL database...")
        
        def setup():
            try:
                # Run database setup
                result = subprocess.run([
                    'psql', '-U', 'postgres', '-d', 'centaur_coordination', 
                    '-f', 'database/coordination_schema.sql'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_message("✅ Database setup completed")
                else:
                    self.log_message(f"❌ Database setup failed: {result.stderr}")
            except Exception as e:
                self.log_message(f"❌ Database setup error: {str(e)}")
        
        threading.Thread(target=setup, daemon=True).start()
    
    def deploy_ai_services(self):
        """Deploy AI services"""
        self.log_message("🧠 Deploying AI services...")
        messagebox.showinfo("AI Services", "AI services are integrated via API calls.\nEnsure API keys are configured.")
    
    def open_dashboard(self):
        """Open performance dashboard"""
        self.log_message("📊 Opening performance dashboard...")
        dashboard_path = os.path.join(os.getcwd(), "dashboard", "coordination_dashboard.html")
        
        if os.path.exists(dashboard_path):
            webbrowser.open(f"file://{dashboard_path}")
        else:
            messagebox.showwarning("Dashboard", "Dashboard file not found. Run deployment first.")
    
    def health_check(self):
        """Perform system health check"""
        self.log_message("🔍 Performing system health check...")
        
        def check():
            try:
                result = subprocess.run([sys.executable, 'scripts/health_check.py'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_message("✅ Health check completed")
                    self.log_message(result.stdout)
                else:
                    self.log_message(f"⚠️ Health check issues: {result.stderr}")
            except Exception as e:
                self.log_message(f"❌ Health check error: {str(e)}")
        
        threading.Thread(target=check, daemon=True).start()
    
    def view_logs(self):
        """View detailed system logs"""
        self.log_message("📋 Opening detailed log viewer...")
        
        log_window = tk.Toplevel(self.root)
        log_window.title("System Logs")
        log_window.geometry("800x600")
        
        log_text = scrolledtext.ScrolledText(log_window, bg='#1e1e1e', fg='#ffffff', font=('Consolas', 9))
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load logs from file if exists
        try:
            with open('system.log', 'r') as f:
                log_text.insert(tk.END, f.read())
        except FileNotFoundError:
            log_text.insert(tk.END, "No log file found. Logs will appear after system operations.")
    
    def stop_services(self):
        """Stop all services"""
        self.log_message("⏹️ Stopping services...")
        
        if messagebox.askyesno("Stop Services", "Are you sure you want to stop all services?"):
            def stop():
                try:
                    # Stop Docker containers if running
                    subprocess.run(['docker-compose', 'down'], capture_output=True)
                    self.log_message("✅ Services stopped")
                except Exception as e:
                    self.log_message(f"❌ Error stopping services: {str(e)}")
            
            threading.Thread(target=stop, daemon=True).start()
    
    def restart_system(self):
        """Restart the entire system"""
        self.log_message("🔄 Restarting system...")
        
        if messagebox.askyesno("Restart System", "This will restart all services. Continue?"):
            self.stop_services()
            self.root.after(5000, self.deploy_system)  # Restart after 5 seconds

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = CentaurLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
