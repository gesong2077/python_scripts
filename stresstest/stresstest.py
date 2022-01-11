#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import yaml
import psutil
import time

def main():
    # 获取当前脚本所在文件夹路径
    curPath = os.path.dirname(os.path.realpath(__file__))
    # 设置yaml文件读取路径
    configFilePath = os.path.join(curPath, "config.yaml")

    # 尝试读取配置文件
    try:
        with open(configFilePath, 'r') as f:
            configs = yaml.safe_load(f)
            duration = configs['Duration']
            marginOfFreqError = configs['MarginOfFreqError']
            allowedThrottledTimes = configs['AllowedThrottledTimes']

    # 配置文件读取出错，使用默认值
    except Exception as e:
        duration = '10m'
        marginOfFreqError = 0.02
        allowedThrottledTimes = 5
    
    # CPU最大频率
    cpuMaxFrequency = float('%.2f' % (psutil.cpu_freq()[2] / 1000))

    # CPU降频次数
    thermalThrottledTimes = 0

    # CPU最高温度
    maxTemperature = 0

    # 获取CPU逻辑核心数
    numofLogicalCores = psutil.cpu_count()

    # 启动压力测试进程
    try:
        stressTestProcess = psutil.Popen(['stress', '-q', '-c', str(numofLogicalCores), '-t', duration])
    except Exception as e:
        print(e)
        return

    # 静置5秒再开始统计CPU数据
    print("**********压力测试开始*************")
    time.sleep(5)
    
    try:
        while True:
            # 检查压力测试是否结束
            retCode = stressTestProcess.poll()
            if retCode is not None:
                break

            # 清屏
            os.system("clear")

            # # 获取CPU每个核心的频率（树莓派不支持）
            # cpuFrequencyTupleList = psutil.cpu_freq(percpu=True)

            # # 获取CPU每个核心的温度（树莓派不支持）
            # cpuTemperatureTupleList = psutil.sensors_temperatures()["coretemp"]

            # 获取CPU核心频率
            cpuCurrentFrequency = float('%.2f' % (psutil.cpu_freq()[0] / 1000))

            # 如果当前CPU频率和CPU最大频率差距大于阈值，代表出现降频，小于这个值视作误差
            if cpuMaxFrequency - cpuCurrentFrequency > marginOfFreqError:
                thermalThrottledTimes = thermalThrottledTimes + 1

            # 获取CPU当前温度
            cpuCurrentTemperature = float('%.1f' % psutil.sensors_temperatures()["cpu_thermal"][0][1])

            if cpuCurrentTemperature > maxTemperature:
                maxTemperature = cpuCurrentTemperature

            # # 获取当前CPU核心电压（仅限树莓派raspberry pi os上使用，如要在其他系统上使用请自行谷歌如何安装vcgencmd）
            # cmdOutput = os.popen('vcgencmd measure_volts core').readline()
            # cpuCurrentCoreVoltage = cmdOutput.replace("volt=","").replace("'C\n","")

            print("**********压力测试进行中*************")
            print("CPU当前频率：" + str(cpuCurrentFrequency) + "GHz")
            print("CPU当前温度：" + str(cpuCurrentTemperature)+"摄氏度")
            # print("CPU当前电压：" + cpuCurrentCoreVoltage)

            # 获取CPU每个核的占用
            cpuUsageList = psutil.cpu_percent(interval=None, percpu=True)

            for i in range(numofLogicalCores):                   
                print("CPU " + str(i+1) + " ：")
                print("使用率：" + str(cpuUsageList[i]) + ' %')
                # print("频率：" + str(cpuFrequencyTupleList[i][0]))
                # print("温度：" + str(cpuTemperatureTupleList[i+1][1]))
                print("")         

            # 每隔2秒检测一次
            time.sleep(2)


    except Exception as e:
        print(e)
        stressTestProcess.terminate()
        stressTestProcess.wait()
    
    print("**********压力测试结束*************")
    print("最高温度：" + str(maxTemperature) + "摄氏度")
    if thermalThrottledTimes > allowedThrottledTimes:
        print("CPU出现了过热降频的情况")
    else:
        print("CPU未出现过热降频的情况")



main()
