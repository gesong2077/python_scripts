# python_scripts
一些实用的树莓派测试用的python脚本。

## stresstest
Linux压力测试工具，个人用于树莓派超频后测试稳定性。

### 环境要求 ###
* stress工具
* python的psutil库

### 环境安装
``` bash
sudo apt update
sudo apt upgrade -y
sudo apt install stress
sudo pip3 install psutil
```
### 运行
``` bash
sudo python3 stresstest.py
```
