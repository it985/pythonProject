import sched
import time
import random
import logging
from datetime import datetime
from http.cookies import SimpleCookie
import requests

"""
1. 安装Python依赖 requests
pip install requests

2. 设置bilibili的cookie，可配置多个账号

3. 运行脚本
python3 violation.py

"""

cookies = [
    # cookie放到这里
    {
        "expires": 1681661611,
        "http_only": 1,
        "name": "SESSDATA",
        "same_site": 0,
        "secure": 0,
        "value": "9e3afc68%2C1689437611%2C41231612"
    },
    {
        "expires": 1681661611,
        "http_only": 0,
        "name": "bili_jct",
        "same_site": 0,
        "secure": 0,
        "value": "57c1c9aa4f2a21a6552faa99845d2e57"
    },
    {
        "expires": 1681661611,
        "http_only": 0,
        "name": "DedeUserID",
        "same_site": 0,
        "secure": 0,
        "value": "300767383"
    },
    {
        "expires": 1681661611,
        "http_only": 0,
        "name": "DedeUserID__ckMd5",
        "same_site": 0,
        "secure": 0,
        "value": "5f1c747826d1f2d3"
    },
    {
        "expires": 1681661611,
        "http_only": 0,
        "name": "sid",
        "same_site": 0,
        "secure": 0,
        "value": "n9d8toah"
    }
]


# 日志配置
def logger_config(log_path='main.log', logging_name='main'):
    '''
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(module)-10s line:%(lineno)3d] %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = logger_config()


class RoomInfo():
    JokeArea = 624
    MovieArea = 33

    def __init__(self, data) -> None:
        self.room_id = data.get("room_id")
        self.title = data.get("title")
        self.area_name = data.get("area_v2_name")
        self.have_live = data.get("live_status")

    def isJokeArea(self):
        # 10 -> 624
        return "搞笑" == self.area_name

    def isMovieArea(self):
        # 10 -> 33
        return "影音馆" == self.area_name

    def __str__(self) -> str:
        return "Room ID <%s> %s Live Status <%s> [%s]" % (self.room_id, self.area_name, self.have_live, self.title)


# 55-65随机数
def random60():
    return random.randint(55, 65)


# bilibili类
class BiliHelper:
    def __init__(self, cookies, schedule) -> None:
        self._cookies = cookies
        self._request = requests.Session()
        s = SimpleCookie(cookies)
        self._bili_jct = s.get("bili_jct").value
        self.schedule = schedule

        # 处理违规消息的id的集合
        self._deal_id = set()
        self._headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "cookie": self._cookies
        }
        info = self.getInfo()
        self.room_id = info.room_id
        logger.info("User info %s", info)

        # 2s后启动 检测违规，优先级是2
        self.schedule.enter(2, 2, self.checkViolation, ())

    def checkViolation(self):
        # 55-65随机，后启动 检测违规，优先级是2
        self.schedule.enter(random60(), 2, self.checkViolation, ())
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/anchorViolationsRecord/GetAnchorViolationsRecord?page=1&page_size=6"
        resp = self._request.get(url, headers=self._headers)
        j = resp.json()
        """
        {
            "code": 0,
            "message": "0",
            "ttl": 1,
            "data":
            {
                "page_size": 6,
                "page": 1,
                "count": 7,
                "violations_record":
                [
                    {
                        "id": 50268687,
                        "violations_reason": "分区错误，请立即更换至影音馆",
                        "penalty_reason": "禁止开播60秒",
                        "break_time": "2023年1月3日3时12分"
                    },
                    {
                        "id": 50268403,
                        "violations_reason": "分区错误，请立即更换至影音馆",
                        "penalty_reason": "警告",
                        "break_time": "2023年1月3日2时21分"
                    }
                ]
            }
        }
        """
        if j.get("code") == 0:
            record = j.get("data", {}).get("violations_record")
            if record:
                # 处理第一条（最新）消息，通过id去重
                if record[0]['id'] in self._deal_id:
                    return
                self._deal_violation(record[0])
                return record[0]
        logger.info("<%s> requet error %s", self.room_id, resp.text)

    def _deal_violation(self, data):
        """
        处理90s内的消息
        {
            "id": 50268403,
            "violations_reason": "分区错误，请立即更换至影音馆",
            "penalty_reason": "警告",
            "break_time": "2023年1月3日2时21分"
        }
        """
        strp = "%Y年%m月%d日%H时%M分"
        t = datetime.strptime(data['break_time'], strp)
        self._deal_id.add(data['id'])
        if (datetime.now() - t).seconds < 90:
            # 90s内的警告就处理 切换
            logger.info("<%s> 需要处理 %s", self.room_id, data)
            self.turnToMovie()
        else:
            logger.info("<%s> 无需处理 %s", self.room_id, data)

    def turnToMovie(self):
        info = self.getInfo()
        if not info.isMovieArea():
            # to movie
            ok = self.updateArea(info.MovieArea, info)
            logger.info("<%s> trun to movie [%s]", self.room_id, ok)
            if ok:
                # 2 小时后转为 搞笑区
                logger.info("<%s> 2h after turn joke ....", self.room_id)
                self.schedule.enter(60 * 60 * 2, 1, self.turnToJoke, ())

        else:
            logger.info("<%s> 不是 搞笑区 无需处理", self.room_id)

    def turnToJoke(self):
        info = self.getInfo()
        if not info.isJokeArea():
            # 不是joke 就转到 to joke
            ok = self.updateArea(info.JokeArea, info)
            logger.info("<%s> trun to joke [%s]", self.room_id, ok)
        else:
            logger.info("<%s> 是 搞笑区无需处理", self.room_id)

    def openLive(self):
        # 开播 搞笑区
        info = self.getInfo()
        if info.have_live == 0:
            # 未开播
            self._getNewRoomSwitch()
            self._startLive()
        else:
            logger.info("<%s> 已开播。。。", self.room_id)

    def _startLive(self):
        url = "https://api.live.bilibili.com/room/v1/Room/startLive"
        data = {
            "room_id": self.room_id,
            "area_v2": RoomInfo.JokeArea,
            "platform": "pc",
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
        }
        resp = self._request.post(url, data=data, headers=self._headers)
        resp_json = resp.json()
        if resp_json.get("code") == 0:
            # 请求成功
            logger.info("<%s> ok %s", self.room_id, resp_json.get("data", {}).get("rtmp"))
            return True
        else:
            logger.info("<%s> request error %s", self.room_id, resp.text)

    def _getNewRoomSwitch(self):
        url = "https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=10&area_id=624"
        resp = self._request.get(url, headers=self._headers)
        logger.info("<%s> req %s", self.room_id, resp.text)

    def updateArea(self, area_id, info: RoomInfo):
        # 更新分区
        url = "https://api.live.bilibili.com/room/v1/Room/update"
        # room_id=24785144&area_id=33&csrf_token=7bba09853122a40e225f87143f900ee8&csrf=7bba09853122a40e225f87143f900ee8
        data = {
            "room_id": info.room_id,
            "area_id": area_id,
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
        }
        resp = self._request.post(url, data=data, headers=self._headers)
        resp_json = resp.json()
        if resp_json.get("code") == 0:
            # 请求成功
            return True
        else:
            logger.info("<%s> request error %s", self.room_id, resp.text)

    def getInfo(self) -> RoomInfo:
        # 获取房间信息
        url = "https://api.live.bilibili.com/xlive/app-blink/v1/room/GetInfo?platform=pc"
        resp = self._request.get(url, headers=self._headers)
        resp_json = resp.json()
        if resp_json.get("code") == 0:
            # 请求成功
            data = resp_json.get("data", {})
            info = RoomInfo(data)
            return info


def main():
    # 初始化sched模块的 scheduler 类
    # 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
    schedule = sched.scheduler(time.time, time.sleep)

    for cookie in cookies:
        if not cookie:
            continue
        helper = BiliHelper(cookie, schedule)
        # helper.checkViolation()
        # 主动开播
        # helper.openLive()

    schedule.run()


if __name__ == "__main__":
    main()

