#!/usr/bin/env python3
"""
File watcher script for development with auto-reload
"""
import os
import sys
import subprocess
import signal
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_app()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only reload on Python file changes
        if event.src_path.endswith('.py') or event.src_path.endswith('.html') or event.src_path.endswith('.js'):
            print(f"\nFile changed: {event.src_path}")
            self.restart_app()
    
    def restart_app(self):
        if self.process:
            print("Stopping app...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        print("Starting app...")
        self.process = subprocess.Popen([
            'hypercorn', 'app:app', 
            '--bind', '0.0.0.0:8000',
            '--access-logfile', '-',
            '--error-logfile', '-'
        ])

def main():
    handler = AppReloadHandler()
    observer = Observer()
    observer.schedule(handler, path='/app', recursive=True)
    observer.start()
    
    def signal_handler(signum, frame):
        print("\nShutting down...")
        observer.stop()
        if handler.process:
            handler.process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)
    finally:
        observer.join()

if __name__ == "__main__":
    main()