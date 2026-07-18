import time
from typing import Any


class ContentInfo:
    """
    对应 JavaScript 中的 g5.ContentInfo。

    依赖：
        g5.UserInfo
        ds.getData(column_index, row_index)
        ds.setData(column_index, row_index, value)
    """

    size = 20

    def __init__(self) -> None:
        self.id = "0"
        self.seconds = 0
        self.status = ""

        self.uplinkType = ""
        self.uplinkId = "0"

        self.content = ""
        self.longContent = False
        self.longContentText = ""

        self.photo1 = ""
        self.photo2 = ""
        self.photo3 = ""
        self.photo4 = ""

        self.clickCount = 0
        self.reCount = 0
        self.fwCount = 0
        self.likeCount = 0
        self.unlikeCount = 0

        self.isForward = False
        self.isLike = False
        self.isUnlike = False

        self.forceTopSn = "0"

        self.photos: list[str] = []

        self.exUserInfo = g5.UserInfo()
        self.exUplinkType = ""
        self.exContentId = "0"
        self.exIsForward = False
        self.exIsLike = False
        self.exIsUnlike = False

        self.startTime = 0

        self.init()

    @staticmethod
    def _to_int(value: Any, default: int = 0) -> int:
        """
        将数据转换成整数。

        对应 JavaScript 中：
            parseInt(value == "" ? "0" : value)

        与 JavaScript 不同的是，Python 在遇到 None 或非法字符串时
        不会抛出异常，而是返回 default。
        """
        if value is None or value == "":
            return default

        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def init(self) -> None:
        """
        初始化派生数据。

        1. 根据 photo1～photo4 构建 photos。
        2. 将计数字段转换为整数。
        3. 根据 seconds 计算 startTime。
        """
        if len(self.photos) <= 0:
            if self.photo1:
                self.photos.append(self.photo1)

            if self.photo2:
                self.photos.append(self.photo2)

            if self.photo3:
                self.photos.append(self.photo3)

            if self.photo4:
                self.photos.append(self.photo4)

        self.clickCount = self._to_int(self.clickCount)
        self.reCount = self._to_int(self.reCount)
        self.fwCount = self._to_int(self.fwCount)
        self.likeCount = self._to_int(self.likeCount)
        self.unlikeCount = self._to_int(self.unlikeCount)

        self.seconds = self._to_int(self.seconds)
        self.startTime = int(time.time()) - self.seconds

    def loadFromDataset(self, ds: Any, x: int, idx: int) -> None:
        """
        从 Dataset 的第 idx 行开始读取 ContentInfo 数据。

        参数：
            ds:
                提供 getData(column, row) 方法的 Dataset。
            x:
                起始列。
            idx:
                行索引。
        """
        p = x

        self.id = ds.getData(p, idx)
        p += 1

        self.seconds = ds.getData(p, idx)
        p += 1

        self.status = ds.getData(p, idx)
        p += 1

        self.uplinkType = ds.getData(p, idx)
        p += 1

        self.uplinkId = ds.getData(p, idx)
        p += 1

        self.content = ds.getData(p, idx)
        p += 1

        self.longContent = ds.getData(p, idx) == "T"
        p += 1

        self.photo1 = ds.getData(p, idx)
        p += 1

        self.photo2 = ds.getData(p, idx)
        p += 1

        self.photo3 = ds.getData(p, idx)
        p += 1

        self.photo4 = ds.getData(p, idx)
        p += 1

        self.clickCount = ds.getData(p, idx)
        p += 1

        self.reCount = ds.getData(p, idx)
        p += 1

        self.fwCount = ds.getData(p, idx)
        p += 1

        self.likeCount = ds.getData(p, idx)
        p += 1

        self.unlikeCount = ds.getData(p, idx)
        p += 1

        self.isForward = ds.getData(p, idx) == "1"
        p += 1

        self.isLike = ds.getData(p, idx) == "1"
        p += 1

        self.isUnlike = ds.getData(p, idx) == "1"
        p += 1

        self.forceTopSn = ds.getData(p, idx)

        self.init()

    def loadExFromDataset(self, ds: Any, x: int, idx: int) -> None:
        """
        从 Dataset 中读取附加信息。
        """
        self.exUserInfo = g5.UserInfo()
        self.exUserInfo.loadFromDataset(ds, x, idx)

        x += self.exUserInfo.size

        self.exUplinkType = ds.getData(x + 0, idx)
        self.exContentId = ds.getData(x + 1, idx)
        self.exIsForward = ds.getData(x + 2, idx) == "1"
        self.exIsLike = ds.getData(x + 3, idx) == "1"
        self.exIsUnlike = ds.getData(x + 4, idx) == "1"

    def setDataset(self, ds: Any, x: int, idx: int) -> None:
        """
        将当前对象写入 Dataset 的第 idx 行。

        参数：
            ds:
                提供 setData(column, row, value) 方法的 Dataset。
            x:
                起始列。
            idx:
                行索引。
        """
        p = x

        ds.setData(p, idx, self.id)
        p += 1

        ds.setData(p, idx, self.seconds)
        p += 1

        ds.setData(p, idx, self.status)
        p += 1

        ds.setData(p, idx, self.uplinkType)
        p += 1

        ds.setData(p, idx, self.uplinkId)
        p += 1

        ds.setData(p, idx, self.content)
        p += 1

        ds.setData(p, idx, "T" if self.longContent else "F")
        p += 1

        ds.setData(p, idx, self.photo1)
        p += 1

        ds.setData(p, idx, self.photo2)
        p += 1

        ds.setData(p, idx, self.photo3)
        p += 1

        ds.setData(p, idx, self.photo4)
        p += 1

        ds.setData(p, idx, self.clickCount)
        p += 1

        ds.setData(p, idx, self.reCount)
        p += 1

        ds.setData(p, idx, self.fwCount)
        p += 1

        ds.setData(p, idx, self.likeCount)
        p += 1

        ds.setData(p, idx, self.unlikeCount)
        p += 1

        ds.setData(p, idx, "1" if self.isForward else "0")
        p += 1

        ds.setData(p, idx, "1" if self.isLike else "0")
        p += 1

        ds.setData(p, idx, "1" if self.isUnlike else "0")
        p += 1

        ds.setData(p, idx, self.forceTopSn)

    def clone(self) -> "ContentInfo":
        """
        复制当前 ContentInfo 对象。

        与原 JavaScript 代码一致：
        exUserInfo 目前是浅复制，即两个 ContentInfo 可能引用同一个
        UserInfo 对象。
        """
        result = ContentInfo()

        result.id = self.id
        result.seconds = self.seconds
        result.status = self.status

        result.uplinkType = self.uplinkType
        result.uplinkId = self.uplinkId

        result.content = self.content
        result.longContent = self.longContent
        result.longContentText = self.longContentText

        result.photo1 = self.photo1
        result.photo2 = self.photo2
        result.photo3 = self.photo3
        result.photo4 = self.photo4

        result.clickCount = self.clickCount
        result.reCount = self.reCount
        result.fwCount = self.fwCount
        result.likeCount = self.likeCount
        result.unlikeCount = self.unlikeCount

        result.isForward = self.isForward
        result.isLike = self.isLike
        result.isUnlike = self.isUnlike

        result.forceTopSn = self.forceTopSn

        result.exUserInfo = self.exUserInfo
        result.exUplinkType = self.exUplinkType
        result.exContentId = self.exContentId
        result.exIsForward = self.exIsForward
        result.exIsLike = self.exIsLike
        result.exIsUnlike = self.exIsUnlike

        result.photos = self.photos.copy()

        result.init()

        # 原 JS clone() 会在 init() 后恢复原来的 startTime。
        result.startTime = self.startTime

        return result