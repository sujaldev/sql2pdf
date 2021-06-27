from lib.server.superdraco import *


class Pdf(Server):
    def routes(self):
        return {
            "/": self.pdf_view
        }

    def pdf_view(self):
        self.encode = False
        with open("./feynman.pdf", "rb") as f:
            data = f.read()
        header = b"""HTTP/1.1 200 OK\r\nDate: Sun, 27 Jun 2021 03:28:56 GMT\r\nServer: Apache\r\nLast-Modified: Tue, 22 Aug 2006 00:20:13 GMT\r\nETag: "240096-41b9030b12940"\r\nAccept-Ranges: bytes\r\nContent-Length: 2359446\r\nContent-Type: application/pdf\r\n\r\n"""
        new_header = b"""HTTP/1.1 200 OK\r\nContent-Type: application/pdf\r\nContent-Disposition: attachment\r\n\r\n"""
        data = data.replace(header, new_header)
        print(data[:1000])
        return data


Pdf()
