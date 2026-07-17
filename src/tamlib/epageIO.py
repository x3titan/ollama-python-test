from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests

from .eio import EIO


class EPageIOError(Exception):
    """EPage通信基础异常。"""


class EPageConnectionError(EPageIOError):
    """无法连接EPage服务器。"""


class EPageTimeoutError(EPageIOError):
    """EPage请求超时。"""


class EPageHTTPError(EPageIOError):
    """EPage服务器返回了异常HTTP状态码。"""

    def __init__(
        self,
        status_code: int,
        url: str,
        response_text: str,
    ) -> None:
        self.status_code = status_code
        self.url = url
        self.response_text = response_text

        super().__init__(
            f"EPage请求失败，HTTP状态码：{status_code}，URL：{url}"
        )


class EPageIO:
    """
    用于与EPage服务器进行HTTP/HTTPS通信。

    URL格式：

        base_url + page_name + "?_T_=" + taskset_name

    示例：

        base_url:
            https://fistalk.com

        page_name:
            /main/page1

        taskset_name:
            taskset1

        最终URL:
            https://fistalk.com/main/page1?_T_=taskset1

    请求时发送 eio.buffo。
    返回结果写入 eio.buffi，并将 eio.sp 重置为 0。
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        encoding: str = "utf-8",
        verify_ssl: bool = True,
        headers: dict[str, str] | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url不能为空")

        if not base_url.startswith(("http://", "https://")):
            base_url = "https://" + base_url

        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.encoding = encoding
        self.verify_ssl = verify_ssl

        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "text/plain; charset=utf-8",
            "Accept": "text/plain, */*",
            "User-Agent": "tamlib-epage-client/0.1",
        })

        if headers:
            self.session.headers.update(headers)

    def build_url(
        self,
        page_name: str,
        taskset_name: str,
    ) -> str:
        """根据页面名称和任务集名称生成请求URL。"""

        if not page_name:
            raise ValueError("page_name不能为空")

        if not taskset_name:
            raise ValueError("taskset_name不能为空")

        normalized_page_name = page_name.lstrip("/")

        url = urljoin(
            self.base_url,
            normalized_page_name,
        )

        return url

    def post(
        self,
        page_name: str,
        taskset_name: str,
        post_data: str,
        *,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> str:
        """
        向EPage服务器发送字符串，并返回服务器响应字符串。

        post_data会作为原始HTTP请求正文发送。
        """

        url = self.build_url(page_name, taskset_name)

        request_timeout = (
            self.timeout
            if timeout is None
            else timeout
        )

        try:
            response = self.session.post(
                url,
                params={
                    "_T_": taskset_name,
                },
                data=post_data,
                headers=headers,
                timeout=request_timeout,
                verify=self.verify_ssl,
            )

            response.encoding = self.encoding

            if not response.ok:
                raise EPageHTTPError(
                    status_code=response.status_code,
                    url=response.url,
                    response_text=response.text,
                )

            return response.text

        except requests.exceptions.Timeout as exc:
            raise EPageTimeoutError(
                f"EPage请求超时：{url}"
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            raise EPageConnectionError(
                f"无法连接EPage服务器：{url}"
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise EPageIOError(
                f"EPage请求发生错误：{exc}"
            ) from exc

    def execute(
        self,
        page_name: str,
        taskset_name: str,
        eio: EIO,
        *,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        clear_output: bool = False,
    ) -> EIO:
        """
        使用EIO对象与EPage服务器交互。

        请求数据：
            eio.buffo

        返回数据：
            写入 eio.buffi

        请求完成后：
            eio.sp = 0

        参数 clear_output：
            False：保留 eio.buffo
            True：请求完成后清空 eio.buffo
        """

        if not isinstance(eio, EIO):
            raise TypeError("eio必须是EIO对象")

        response_text = self.post(
            page_name=page_name,
            taskset_name=taskset_name,
            post_data=eio.buffo,
            headers=headers,
            timeout=timeout,
        )

        eio.buffi = response_text
        eio.sp = 0

        if clear_output:
            eio.buffo = ""

        return eio

    def close(self) -> None:
        """关闭底层HTTP会话。"""
        self.session.close()

    def __enter__(self) -> EPageIO:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> None:
        self.close()