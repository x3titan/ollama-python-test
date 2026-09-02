import math
import random

from pathlib import Path

from ollama import chat
from ollama import ChatResponse

from tamlib import fistalkIO
from tamlib.epageIO import EIO, EDataSet, EPageIO
from tamlib.fistalkIO import FistalkTaskset, ContentInfo, UserInfo, TwitterDiv

from tamlib.tamPub import TamPub

# tokenAdmin = FistalkTaskset.loginAdmin("argon2", "111111")
tokenAdmin = "43EEA795-B912-499F-80EC-F214CEC136C2"
contentIdList = FistalkTaskset.getContentIdList(tokenAdmin, 0, 20)
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
contentId = contentIdList.get_data(0, random.randint(0, contentIdList.row_count - 1))
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
if record.v_content.photo1 and not record.v_content.photo1.startswith("?"):
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
                    "你是一个OCR识别助手。" "请识别图片中的所有文字，以及图片展示的内容。" "不要解释，不要总结，不要添加任何额外内容。" "保持原有顺序输出即可。"
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
图片文字及内容：
{photoContent}
要求：
1. 根据正文和图片内容输出一个回复策略。
2. 回复自然，像真人。
3. 不要解释。
4. 不要输出分析过程。

输出格式：
1. 对贴子的内容表示：赞成/反对/随便说说/理性分析/深入分析等等（根据帖子的内容决定，要有一定的随机性）。
2. 目前的情绪：正常/开心/沮丧/失望/愤怒/调侃等(根据帖子的内容决定，要有一定的随机性)。
3. 回帖的形式：正常/提问/解释/无厘头等(根据帖子的内容决定，要有一定的随机性)。
以上内容要带标号和冒号前面的部分，比如: 1. 对贴子的内容表示：反对
"""
# 你的履历和性格特征如下,这些只作为性格参考，回复不要直接提及以下内容，不要说自己在哪里干什么这种隐私问题，如果要多说话就问题展开讨论就好了：
# {aiUserList.get_data(4,aiUserIndex)}
print("========== AI发帖规范 ==========")
print(prompt)

response: ChatResponse = chat(model="qwen3:4b", messages=[{"role": "system", "content": "你是一位中文社交媒体用户。"}, {"role": "user", "content": prompt}])

reply = (response.message.content or "").strip()
print("========== AI回复策略 ==========")
print(reply)

# 计算回复字数
replyLength = len(record.v_content.content) + len(photoContent)
replyLength = max(15,replyLength)
replyLength = min(400, replyLength)
replyLength = TamPub.random_hyperbolic_int(
    10,
    replyLength,
    100,
    5,
    4
)

# 产生回复
prompt = f"""
你现在是一名社交媒体用户。
下面是一条帖子：
发帖人：
{record.v_userInfo.nickName}
帖子正文：
{record.v_content.content}
图片文字及内容：
{photoContent}
要求：
1. 根据正文和图片内容回复。
2. 回复自然，像真人。
3. 不要解释。
4. 不要输出分析过程。
5. 只输出回复内容，特别是尾部不要有(178字)这种东西。
6. 回答的最好有智慧和深度
另外要求：
{reply}
4. 输出{replyLength}字左右。
"""
# 你的履历和性格特征如下,这些只作为性格参考，回复不要直接提及以下内容，不要说自己在哪里干什么这种隐私问题，如果要多说话就问题展开讨论就好了：
# {aiUserList.get_data(4,aiUserIndex)}
# 6. 输出{TamPub.random_string({"10": 50, "20": 40, "30": 30, "100": 10, "180": 10, "400": 5})}字左右。
# 7. 对贴子的内容表示{TamPub.random_string({"赞成": 50, "反对": 5, "随便说说的平和态度": 50})}。
# 8. 目前的心情：{TamPub.random_string({"平和": 50, "开心": 50, "沮丧": 10, "失望": 10, "愤怒": 5, "调侃": 50})}。
# 9. 回帖以{TamPub.random_string({"正常": 50, "提问": 10, "解释": 10, "无厘头": 20})}的形式。
print("========== AI发帖规范 ==========")
print(prompt)

response: ChatResponse = chat(model="qwen3:4b", messages=[{"role": "system", "content": "你是一位中文社交媒体用户。"}, {"role": "user", "content": prompt}])

reply = (response.message.content or "").strip()

print("========== AI回复 ==========")
print(reply)

FistalkTaskset.follow(aiToken, record.v_userInfo.id)

r = FistalkTaskset.newTwitterV2(aiToken, reply, "R", contentId)
