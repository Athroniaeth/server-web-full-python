from http.server import *
from random import randint

HOST = "192.168.1.12"
PORT = 9999

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

request = None
handler = None
sessions = {}

routes = {
    "/favicon.ico": ""
}

def generate_sid():
    return "".join(str(randint(1, 9)) for _ in range(100))

def open_file(path):
    return "\n" + open(path, "r").read() + "\n"

def app_route(route):
    def inner(func):
        routes[route] = func
    return inner

def return_template(src):
    global request
    global handler
    ex_locals = {}

    if request is None: return ""

    src += "/"

    html = ""
    html += pyodide_js
    exec(open_file(src + "server.py"), None, ex_locals)
    print(ex_locals)
    html += pyodide_script_start
    html += open_file("client.py") # client.py of server before the client.py of page
    html += open_file(src + "client.py")
    html += pyodide_script_end

    html += open_file(src + "index.html")
    return html, ex_locals["after"]

class SessionHandler(BaseHTTPRequestHandler):

    def do_GET(self): self.return_path()
    def do_POST(self): self.return_path()

    def return_path(self):
        global request

        if self.path in routes:
            response = 200
            self.cookie = None  # Addition

            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.user = cookies["sid"] if (cookies["sid"] in sessions) else False
            else:
                self.user = False

            request = self
            content, after_func = routes[self.path]()

            self.send_response(response)
            self.send_header('Content-type', 'text/html')
            if self.cookie: self.send_header('Set-Cookie', self.cookie)
            self.end_headers()

            after_func()
            self.wfile.write(bytes(content, "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def parse_cookies(self, cookie_list):
            return dict(((c.split("=")) for c in cookie_list.split(";"))) \
                if cookie_list else {}

@app_route("/")
def home():
    return return_template("accueil")

@app_route("/login")
def home2():
    return return_template("login")

@app_route("/logout")
def home3():
    return return_template("logout")

    # + "Welcome User!" if self.user else "Welcome Stranger!"
        # return "Welcome User!" if self.user else "Welcome Stranger!"

    #@app_route("/login")
    #def login(self):
    #    # Password would normally be checked here
    #    sid = self.generate_sid()
    #    self.cookie = "sid={}".format(sid)
    #    sessions[sid] = {"username", "useragent", "ip address", "expiry"}
    #    return "Logged In"
#
    #@app_route("/logout")
    #def logout(self):
    #    if not self.user:
    #        return "Can't Log Out: No User Logged In"
#
    #    self.cookie = "sid="
    #    del sessions[self.user]
    #    return "Logged Out"

handler = SessionHandler
server = HTTPServer((HOST, PORT), handler)
print("Server now running...")
server.serve_forever()
server.server_close()
print("Server stopped!")