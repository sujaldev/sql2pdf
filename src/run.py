import os
from src.GUI.gui import Gui


def launch_window(self):
    print(self.root)
    os.system(f"google-chrome --app={self.root}")


gui = Gui(port=1234, runtime_funcs=launch_window)
