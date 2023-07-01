from request import http
import setting
import json
from loghelper import log
import yaml


def game_captcha(gt: str, challenge: str, header: dict):
    return ocr(gt, challenge)


def bbs_captcha(gt: str, challenge: str):
    return ocr(gt, challenge)


def read_appkey():
    with open('./config/ocr.yaml') as file:
        data = yaml.safe_load(file)
        return data['appkey']


def ocr(gt: str, challenge: str):
    appkey = read_appkey()
    log.info("验证码识别中....")
    try:
        req = http.post(url='http://api.rrocr.com/api/recognize.html', headers=setting.headers, params={
            'appkey': appkey, 'gt': gt, 'challenge': challenge, 'referer': setting.bbs_captcha_verify})
    except Exception as e:
        log.warning("验证码识别异常: " + str(e))
        return None

    if req.status_code == 200:
        data = json.loads(req.text)
        log.info("识别成功")
        return data['data']['validate']
    else:
        log.info("识别失败")
        return None  # 失败返回None 成功返回validate
