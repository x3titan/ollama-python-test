import requests
from pathlib import Path

from ollama import chat
from ollama import ChatResponse

from tamlib import fistalkIO
from tamlib.epageIO import EIO, EPageIO
from tamlib.fistalkIO import FistalkTaskset, ContentInfo, UserInfo, TwitterDiv


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


# record = fistalkIO.FistalkTaskset.pullTwitterRecord("952D2750-8AE0-4EC7-BDBF-81799058789E", "117354")
# record = fistalkIO.FistalkTaskset.pullTwitterRecord("952D2750-8AE0-4EC7-BDBF-81799058789E", "118767")
record = fistalkIO.FistalkTaskset.pullTwitterRecord("952D2750-8AE0-4EC7-BDBF-81799058789E", "118766")

if record is None:
    exit(1)
print("========== Content ==========")
print(record.v_content.content)
print("photo1=" + record.v_content.photo1)
print("nickName=" + record.v_userInfo.nickName)
photoContent = "无"
if (len(record.v_content.photo1)>0):
    project_dir = Path.cwd()
    save_file = project_dir / "temp" / "contentPhoto1.jpg"
    FistalkTaskset.downloadPhoto(record.v_content.photo1, save_file)

    print("========== OCR Start ==========")
    response: ChatResponse = chat(
        model="qwen2.5vl:7b",
        messages=[
            {
                "role": "system",
                "content": ("你是一个OCR识别助手。" "请识别图片中的所有文字。" "不要解释，不要总结，不要添加任何额外内容。" "保持原有顺序输出即可。"),
            },
            {
                "role": "user",
                "content": "识别图片中的全部文字。",
                "images": [str(save_file)],
            },
        ],
    )
    photoContent = response.message.content
    print(response.message.content)


prompt = f"""
你现在是一名社交媒体用户。

下面是一条帖子：

发帖人：
{record.v_userInfo.nickName}

帖子正文：
{record.v_content.content}

图片文字：
{photoContent}

要求：

1. 根据正文和图片内容回复。
2. 回复自然，像真人。
3. 不要解释。
4. 不要输出分析过程。
5. 只输出回复内容。
对此贴发出提问
"""

response: ChatResponse = chat(model="qwen3:4b", messages=[{"role": "system", "content": "你是一位中文社交媒体用户。"}, {"role": "user", "content": prompt}])

reply = response.message.content.strip()

print("========== AI回复 ==========")
print(reply)
