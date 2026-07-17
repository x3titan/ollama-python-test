import requests
from tamlib.eio import EIO
from tamlib.epageIO import EPageIO

eio = EIO()
eio.append_string16("952D2750-8AE0-4EC7-BDBF-81799058789E")
epageServer = EPageIO("https://fistalk.com")
result = epageServer.post(
    "/faith/pc/main",
    "getUserInfo",
    eio.buffo
)

if result:
    print("调用成功")
    print(result.buffi)
else:
    print("调用失败")
