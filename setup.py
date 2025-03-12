R = "\033[31m"
P = "\033[38;5;135m"
RST = "\033[0m"
ERR = f"{P}[{RST}{R}ERROR{RST}{P}]{RST}"

import sys, subprocess
python_version = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.split()[1]
if tuple(map(int, python_version.split('.'))) < (3, 10, 6):
    print(f"{ERR}: Python version 3.10.6 or higher required, and you are using Python {python_version}")
    sys.exit()

from IPython.display import display, HTML, clear_output, Image
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import shutil
import json
import os

from nenen88 import pull, say, download, clone, tempe

SyS = get_ipython().system
CD = os.chdir

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MRK = SRC / 'marking.py'
MARKED = SRC / 'marking.json'
TMP = Path('/tmp')

SRC.mkdir(parents=True, exist_ok=True)
iRON = os.environ

def load_css():
    display(HTML(f"<style>{CSS.read_text()}</style>"))

def tmp_cleaning(v):
    for i in TMP.iterdir():
        if i.is_dir() and i != v:
            shutil.rmtree(i)
        elif i.is_file() and i != v:
            i.unlink()

def check_ffmpeg():
    i = get_ipython().getoutput('conda list ffmpeg')
    if not any('ffmpeg' in l for l in i):
        c = [
            ('mamba install -y ffmpeg curl', '\ninstalling ffmpeg...'),
            ('mamba install -y cuda-runtime=12.4.1', 'installing cuda-runtime=12.4.1...'),
            ('mamba install -y cudnn=9.2.1.18', 'installing cudnn=9.2.1.18...'),
            ('conda clean -y --all', None)
        ]

        for d, m in c:
            if m is not None:
                print(m)
            subprocess.run(shlex.split(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def marking(p, n, i):
    t = p / n
    if not t.exists():
        t.write_text(json.dumps({
            'ui': i, 'launch_args': '',
            'zrok_token': '', 'ngrok_token': '',
            'tunnel': ''
        }, indent=4))
    d = json.loads(t.read_text())
    d.update({'ui': i, 'launch_args': ''})
    t.write_text(json.dumps(d, indent=4))

def install_tunnel():
    bins = {
        'zrok': {
            'bin': HOME / '.zrok/bin/zrok',
            'url': 'https://github.com/openziti/zrok/releases/download/v0.4.44/zrok_0.4.44_linux_amd64.tar.gz'
        },
        'ngrok': {
            'bin': HOME / '.ngrok/bin/ngrok',
            'url': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz'
        }
    }

    for n, b in bins.items():
        binPath = b['bin']
        if binPath.exists():
            continue

        url = b['url']
        name = Path(url).name
        binDir = binPath.parent

        binDir.mkdir(parents=True, exist_ok=True)

        SyS(f'curl -sLo {binDir}/{name} {url}')
        SyS(f'tar -xzf {binDir}/{name} -C {binDir} --wildcards *{n}')
        SyS(f'rm -f {binDir}/{name}')

        if str(binDir) not in iRON.get('PATH', ''):
            iRON['PATH'] += ':' + str(binDir)

        binPath.chmod(0o755)

def facetrainer(ui):
    with loading:
        display(Image(filename=str(IMG)))

    SDTFusion = {
        'FaceFusion': ('--depth 1 https://github.com/LaoJiuYes/facefusion-lockless FaceFusion', TMP / 'venv-fusion')
    }

    with output:
        if ui in SDTFusion:
            WEBUI = HOME / ui
            repo, vnv = SDTFusion[ui]

        say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
        clone(repo)

        marking(SRC, MARKED, ui)
        tmp_cleaning(vnv)

        if ui == 'FaceFusion':
            check_ffmpeg()
            req = [
                f"rm -rf {HOME}/tmp {HOME}/.cache/*", 
                f"ln -vs /tmp {HOME}/tmp"
            ]

        for lines in req: SyS(f'{lines}>/dev/null 2>&1')

        scripts = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
        ]

        for items in scripts: download(items)

        tempe()

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', str(MRK))
            get_ipython().run_line_magic('run', str(WEBUI / 'venv.py'))

            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")
            CD(HOME)

def oppai(btn):
    global ui
    ui = btn
    multi_panel.layout.display = 'none'

    config = json.load(MARKED.open('r')) if MARKED.exists() else {}
    cui = config.get('ui')
    WEBUI = HOME / ui if ui else None

    if WEBUI and WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            CD(WEBUI)
            with output:
                SyS("git pull origin master")

                x = [
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
                    f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
                ]

                print()
                for y in x:
                    download(y)

    else:
        if cui and cui != ui:
            ass = HOME / cui
            with output:
                if ass.exists():
                    print(f"{cui} is installed. uninstall it before switching to {ui}.")
                    return

        facetrainer(ui)

output = widgets.Output()
loading = widgets.Output()

row2 = ['FaceFusion']
buttons2 = [widgets.Button(description='') for btn in row2]
for button, btn in zip(buttons2, row2):
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: oppai(btn))

multi_panel = widgets.VBox([widgets.HBox(buttons2)], layout=widgets.Layout(width='640px', height='520px'))
multi_panel.add_class('multi-panel')

def multi_widgets():
    for cmd in [
        f'curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/SM/setup.css',
        f'curl -sLo {IMG} https://github.com/gutris1/segsmaker/raw/main/script/SM/loading.png',
        f'curl -sLo {MRK} https://github.com/gutris1/segsmaker/raw/main/script/SM/marking.py'
    ]: SyS(cmd)

    load_css()
    display(multi_panel, output, loading)

CD(HOME)
multi_widgets()
