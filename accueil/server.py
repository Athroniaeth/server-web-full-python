def after():
    if request.user:
        request.wfile.write(bytes("Connecté", "utf-8"))