# python_scripts
一些实用的树莓派测试用的python脚本。

## stresstest
Linux压力测试工具，可用于树莓派超频后测试稳定性。

### 环境安装
``` bash
sudo apt update
sudo apt upgrade -y
sudo apt install stress
sudo pip3 install pyyaml
sudo pip3 install psutil
```
### 运行
``` bash
sudo python3 stresstest.py
```
