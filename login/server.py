# Password would normally be checked here
sid = generate_sid()
request.cookie = "sid={}".format(sid)
sessions[sid] = {"username", "useragent", "ip address", "expiry"}

def after():
    request.wfile.write(bytes("Logged In", "utf-8"))
