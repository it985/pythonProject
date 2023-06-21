# 官方默认设置的安装源   https://pypi.python.org/simple
# 阿里云 http://mirrors.aliyun.com/pypi/simple
# 豆瓣(douban) http://pypi.douban.com/simple
# 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple
# 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple
# 阿里云 http://mirrors.aliyun.com/pypi/simple/

import os
ini = "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\n"
pippath=os.environ["USERPROFILE"]+"\\pip\\"
exec("if not os.path.exists(pippath):\n\tos.mkdir(pippath)")
open(pippath+"/pip.ini","w+").write(ini)
