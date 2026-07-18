import time
from tokenize import String
from typing import Any
from .epageIO import EDataSet, EIO, EPageIO
from types import SimpleNamespace


class ContentInfo:
    """
    对应 JavaScript 中的 g5.ContentInfo。

    依赖：
        g5.UserInfo
        ds.get_data(column_index, row_index)
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

        self.exUserInfo = UserInfo()
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

    def loadFromDataset(self, ds: EDataSet, x: int, idx: int) -> None:
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

        self.id = ds.get_data(p, idx)
        p += 1

        self.seconds = ds.get_data(p, idx)
        p += 1

        self.status = ds.get_data(p, idx)
        p += 1

        self.uplinkType = ds.get_data(p, idx)
        p += 1

        self.uplinkId = ds.get_data(p, idx)
        p += 1

        self.content = ds.get_data(p, idx)
        p += 1

        self.longContent = ds.get_data(p, idx) == "T"
        p += 1

        self.photo1 = ds.get_data(p, idx)
        p += 1

        self.photo2 = ds.get_data(p, idx)
        p += 1

        self.photo3 = ds.get_data(p, idx)
        p += 1

        self.photo4 = ds.get_data(p, idx)
        p += 1

        self.clickCount = ds.get_data(p, idx)
        p += 1

        self.reCount = ds.get_data(p, idx)
        p += 1

        self.fwCount = ds.get_data(p, idx)
        p += 1

        self.likeCount = ds.get_data(p, idx)
        p += 1

        self.unlikeCount = ds.get_data(p, idx)
        p += 1

        self.isForward = ds.get_data(p, idx) == "1"
        p += 1

        self.isLike = ds.get_data(p, idx) == "1"
        p += 1

        self.isUnlike = ds.get_data(p, idx) == "1"
        p += 1

        self.forceTopSn = ds.get_data(p, idx)

        self.init()

    def loadExFromDataset(self, ds: EDataSet, x: int, idx: int) -> None:
        """
        从 Dataset 中读取附加信息。
        """
        self.exUserInfo = UserInfo()
        self.exUserInfo.loadFromDataset(ds, x, idx)

        x += self.exUserInfo.size

        self.exUplinkType = ds.get_data(x + 0, idx)
        self.exContentId = ds.get_data(x + 1, idx)
        self.exIsForward = ds.get_data(x + 2, idx) == "1"
        self.exIsLike = ds.get_data(x + 3, idx) == "1"
        self.exIsUnlike = ds.get_data(x + 4, idx) == "1"

    def setDataset(self, ds: EDataSet, x: int, idx: int) -> None:
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


class UserInfo:
    """
    对应 JavaScript 中的 g5.UserInfo。

    Dataset 字段数量：
        19
    """

    size: int = 19

    def __init__(self) -> None:
        self.id: str = "0"
        self.status: str = ""

        self.regDatetime: Any = ""
        self.lastAccessTime: Any = ""

        self.userName: str = ""
        self.mobile: str = ""
        self.nickName: str = ""
        self.note: str = ""

        self.photo: str = ""
        self.titleBg: str = ""
        self.homePage: str = ""

        self.followCount: Any = 0
        self.fansCount: Any = 0
        self.postCount: Any = 0

        self.follow: str = "0"
        self.block1: str = "0"
        self.block2: str = "0"

        self.email: str = ""

        self.isFollow: bool = False
        self.isBlock1: bool = False
        self.isBlock2: bool = False
        self.isHide: bool = False

    def loadFromDataset(
        self,
        ds: EDataSet,
        x: int,
        idx: int,
    ) -> None:
        """
        从 EDataSet 的指定行读取用户信息。

        参数：
            ds:
                数据集。
            x:
                起始列索引。
            idx:
                行索引。
        """
        self.id = ds.get_data(x + 0, idx)
        self.status = ds.get_data(x + 1, idx)

        self.regDatetime = self.getUtcTime(
            ds.get_data(x + 2, idx),
            True,
        )

        self.lastAccessTime = ds.get_data(x + 3, idx)
        self.userName = ds.get_data(x + 4, idx)
        self.mobile = ds.get_data(x + 5, idx)
        self.nickName = ds.get_data(x + 6, idx)
        self.note = ds.get_data(x + 7, idx)
        self.photo = ds.get_data(x + 8, idx)
        self.titleBg = ds.get_data(x + 9, idx)
        self.homePage = ds.get_data(x + 10, idx)
        self.followCount = ds.get_data(x + 11, idx)
        self.fansCount = ds.get_data(x + 12, idx)
        self.postCount = ds.get_data(x + 13, idx)
        self.follow = ds.get_data(x + 14, idx)
        self.block1 = ds.get_data(x + 15, idx)
        self.block2 = ds.get_data(x + 16, idx)
        self.email = ds.get_data(x + 17, idx)

        self.isFollow = self.follow == "1"
        self.isBlock1 = self.block1 == "1"
        self.isBlock2 = self.block2 == "1"
        self.isHide = ds.get_data(x + 18, idx) == "1"

    def setDataset(
        self,
        ds: EDataSet,
        x: int,
        idx: int,
    ) -> None:
        """
        将当前用户信息写入 EDataSet。
        """
        ds.setData(x + 0, idx, self.id)
        ds.setData(x + 1, idx, self.status)
        ds.setData(x + 2, idx, self.regDatetime)
        ds.setData(x + 3, idx, self.lastAccessTime)
        ds.setData(x + 4, idx, self.userName)
        ds.setData(x + 5, idx, self.mobile)
        ds.setData(x + 6, idx, self.nickName)
        ds.setData(x + 7, idx, self.note)
        ds.setData(x + 8, idx, self.photo)
        ds.setData(x + 9, idx, self.titleBg)
        ds.setData(x + 10, idx, self.homePage)
        ds.setData(x + 11, idx, self.followCount)
        ds.setData(x + 12, idx, self.fansCount)
        ds.setData(x + 13, idx, self.postCount)
        ds.setData(x + 14, idx, self.follow)
        ds.setData(x + 15, idx, self.block1)
        ds.setData(x + 16, idx, self.block2)
        ds.setData(x + 17, idx, self.email)
        ds.setData(x + 18, idx, "1" if self.isHide else "0")

    def clone(self) -> "UserInfo":
        """
        创建当前 UserInfo 的副本。

        当前字段均为字符串、数字、布尔值等简单类型，
        因此浅复制即可。
        """
        return copy(self)

    @staticmethod
    def getUtcTime(value: Any, local_time: bool = True) -> Any:
        """
        对应 JavaScript 中的：

            g5.getUtcTime(value, true)

        目前先原样返回。

        等你把原 JavaScript 的 getUtcTime() 函数提供出来后，
        再将这里改为准确的时间转换逻辑。
        """
        return value


class TwitterDiv:
    def __init__(self):
        self.v_content = ContentInfo()
        self.v_reContent = ContentInfo()
        self.v_userInfo = UserInfo()
        self.v_reUserInfo = UserInfo()


class FistalkTaskset:
    URL = "https://fistalk.com"

    @staticmethod
    def loadTwitterRecord(
        twitterDiv: TwitterDiv,
        dataset: EDataSet,
        index: int,
    ) -> None:
        """
        从 dataset 的指定记录中读取一条 Twitter 内容数据，
        并将结果保存到 panel 对象。

        对应 JavaScript：
            loadTwitterRecord(panel, dataset, index)
        """
        twitterDiv.v_content = ContentInfo()
        twitterDiv.v_reContent = ContentInfo()
        twitterDiv.v_userInfo = UserInfo()
        twitterDiv.v_reUserInfo = UserInfo()

        dx = 0

        twitterDiv.v_content.loadFromDataset(dataset, dx, index)
        dx += twitterDiv.v_content.size

        twitterDiv.v_reContent.loadFromDataset(dataset, dx, index)
        dx += twitterDiv.v_reContent.size

        twitterDiv.v_userInfo.loadFromDataset(dataset, dx, index)
        dx += twitterDiv.v_userInfo.size

        twitterDiv.v_reUserInfo.loadFromDataset(dataset, dx, index)
        dx += twitterDiv.v_reUserInfo.size

        twitterDiv.v_content.loadExFromDataset(dataset, dx, index)

        if twitterDiv.v_content.uplinkType == "L":
            temp = twitterDiv.v_content.uplinkType
            twitterDiv.v_content.uplinkType = twitterDiv.v_content.exUplinkType
            twitterDiv.v_content.exUplinkType = temp

            temp = twitterDiv.v_userInfo
            twitterDiv.v_userInfo = twitterDiv.v_content.exUserInfo
            twitterDiv.v_content.exUserInfo = temp

            twitterDiv.v_content.isForward = twitterDiv.v_content.exIsForward
            twitterDiv.v_content.isLike = twitterDiv.v_content.exIsLike
            twitterDiv.v_content.isUnlike = twitterDiv.v_content.exIsUnlike

    @staticmethod
    def pullTwitterRecord(token: str, contentId: str) -> TwitterDiv:
        eio = EIO()
        eio.append_string16(token)
        eio.append_string16("T")
        eio.append_string16(contentId)
        eio.append_string16("0")
        epageServer = EPageIO(FistalkTaskset.URL)
        result = epageServer.post("/faith/pc/main", "showTopic", eio.buffo)

        if result is None:
            return None

        if result.read_string8() != "T":
            return None

        ds = result.read_data_set()
        contentLong = result.read_string16()
        twitterDiv = TwitterDiv()
        FistalkTaskset.loadTwitterRecord(twitterDiv, ds, 0)
        if len(contentLong) > 0:
            twitterDiv.v_content.content = contentLong

        return twitterDiv
