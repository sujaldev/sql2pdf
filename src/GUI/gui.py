import os
import pdfkit
from src.backend.gen_html import *
from lib.server.superdraco import *
from src.GUI.gui_templates import *
from lib.server.url_parse import percent_decode


class Gui(Server):
    def __init__(self, host="127.0.0.1", port=0, runtime_funcs=None):
        super().__init__(host=host, port=port, runtime_funcs=runtime_funcs)

    def routes(self):
        return {
            "/": self.home,
            "/genpdf": self.generate_pdf,
            "/genhtml": self.generate_html
        }

    def home(self):
        request = self.request
        return f"HTTP 1.1/ 200 OK\n\n{home_gui}"

    def generate_html(self):
        data = self.parse_http()
        html = gen_html(percent_decode(data["headers"]["query"]), password=percent_decode(data["headers"]["password"]))
        return f"HTTP 1.1/ 200 OK\n\n{html}"

    def generate_pdf(self):
        self.encode = False
        file_name = f'{self.parse_http()["headers"]["heading"]}.pdf'.encode("utf8")
        with open("./temp.html", "w") as f:
            f.write(self.generate_html().replace("HTTP 1.1/ 200 OK\n\n", ""))
        with open("./temp.html", "r") as f:
            pdfkit.from_file(f, "temp.pdf")
        with open("./temp.pdf", "rb") as f:
            pdf = f.read()
        os.remove("./temp.html")
        os.remove("./temp.pdf")
        h = b"""HTTP/1.1 200 OK\nContent-Type: application/pdf\nContent-Disposition: attachment; filename="%f%\n\n%p%"""
        h = h.replace(b"%f%", file_name).replace(b"%p%", pdf)
        return h
