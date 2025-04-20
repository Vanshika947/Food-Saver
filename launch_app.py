import webview
import threading
import subprocess

def run_streamlit():
    subprocess.Popen(['streamlit', 'run', 'launch_app.py'])

# Start Streamlit in the background
threading.Thread(target=run_streamlit).start()

# Open it in a native GUI window
webview.create_window('My Streamlit App', 'http://localhost:8501')
webview.start()