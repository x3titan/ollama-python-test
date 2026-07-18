import requests
from tamlib import fistalkIO
from tamlib.epageIO import EIO, EPageIO

"""
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


eio = EIO()
eio.append_string16("952D2750-8AE0-4EC7-BDBF-81799058789E")
eio.append_string16("T")
eio.append_string16("117354")
eio.append_string16("0")
epageServer = EPageIO("https://fistalk.com")
result = epageServer.post("/faith/pc/main", "showTopic", eio.buffo)
if result is None:
    exit(1)

if result.read_string8() != "T":
    exit(1)
ds = result.read_data_set()
contentLong = result.read_string16()
twitterDiv = fistalkIO.TwitterDiv()
fistalkIO.FistalkTaskset.loadTwitterRecord(twitterDiv, ds, 0)
if len(contentLong) > 0:
    twitterDiv.v_content.content = contentLong
print(twitterDiv.v_content.content)
print(twitterDiv.v_content.photo1)


if result:
    print("调用成功")
    # print(result.buffi)
else:
    print("调用失败")
"""


record = fistalkIO.FistalkTaskset.pullTwitterRecord("952D2750-8AE0-4EC7-BDBF-81799058789E", "117354")
if record is None:
    exit(1)
print(record.v_content.content)
print(record.v_userInfo.nickName)
