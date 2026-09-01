import requests
from pathlib import Path

from ollama import chat
from ollama import ChatResponse

from tamlib import fistalkIO
from tamlib.epageIO import EIO, EDataSet, EPageIO
from tamlib.fistalkIO import FistalkTaskset, ContentInfo, UserInfo, TwitterDiv


# token = FistalkTaskset.getTokenByUsername("aaa", "96E79218965EB72C92A549DD5A330112", "yangcongbing")
# if (len(token)<=0):
#     print("can not get token")
#     exit(1)
# print ("get token: " + token)

# newFilename = FistalkTaskset.uploadImage(
#     token, "D:\\temp\\AIUserInfo\\f46c5971-fe0c-4845-8810-777f1ead5cfe.png", FistalkTaskset.UploadImageFunction.SET_PHOTO
# )
# print("userPhoto: " + newFilename)

# newFilename = FistalkTaskset.uploadImage(
#     token, "D:\\temp\\AIUserInfo\\f46c5971-fe0c-4845-8810-777f1ead5cfe.png", FistalkTaskset.UploadImageFunction.SET_TITLE_BG
# )
# print("titleBg: " + newFilename)


# # FistalkTaskset.uploadImage()
# exit(0)


import os

# tokenAdmin = FistalkTaskset.loginAdmin("argon2", "111111")
tokenAdmin = "43EEA795-B912-499F-80EC-F214CEC136C2"
contentIdList = FistalkTaskset.getContentIdList(tokenAdmin, 0, 10)
if (contentIdList is None):
    exit(1)
for i in range(contentIdList.row_count):
    print(contentIdList.get_data(0,i))

aiUserList = FistalkTaskset.getAIUserList(tokenAdmin, 0, 10000)
if aiUserList is None:
    exit(1)
for i in range(aiUserList.row_count):
    print(aiUserList.get_data(1, i))


exit(0)

#####批量上传头像以及背景图
# 图片所在目录
IMAGE_DIR = r"D:\temp\AIUserInfo"

# 建议将密钥放进环境变量，避免直接写在代码中
APP_NAME = "aaa"
APP_SECRET = "96E79218965EB72C92A549DD5A330112"

users = [
    "xuegaobujia",
    "mangguobuding",
    "woshikongqi",
    "calgaryyu",
    "newyorkpan",
    "perthli",
    "aucklandhe",
    "seoulzhou",
    "parislin",
    "berlinyao",
    "dubaichen",
    "bostonwu",
    "kyotofeng"
]

success_count = 0
failed_items = []

for user_name in users:
    print(f"\n开始处理账号：{user_name}")

    try:
        token = FistalkTaskset.getTokenByUsername(APP_NAME, APP_SECRET, user_name)

        if not token:
            raise RuntimeError("无法获取 token")

        avatar_path = os.path.join(IMAGE_DIR, f"{user_name}_avatar.png")

        header_path = os.path.join(IMAGE_DIR, f"{user_name}_header.png")

        if not os.path.isfile(avatar_path):
            raise FileNotFoundError(f"头像文件不存在：{avatar_path}")

        if not os.path.isfile(header_path):
            raise FileNotFoundError(f"题头文件不存在：{header_path}")

        # 上传头像
        avatar_filename = FistalkTaskset.uploadImage(token, avatar_path, FistalkTaskset.UploadImageFunction.SET_PHOTO)

        print(f"头像上传成功：{avatar_filename}")

        # 上传题头背景
        header_filename = FistalkTaskset.uploadImage(token, header_path, FistalkTaskset.UploadImageFunction.SET_TITLE_BG)

        print(f"题头上传成功：{header_filename}")
        success_count += 1

    except Exception as error:
        print(f"账号 {user_name} 上传失败：{error}")

        failed_items.append({"userName": user_name, "error": str(error)})

print("\n========== 上传结束 ==========")
print(f"账号总数：{len(users)}")
print(f"成功账号：{success_count}")
print(f"失败账号：{len(failed_items)}")

if failed_items:
    print("\n失败明细：")

    for item in failed_items:
        print(f"- {item['userName']}：{item['error']}")

exit(0)

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


aiToken = "952D2750-8AE0-4EC7-BDBF-81799058789E"
# contentId = "118766"
# contentId = "117354"
# contentId = "118767"
contentId = "118546"
record = fistalkIO.FistalkTaskset.pullTwitterRecord(aiToken, contentId)

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
    FistalkTaskset.downloadPhoto(record.v_content.photo1, str(save_file))

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
7. 输出200字左右
8. 表现的冷酷一点
"""
# 6. 对此贴发出提问

response: ChatResponse = chat(model="qwen3:4b", messages=[{"role": "system", "content": "你是一位中文社交媒体用户。"}, {"role": "user", "content": prompt}])

reply = (response.message.content or "").strip()

print("========== AI回复 ==========")
print(reply)

r = FistalkTaskset.newTwitterV2(aiToken, reply, "R", contentId)
print(f"========== 发帖 {'success' if r else 'fail'} ==========")
