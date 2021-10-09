import os
import re

import paramiko
import pysftp

scp = paramiko.Transport(('47.102.139.195', 22))
scp.connect(username='root', password='Root123456')
sftp = paramiko.SFTPClient.from_transport(scp)


log_path = 'http://47.102.139.195:6800/logs/qianchenwuyou/seeker/2021-09-30T18_55_47.log'

content_list = os.popen("curl " + log_path).readlines()
content_list.append('\n')
# print(content_list)

data, string = [], ''
for content in content_list:
    if content != '\n':
        string += content
    else:
        data.append(string.replace('\n', '<br>').replace(' ', '&nbsp;'))
print(data)




