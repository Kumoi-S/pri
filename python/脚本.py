# report
import requests
import re
import random
import time
import json


# 登录网址
login_url = 'https://sso.stu.edu.cn/login'
# 上报网址
repo_url = 'https://my.stu.edu.cn/health-report/report/saveReport.do'


# 构造请求头
header = {'User-Agent': 'Mozilla/5.0'}
payload = {'jsessionid': '', 'service': 'https://my.stu.edu.cn/health-report/init-stu-user'}


# 正则表达式
lt_pattern = re.compile(r'name="lt" value="(.+?)"')
ex_pattern = re.compile(r'name="execution" value="(.+?)"')
id_pattern = re.compile(r'JSESSIONID=(.+?);')
status_pattern = re.compile(r'<div class="welcome" style="padding:10px">(.+)')
check_pattern = re.compile(r'请报今天的健康信息！')


# 获取登录所需参数
r = requests.get(login_url, params=payload, headers=header,verify=False)
lt = lt_pattern.findall(r.text)[0]
ex = ex_pattern.findall(r.text)[0]
header.update(Cookie=r.headers['Set-Cookie'])
payload['jsessionid'] = id_pattern.findall(r.headers['Set-Cookie'])[0]


# 登录
log_data = {
    'username': '19mysong',     # 输入用户名
    'password': 'Smy20011006',     # 输入密码
    'lt': lt,
    'execution': ex,
    '_eventId': 'submit'
}
r1 = requests.post(login_url, params=payload, headers=header, data=log_data, verify=False)
r2 = r1.history[2]
header['Cookie'] = r2.headers['Set-Cookie']
status = status_pattern.findall(r1.text)[0]
status = re.sub(r'[(<span>)|(</span>)]', '', status)
check = check_pattern.findall(status)


# 上报信息
morn_heat = str(round(random.uniform(36.5, 36.8), 1))
noon_heat = str(round(random.uniform(36.5, 36.8), 1))
repo_data = {
    'health': '良好'.encode('utf-8'),
    'familyHealth': '良好'.encode('utf-8'),
    'importantPersonType': '4',
    'dailyReport.afternoorBodyHeat': noon_heat,
    'dailyReport.forenoonBodyHeat': morn_heat,
    'dailyReport.hasCough': 'false',
    'dailyReport.hasShortBreath': 'false',
    'dailyReport.hasWeak': 'false',
    'dailyReport.hasFever': 'false'
}

# 上报
time.sleep(3)
if len(check):
    r3 = requests.post(repo_url, headers=header, data=repo_data, verify=False)
    if json.loads(r3.text)["success"]:
        print('上报成功！')
        time.sleep(2)
    else:
        print('上报失败！')
        time.sleep(2)
else:
    print('已经上报！')
    time.sleep(2)