from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint

sessions = {}
routes = {"/favicon.ico": ""}

pyodide_js = """ <script src="https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js"></script>"""
pyodide_script_start = """
<script>
async function main() {
  let pyodide = await loadPyodide();
  // Pyodide is now ready to use...
  pyodide.runPython(`"""

pyodide_script_end = """  `);
};
main();
</script>"""

HOST = "192.168.1.12"
PORT = 9999

def app_route(route):
    def inner(func):
        routes[route] = func()
    return inner

def open_file(path):
    return "\n" + open(path, "r").read() + "\n"

def return_template(src):
    html = ""
    html += pyodide_js
    print("t")
    html += pyodide_script_start
    html += open_file("client.py") # client.py of server before the client.py of page
    html += open_file(src + "client.py")
    html += pyodide_script_end

    html += open_file(src + "index.html")
    return html

class NeuralHTTP(BaseHTTPRequestHandler):

    def return_path(self):

        if self.path in routes:
            self.cookie = None  # Addition
            if self.cookie:
                self.send_header('Set-Cookie', self.cookie)  # Addition
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(routes[self.path], "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def do_GET(self): self.return_path()
    def do_POST(self): self.return_path()


@app_route("/")
def index():
   return return_template("page1/")


def generate_sid(self):
    return "".join(str(randint(1, 9)) for _ in range(100))

def parse_cookies(self, cookie_list):
    return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}


if __name__ == '__main__':
    server = HTTPServer((HOST, PORT), NeuralHTTP)
    print("Server now running...")
    server.serve_forever()
    server.server_close()
    print("Server stopped!")
