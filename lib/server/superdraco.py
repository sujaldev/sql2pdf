import socket
from lib.server.url_parse import *


class Server:
    def __init__(self, host="127.0.0.1", port=0, runtime_funcs=None):
        self.host = host
        self.port = port
        self.runtime_funcs = runtime_funcs
        self.route_dict = self.routes()
        self.request = ""

        self.encode = True  # disables encoding for only one request if set to False

        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.root = f"http://{self.host}:{self.sock.getsockname()[1]}"
        print(f"SERVER UP AND RUNNING AT {self.root}/")
        self.run_server()

    def routes(self):
        return {
            "/": self.default_home
        }

    def default_home(self):
        html = f"""HTTP 1.1/ 200 OK

<!DOCTYPE html>
<html>
<head>
    <title>Success!</title>
</head>
<body>
    <h1>SUPERDRACO SERVER UP AND RUNNING AT {self.host} ON PORT {self.port}!</h1>
</body>
</html>"""
        return html

    def unsupported_feature(self):
        request = self.request
        html = f"""HTTP 1.1/ 200 OK

<!DOCTYPE html>
<html>
<head>
    <title>ERROR - UNSUPPORTED FEATURE</title>
</head>
<body>
    <h1>THIS FEATURES IS NOT SUPPORTED YET! SERVER RECEIVED THE FOLLOWING REQUEST<br></h1>
    <p>{request}</p>
</body>
</html>"""
        return html

    def http_404(self):
        request = self.request
        html = f"""HTTP 1.1/ 404 bad request

<!DOCTYPE html>
<html>
<head>
    <title>ERROR 404</title>
</head>
<body>
    <h1>ERROR 404 - PAGE NOT FOUND! SERVER RECEIVED THE FOLLOWING REQUEST:<br></h1>
    <p>{request}</p>
</body>
</html>"""
        return html

    def parse_http(self):
        query = self.request
        http_params = query.split("\n")
        http_req = http_params[0].split(" ")
        method = http_req[0]
        url_data = extract_params(http_req[1])
        path = url_data[0]
        headers = url_data[1]
        http_version = http_req[2]
        print(method, path, http_version)
        return {
            "method": method,
            "path": path,
            "http_version": http_version,
            "headers": headers,
            "params": http_params[1:]
        }

    def run_server(self):
        if self.runtime_funcs is not None:
            print("found function")
            self.runtime_funcs(self)
        while True:
            client_sock, client_address = self.sock.accept()
            req = client_sock.recv(1024)
            self.request = req.decode()
            query_dict = self.parse_http()
            if query_dict["method"] == "GET":
                if query_dict["path"] in self.route_dict.keys():
                    response = self.route_dict[query_dict["path"]]()
                    if self.encode:
                        response = bytes(response, "utf8")
                    else:
                        self.encode = True
                    client_sock.send(response)
                elif query_dict["path"] == "/superdraco-burnout":
                    client_sock.close()
                    break
                else:
                    client_sock.send(bytes(self.http_404(), "utf8"))
            else:
                client_sock.send(bytes(self.unsupported_feature(), "utf8"))
            client_sock.close()
