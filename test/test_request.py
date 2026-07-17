import requests
from tamlib import EIO, EPageIO

eio = EIO()
eio.append_byte(1)
eio.append_word(100)
eio.append_string16("测试数据")

packed_data = writer.get_output()

print("打包结果：", packed_data)

url = "https://fistalk.com"
try:
    response = requests.get(url, timeout=10)

    print("HTTP状态码：", response.status_code)
    print()

    print("返回内容：")
    response.encoding = "utf-8"
    #print(response.text)

except Exception as e:
    print(e)