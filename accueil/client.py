counter = 0
@client_side
async def click(e):
    global counter
    counter += 1
    js.document.getElementById("count").innerText = str(counter)

element = js.document.getElementById("b1")
element.addEventListener("click", pyodide.ffi.create_proxy(click))