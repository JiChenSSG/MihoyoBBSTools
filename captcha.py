from request import http
import setting
import json
from loghelper import log
import yaml
from twocaptcha import TwoCaptcha


def game_captcha(gt: str, challenge: str, header: dict):
    return ocr(gt, challenge)


def bbs_captcha(gt: str, challenge: str):
    return ocr(gt, challenge)


def read_appkey():
    with open('./config/ocr/config.yaml') as file:
        data = yaml.safe_load(file)
        return data['appkey']


def ocr(gt: str, challenge: str):
    appkey = read_appkey()
    
    solver = TwoCaptcha(appkey)
    
    log.info("验证码识别中....")

    try:
        req = solver.geetest(
                gt=gt,
                apiServer='api.geetest.com',
                challenge=challenge,
                url=setting.bbs_captcha_verify
            )
    except Exception as e:
        log.warning("验证码识别异常: " + str(e))
        return None
    
    if req.get('code') is None:
        log.info("识别失败")
        return None
    
    req = json.loads(req.get('code'))
    
    log.info("识别成功")
    return req.get('geetest_validate')
