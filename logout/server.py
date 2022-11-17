if not request.user:
    request.wfile.write(bytes("Can't Log Out: No User Logged In", "utf-8"))
else:
    request.cookie = "sid="
    del sessions[request.user]

def after():
    if request.user:
        request.wfile.write(bytes("Logged Out", "utf-8"))
