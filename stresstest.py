#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import psutil
import time

# 设置压力测试时间
testingTimeInSeconds = 600

# 设置最高频率与当前频率差值视为降频的阈值（误差范围）
deltaFreqThreshold = 0.02

# 降频出现次数的阈值，大于这个数字视为降频
throttledTimesThreshold = 5

def main():

    # CPU最大频率
    cpuMaxFrequency = float('%.2f' % (psutil.cpu_freq()[2] / 1000))

    # CPU降频次数
    thermalThrottledTimes = 0

    # CPU最高温度
    maxTemperature = 0

    # 获取CPU物理核心数
    numofPhysicalCores = psutil.cpu_count(logical=False)

    # 启动压力测试进程
    stressTestProcess = psutil.Popen(['stress', '-q', '-c', str(numofPhysicalCores), '-t', str(testingTimeInSeconds) + "s"])

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
            if cpuMaxFrequency - cpuCurrentFrequency > deltaFreqThreshold:
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
            print("CPU当前电压：" + cpuCurrentCoreVoltage)

            # 获取CPU每个核的占用
            cpuUsageList = psutil.cpu_percent(interval=None, percpu=True)

            for i in range(numofPhysicalCores):
                print("")
                print("CPU " + str(i+1) + " ：")
                print("使用率：" + str(cpuUsageList[i]) + ' %')
                # print("频率：" + str(cpuFrequencyTupleList[i][0]))
                # print("温度：" + str(cpuTemperatureTupleList[i+1][1]))            

            # 每隔2秒检测一次
            time.sleep(2)


    except Exception as e:
        print(e)
        stressTestProcess.terminate()
        stressTestProcess.wait()
    
    print("**********压力测试结束*************")
    print("最高温度：" + str(maxTemperature) + "摄氏度")
    if thermalThrottledTimes > throttledTimesThreshold:
        print("CPU出现了过热降频的情况")
    else:
        print("CPU未出现过热降频的情况")


main()
