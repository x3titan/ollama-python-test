import random

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

from tamlib.tamPub import TamPub

# tokenAdmin = FistalkTaskset.loginAdmin("argon2", "111111")
tokenAdmin = "43EEA795-B912-499F-80EC-F214CEC136C2"
contentIdList = FistalkTaskset.getContentIdList(tokenAdmin, 0, 10)
if contentIdList is None:
    exit(1)
# for i in range(contentIdList.row_count):
#     print(contentIdList.get_data(0,i))

aiUserList = FistalkTaskset.getAIUserList(tokenAdmin, 0, 10000)
if aiUserList is None:
    exit(1)
# for i in range(aiUserList.row_count):
#     print(aiUserList.get_data(1, i))

# decide content and user(reply)
contentId = contentIdList.get_data(0, 2)
aiUserIndex = random.randint(0, aiUserList.row_count - 1)
aiUsername = aiUserList.get_data(1, aiUserIndex)
print(f"========== 准备回复帖子 {contentId}, AI用户 {aiUsername}, {aiUserList.get_data(2,aiUserIndex)},序号:{aiUserIndex} ==========")


aiToken = FistalkTaskset.getTokenByUsername(tokenAdmin, aiUsername)
record = fistalkIO.FistalkTaskset.pullTwitterRecord(aiToken, contentId)
if record is None:
    exit(1)
print("========== Content ==========")
print(record.v_content.content)
print("photo1=" + record.v_content.photo1)
print("nickName=" + record.v_userInfo.nickName)
photoContent = "无"
if len(record.v_content.photo1) > 0:
    project_dir = Path.cwd()
    save_file = project_dir / "temp" / "contentPhoto1.jpg"
    FistalkTaskset.downloadPhoto(record.v_content.photo1, str(save_file))

    # print("========== OCR Start ==========")
    response: ChatResponse = chat(
        model="qwen2.5vl:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个OCR识别助手。"
                    "请识别图片中的所有文字，以及图片展示的内容。"
                    "不要解释，不要总结，不要添加任何额外内容。"
                    "保持原有顺序输出即可。"
                ),
            },
            {
                "role": "user",
                "content": "识别图片中的全部文字，以及图片展示的内容。",
                "images": [str(save_file)],
            },
        ],
    )
    photoContent = response.message.content
    print(f"识别图片文字：{response.message.content}")

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
6. 输出{TamPub.random_string({"10": 50, "20": 40, "30": 30, "100": 10, "180": 10, "400": 5})}字左右。
7. 对贴子的内容表示{TamPub.random_string({"赞成": 50, "反对": 5, "随便说说的平和态度": 50})}。
8. 目前的心情：{TamPub.random_string({"平和": 50, "开心": 50, "沮丧": 10, "失望": 10, "愤怒": 5, "调侃": 50})}。
9. 回帖以{TamPub.random_string({"正常": 50, "提问": 10, "解释": 10, "无厘头": 20})}的形式。
"""
# 你的履历和性格特征如下,这些只作为性格参考，回复不要直接提及以下内容，不要说自己在哪里干什么这种隐私问题，如果要多说话就问题展开讨论就好了：
# {aiUserList.get_data(4,aiUserIndex)}
print("========== AI发帖规范 ==========")
print(prompt)

response: ChatResponse = chat(model="qwen3:4b", messages=[{"role": "system", "content": "你是一位中文社交媒体用户。"}, {"role": "user", "content": prompt}])

reply = (response.message.content or "").strip()

print("========== AI回复 ==========")
print(reply)

FistalkTaskset.follow(aiToken, record.v_userInfo.id)

r = FistalkTaskset.newTwitterV2(aiToken, reply, "R", contentId)
