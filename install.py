from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from pathlib import Path
import subprocess
import shlex
import json

home = Path.home()
src = home / ".facefusion"
css = src / "style.css"
startup = home / ".ipython/profile_default/startup"
key_file = src / "api-key.json"

R = "\033[0m"
GREEN = f"\033[38;5;35m▶{R}"

def CondaInstall():
    try:
        cmd_list = [
            ('conda install -qy mamba', 'Installing Anaconda'),
            ('mamba install -y python=3.10.13', 'Installing Python 3.10'),
            ('mamba install -y ffmpeg cuda-runtime cudnn', 'Installing Dependencies'),
            ('pip install psutil', 'Installing Python Packages'),
            ('conda clean -qy --all', None)
        ]

        for cmd, msg in cmd_list:
            if msg: print(f"{GREEN} {msg}")
            subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"{GREEN} Installation Complete")
        get_ipython().kernel.do_shutdown(True)

    except KeyboardInterrupt:
        clear_output()
        print("Installation Canceled")

def KeyCheck():
    if not key_file.exists():
        key = input("Enter FaceFusion API Key: ").strip()
        if len(key) < 32:
            print("Invalid API Key (Must be 32+ characters)")
            return
            
        with open(key_file, "w") as f:
            json.dump({"facefusion-key": key}, f)
    
    CondaInstall()

Path(src).mkdir(exist_ok=True)
KeyCheck()