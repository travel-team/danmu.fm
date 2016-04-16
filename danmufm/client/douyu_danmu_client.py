import datetime
import re
import uuid
import hashlib
import socket
import requests
import json
import threading
import time
from ..misc.player import MPlayer
from ..misc.color_printer import ColorPrinter
from ..model.douyu_msg import DouyuMsg
# import sys
import logging

logger = logging.getLogger("danmufm")
gfif_map = {"59": {"index": 1, "name": "火箭",
                   "bimg": "http://staticlive.douyutv.com/upload/dygift/9b4638fc809d7ae7ae4e3440c7b89371.png",
                   "himg": "http://staticlive.douyutv.com/upload/dygift/7f0643700d331aca31a6f6ea255e323e.gif",
                   "cimg": "http://staticlive.douyutv.com/upload/dygift/7dce6b2170eebecf85596b47370217ce.gif",
                   "stay_time": 200000, "type": 2, "style": 6, "pc": 50000, "ef": 1, "is_stay": 1, "drgb": "#210101",
                   "urgb": "#732909", "grgb": "#732909", "brgb": "#5861b5",
                   "small_effect_icon": "http://staticlive.douyutv.com/upload/dygift/5c9f85d09b8a11d68954315c2b1b3fb2.png",
                   "big_effect_icon": "http://staticlive.douyutv.com/upload/dygift/9fcb65afc84344c3dfc4374ebe0b2b6d.gif",
                   "gift_icon": "http://staticlive.douyutv.com/upload/dygift/a0d8447bb7af7b72a0dff6ae4d3cda4d.png",
                   "gift_open_icon": "http://staticlive.douyutv.com/upload/dygift/bef1a093399db8e9289d6de5d9459d85.gif"},
            "54": {"index": 2, "name": "飞机",
                   "bimg": "http://staticlive.douyutv.com/upload/dygift/ebfd70449be168a1315293f68c24ebe4.jpg",
                   "himg": "http://staticlive.douyutv.com/upload/dygift/8e9112823c19cecd7e27e524814d9470.gif",
                   "cimg": "http://staticlive.douyutv.com/upload/dygift/1573eee715b43dbc50002ba67ac5a85c.gif",
                   "stay_time": 60000, "type": 2, "style": 5, "pc": 10000, "ef": 2, "is_stay": 1, "drgb": "#210101",
                   "urgb": "#1276ca", "grgb": "#1276ca", "brgb": "#7cc6f8", "small_effect_icon": "",
                   "big_effect_icon": "", "gift_icon": "", "gift_open_icon": ""}, "52": {"index": 3, "name": "666",
                                                                                         "bimg": "http://staticlive.douyutv.com/upload/dygift/34dd474aa978d2ca7fc733150a039e8b.png",
                                                                                         "himg": "http://staticlive.douyutv.com/upload/dygift/f3956f7b059a6aca4d24c7436ab4e34e.gif",
                                                                                         "cimg": "http://staticlive.douyutv.com/upload/dygift/824221e62370b373085838718f256858.gif",
                                                                                         "stay_time": 6000, "type": 2,
                                                                                         "style": 4, "pc": 600, "ef": 0,
                                                                                         "is_stay": 0,
                                                                                         "drgb": "#210101",
                                                                                         "urgb": "#337e18",
                                                                                         "grgb": "#337e18",
                                                                                         "brgb": "#87d364",
                                                                                         "small_effect_icon": "",
                                                                                         "big_effect_icon": "",
                                                                                         "gift_icon": "",
                                                                                         "gift_open_icon": ""},
            "57": {"index": 4, "name": "赞",
                   "bimg": "http://staticlive.douyutv.com/upload/dygift/78b5de723f55c134d2935327a9253918.png",
                   "himg": "http://staticlive.douyutv.com/upload/dygift/1e50bcda9268706cfae4bd8e9b96e4db.gif",
                   "cimg": "http://staticlive.douyutv.com/upload/dygift/8dcd680f30b229a7992fd19ec85d2d82.gif",
                   "stay_time": 4000, "type": 2, "style": 3, "pc": 10, "ef": 0, "is_stay": 0, "drgb": "#330066",
                   "urgb": "#ff6600", "grgb": "#cc0000", "brgb": "#ffb675", "small_effect_icon": "",
                   "big_effect_icon": "", "gift_icon": "", "gift_open_icon": ""}, "53": {"index": 5, "name": "520",
                                                                                         "bimg": "http://staticlive.douyutv.com/upload/dygift/afc7e25f677d52a6cf961c27ea4cfa87.png",
                                                                                         "himg": "http://staticlive.douyutv.com/upload/dygift/b2d45ef42b523bc0edad465b9ff33ed2.gif",
                                                                                         "cimg": "http://staticlive.douyutv.com/upload/dygift/2a5c2c6de6e8e18483bde772cf28ca04.gif",
                                                                                         "stay_time": 2000, "type": 1,
                                                                                         "style": 2, "pc": 520, "ef": 0,
                                                                                         "is_stay": 0,
                                                                                         "drgb": "#330033",
                                                                                         "urgb": "#ff6633",
                                                                                         "grgb": "#cc0000",
                                                                                         "brgb": "#ffafba",
                                                                                         "small_effect_icon": "",
                                                                                         "big_effect_icon": "",
                                                                                         "gift_icon": "",
                                                                                         "gift_open_icon": ""},
            "50": {"index": 6, "name": "100鱼丸",
                   "bimg": "http://staticlive.douyutv.com/upload/dygift/e4da1fd2fbd8c0611218f5e702b69d0f.png",
                   "himg": "http://staticlive.douyutv.com/upload/dygift/a7cb18b2a449c360a9c9bec6af8b0575.png",
                   "cimg": "http://staticlive.douyutv.com/upload/dygift/424f745bfb8bff7dcd4422e738562f6a.jpg",
                   "stay_time": 1000, "type": 1, "style": 1, "pc": 100, "ef": 0, "is_stay": 0, "drgb": "#000066",
                   "urgb": "#ff6600", "grgb": "#ff3333", "brgb": "#fdd691", "small_effect_icon": "",
                   "big_effect_icon": "", "gift_icon": "", "gift_open_icon": ""}}


class DouyuDanmuClient(object):
    """Docstring for DouyuDanmuClient. """

    def __init__(self, room, auth_dst_ip, auth_dst_port, g_config):
        self.DANMU_ADDR = ("danmu.douyutv.com", 8602)
        self.g_config = g_config
        self.DANMU_AUTH_ADDR = (auth_dst_ip, int(auth_dst_port))
        self.room = room
        self.room_id = str(room["id"])
        self.auth_dst_ip = auth_dst_ip
        self.auth_dst_port = auth_dst_port
        self.dev_id = str(uuid.uuid4()).replace("-", "")
        self.mplayer = MPlayer()

    def start(self):
        self.do_login()
        # if self.live_stat == "离线":
        #     logger.info("主播离线中,正在退出...")
        # else:
        logger.info("主播在线中,准备获取弹幕...")
        self.print_room_info()
        t = threading.Thread(target=self.keeplive)
        t.setDaemon(True)
        t.start()
        # self.send_danmu_chat_msg("[emot:dy108]")
        while True:
            self.get_danmu()

    def print_room_info(self):
        api_url_prefix = "http://douyu.com/api/v1/"
        cctime = int(time.time())
        md5url = "room/" + str(self.room_id) + "?aid=android&client_sys=android&time=" + str(cctime)
        m2 = hashlib.md5(bytes(md5url + "1231", "utf-8"))
        self.url_json = api_url_prefix + md5url + "&auth=" + m2.hexdigest()
        res = requests.get(self.url_json)
        js_data = json.loads(res.text)

        sd_rmtp_url = str(js_data["data"]["rtmp_url"]) + "/" + str(js_data["data"]["rtmp_live"])
        hd_rmtp_url = str(js_data["data"]["rtmp_url"]) + "/" + str(js_data["data"]["rtmp_live"])
        spd_rmtp_url = str(js_data["data"]["rtmp_url"]) + "/" + str(js_data["data"]["rtmp_live"])
        # sd_flv_addr = requests.get(sd_rmtp_url, allow_redirects=False).headers["Location"]
        # hd_flv_addr = requests.get(hd_rmtp_url, allow_redirects=False).headers["Location"]
        # spd_flv_addr = requests.get(spd_rmtp_url, allow_redirects=False).headers["Location"]
        # if self.g_config["quality"] <= 0 or self.g_config["quality"] >= 4:
        #     logger.info("不播放视频")
        # elif self.g_config["quality"] == 1:
        #     logger.info("正在尝试使用Mplayer播放普清视频" + sd_flv_addr)
        #     self.mplayer.start(sd_flv_addr)
        # elif self.g_config["quality"] == 2:
        #     logger.info("正在尝试使用Mplayer播放高清视频" + hd_flv_addr)
        #     self.mplayer.start(hd_flv_addr)
        # else:
        #     logger.info("正在尝试使用Mplayer播放超清视频" + spd_flv_addr)
        #     self.mplayer.start(spd_flv_addr)
        print("=========================================")
        print("= Room Infomation                       =")
        print("=========================================")
        print("= 房间: " + self.room["name"] + "(" + self.room_id + ")")
        print("= 主播: " + self.room["owner_name"] + str(self.room["owner_uid"]))
        print("= 公告: " + re.sub("\n+", "\n", re.sub('<[^<]+?>', '', self.room["gg_show"])))
        print("= 标签: " + str(self.room["tags"]))
        print("= 在线: " + self.live_stat)
        print("= 粉丝: " + self.fans_count)
        print("= 财产: " + self.weight)
        print("=========================================")
        self.danmu_writer = open(self.room_id + '.danmu.log', 'a+')

    def keeplive(self):
        print("启动 KeepLive 线程")
        while True:
            self.send_auth_keeplive_msg()
            self.send_danmu_keeplive_msg()
            # print("发送 KeepLive")
            time.sleep(40)

    def do_login(self):
        self.danmu_auth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.danmu_auth_socket.connect(self.DANMU_AUTH_ADDR)
        self.danmu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.danmu_socket.connect(self.DANMU_ADDR)
        self.send_auth_loginreq_msg()
        recv_msg = self.auth_recv()
        #print('recv_msg——————————%s' % (recv_msg,))
        if "live_stat@=0" in recv_msg:
            self.live_stat = "离线"
        else:
            self.live_stat = "在线"
        self.username = re.search('\/username@=(.+)\/nickname', recv_msg).group(1)
        recv_msg = self.auth_recv()
        self.gid = re.search('\/gid@=(\d+)\/', recv_msg).group(1)
        self.weight = re.search('\/weight@=(\d+)\/', recv_msg).group(1)
        self.fans_count = re.search('\/fans_count@=(\d+)\/', recv_msg).group(1)
        self.send_qrl_msg()
        recv_msg = self.auth_recv()
        # print(recv_msg)
        self.send_auth_keeplive_msg()
        recv_msg = self.auth_recv()
        # print(recv_msg)
        self.send_danmu_loginreq_msg()
        recv_msg = self.danmu_recv()
        #print(recv_msg)
        self.send_danmu_join_group_msg()
        #self.send_danmu_chat_msg('[emot:dy101]')
        # recv_msg = self.danmu_recv()
        # print(recv_msg)

    def get_danmu(self):
        # print("获取弹幕")
        recv_msg = self.danmu_recv()
        # print(recv_msg)
        msg_content = re.sub(r"/(\w+)", "\n\\1", recv_msg[:-1]).replace("@S=", "/").replace("@A=", ":").replace("@=",
                                                                                                                ":")
        data = {}
        for line in msg_content.split('\n'):
            i = line.find(':')
            data[line[:i]] = line[i + 1:]
        data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.danmu_writer.write(str(data))
        if "type@=" not in recv_msg:
            logger.info("无效消息")
        elif "type@=error" in recv_msg:
            logger.info("错误消息,可能认证失效")
        else:
            try:
                msg_type = data.get('type', 'None')
                # print(msg_type)
                if msg_type == "chatmsg":
                    msg_type_zh = "弹幕消息"
                    sender_id = data.get('uid', 'None')
                    nickname = data.get('nn', 'None')
                    content = data.get('txt', 'None')
                    level = data.get('level', 'None')
                    time = data.get('time', 'None')
                    ColorPrinter.green(
                        "|" + msg_type_zh + "| " + nickname + " <Lv:" + level + ">" + " @ " + time + ": " + content + " ")

                elif msg_type == "uenter":
                    msg_type_zh = "入房消息"
                    user_id = data.get('uid', 'None')
                    nickname = data.get('nn', 'None')
                    strength = data.get('ct', 'None')
                    level = data.get('level', 'None')
                    time = data.get('time', 'None')
                    ColorPrinter.red("|" + msg_type_zh + "| " + nickname + " <Lv:" + level + ">" + " @ " + time)

                elif msg_type == "dgb":
                    msg_type_zh = "鱼丸赠送"
                    level = data.get('level', 'None')
                    user_id = data.get('uid', 'None')
                    nickname = data.get('nn', 'None')
                    gfid = data.get('gfid', '-1')
                    hits = data.get('hits', '0')
                    time = data.get('time', 'None')
                    ColorPrinter.yellow(
                        "|" + msg_type_zh + "| " + nickname + " <Lv:" + level + ">" + " @ " + time + ": " +
                        gfif_map.get(gfid, '未知礼物')['name'] + hits + " hits ")
                else:
                    ColorPrinter.green(recv_msg)
            except Exception as e:
                print(e)
                logger.error("解析错误")

    def parse_content(self, msg):
        # print(msg)
        content = msg[12:-1].decode('utf-8', 'ignore')
        return content

    def danmu_recv(self):
        return self.parse_content(self.danmu_socket.recv(4000))

    def auth_recv(self):
        return self.parse_content(self.danmu_auth_socket.recv(4000))

    def send_auth_keeplive_msg(self):
        data = "type@=keeplive/tick@=" + self.timestamp() + "/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/"
        msg = self.message(data)
        self.danmu_auth_socket.sendall(msg)

    def send_danmu_keeplive_msg(self):
        data = "type@=keeplive/tick@=" + self.timestamp() + "/"
        msg = self.message(data)
        self.danmu_socket.sendall(msg)

    def send_danmu_join_group_msg(self):
        data = "type@=joingroup/rid@=" + self.room_id + "/gid@=" + self.gid + "/"
        msg = self.message(data)
        self.danmu_socket.sendall(msg)

    def send_qrl_msg(self):
        data = "type@=qrl/rid@=" + self.room_id + "/"
        msg = self.message(data)
        self.danmu_auth_socket.sendall(msg)

    def send_danmu_loginreq_msg(self):
        #data = "type@=loginreq/username@=" + self.username + "/password@=1234567890123456/roomid@=" + self.room_id + "/"
        data = "type@=loginreq/username@=43538228/ct@=0/password@=536f868c09cfbc81399401da424e42e6/roomid@=272927/devid@=069A2C8020C5AEE79BA0BF6B6E66FED3/rt@=1460663109/vk@=b505fc9809723a554088f2e7a1758a4a/ver@=20150929/ltkid@=/biz@=/stk@=/"
        msg = self.message(data)
        self.danmu_socket.sendall(msg)

    def send_danmu_chat_msg(self, content):
        data = "type@=chatmessage/receiver@=0/content@=" + content + "/scope@=/col@=0/"
        msg = self.message(data)
        print(msg)
        self.danmu_socket.sendall(msg)
        print("send_danmu_chat_msg finished")
        res = self.danmu_recv()
        print(res)

    def send_auth_loginreq_msg(self):
        time = self.timestamp()
        vk = hashlib.md5(bytes(time + "7oE9nPEG9xXV69phU31FYCLUagKeYtsF" + self.dev_id, 'utf-8')).hexdigest()
        data = "type@=loginreq/username@=/ct@=0/password@=/roomid@=" + self.room_id + "/devid@=" + self.dev_id + "/rt@=" + self.timestamp() + "/vk@=" + vk + "/ver@=20150929/"
        #data = "type@=loginreq/username@=43538228/ct@=0/password@=536f868c09cfbc81399401da424e42e6/roomid@=272927/devid@=069A2C8020C5AEE79BA0BF6B6E66FED3/rt@=1460663109/vk@=b505fc9809723a554088f2e7a1758a4a/ver@=20150929/ltkid@=/biz@=/stk@=/"
        msg = self.message(data)
        self.danmu_auth_socket.sendall(msg)

    def timestamp(self):
        return str(int(time.time()))

    def message(self, content):
        return DouyuMsg(content).get_bytes()

    def align_left_str(self, raw_str, max_length, filled_chr):
        my_length = 0
        for i in range(0, len(raw_str)):
            if ord(raw_str[i]) > 127 or ord(raw_str[i]) <= 0:
                my_length += 1

            my_length += 1

        if (max_length - my_length) > 0:
            return raw_str + filled_chr * (max_length - my_length)
        else:
            return raw_str
