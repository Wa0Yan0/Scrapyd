import json
import os

import paramiko
from flask import request, Blueprint
from static.utils.PageUtils import PageUtils

log = Blueprint('log', __name__)

scp = paramiko.Transport(('47.102.139.195', 22))
scp.connect(username='root', password='Root123456')
sftp = paramiko.SFTPClient.from_transport(scp)
log_path = '/var/scrapyd/logs/'


@log.route('/logs')
def projects_dir():
    projects = []
    projects_name = sftp.listdir(log_path)
    queryInfo = json.loads(request.args.get("queryInfo"))
    pageUtils = PageUtils(len(projects_name), queryInfo)
    if queryInfo["query"] != '':
        for i in range(pageUtils.begin(), pageUtils.end()):
            if queryInfo["query"] in projects_name[i]:
                dic = {
                    'name': projects_name[i],
                    'type': 'Directory',
                    'level': 1,
                    'grade': '一级'
                }
                projects.append(dic)
        pageUtils.total = len(projects)
    else:
        for i in range(pageUtils.begin(), pageUtils.end()):
            dic = {
                'name': projects_name[i],
                'type': 'Directory',
                'level': 1,
                'grade': '一级'
            }
            projects.append(dic)
    return pageUtils.wrapper(projects)


@log.route('/logs/<project_name>')
def spiders_dir(project_name):
    spiders = []
    spiders_name = sftp.listdir(log_path + project_name)
    queryInfo = json.loads(request.args.get("queryInfo"))
    pageUtils = PageUtils(len(spiders_name), queryInfo)
    if queryInfo["query"] != '':
        for i in range(pageUtils.begin(), pageUtils.end()):
            if queryInfo["query"] in spiders_name[i]:
                dic = {
                    'name': spiders_name[i],
                    'type': 'Directory',
                    'level': 2,
                    'grade': '二级'
                }
                spiders.append(dic)
        pageUtils.total = len(spiders)
    else:
        for i in range(pageUtils.begin(), pageUtils.end()):
            dic = {
                'name': spiders_name[i],
                'type': 'Directory',
                'level': 2,
                'grade': '二级'
            }
            spiders.append(dic)
    return pageUtils.wrapper(spiders)


@log.route('/logs/<project_name>/<spider_name>')
def logs_file(project_name, spider_name):
    logs = []
    logs_name = sftp.listdir(log_path + project_name + '/' + spider_name)
    queryInfo = json.loads(request.args.get("queryInfo"))
    pageUtils = PageUtils(len(logs_name), queryInfo)
    path = project_name + '/' + spider_name + '/'
    if queryInfo["query"] != '':
        for i in range(pageUtils.begin(), pageUtils.end()):
            if queryInfo["query"] in logs_name[i]:
                size = str(int(sftp.stat(log_path + path + logs_name[i]).st_size / 1024)) + 'k'
                dic = {
                    'name': logs_name[i],
                    'size': size,
                    'type': 'text/plain',
                    'level': 3,
                    'grade': '三级'
                }
                logs.append(dic)
        pageUtils.total = len(logs)
    else:
        for i in range(pageUtils.begin(), pageUtils.end()):
            size = str(int(sftp.stat(log_path + path + logs_name[i]).st_size / 1024)) + 'k'
            dic = {
                'name': logs_name[i],
                'size': size,
                'type': 'text/plain',
                'level': 3,
                'grade': '三级'
            }
            logs.append(dic)
    return pageUtils.wrapper(logs)


@log.route('/logs/<project_name>/<spider_name>/<log_name>')
def show_log(project_name, spider_name, log_name):
    full_path = 'http://47.102.139.195:6800/logs/' + project_name + '/' + spider_name + '/' + log_name
    content_list = os.popen("curl " + full_path).readlines()
    content_list.append('\n')
    data, string = [], ''
    for content in content_list:
        if content != '\n':
            string += content
        else:
            data.append(string.replace('\n', '<br>').replace(' ', '&nbsp;'))
            string = ''
    return json.dumps(data)
