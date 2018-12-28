#coding=utf-8
import os
from iOSCrashAnalysis import FileOperate

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def CrashExport(deviceID, find_str, format1, format2):
    print("============开始导出crashreport==========")
    resultPath = ''.join(['./CrashInfo/'])
    beforePath = os.path.join(resultPath + 'temp')
    if not os.path.exists(beforePath):
        os.makedirs(beforePath)

    afterPath = os.path.join(resultPath)
    if not os.path.exists(afterPath):
        os.makedirs(afterPath)
    print("导出设备中的所有crash文件")
    exportReport = 'idevicecrashreport -u ' + deviceID + ' ' + beforePath + '/'
    print(exportReport)
    os.system(exportReport)  # 导出设备中的crash

    print("============开始过滤并解析待测app相关crashreport==========")
    f = FileOperate.FileFilt()
    f.FindFile(find_str, format1, beforePath)

    # if len(f.fileList) > 0:
    #     mailpath = '/Users/zhulixin/Desktop/iOS-monkey/iOSCrashAnalysis/crash_mail.py'
    #     cmd_mail = 'python ' + mailpath + ' "fail" "VivaVideo iOS UI autotest failed" "出现了新的crash，查看地址: http://10.0.32.6:8082/UIAuto/ios"'
    #     print('发送邮件')
    #     os.system(cmd_mail)

    for file in f.fileList:
        inputFile = os.path.abspath(file)
        analysisPath = ''.join(["./iOSCrashAnalysis/"])
        cmd_analysis = 'python3 ' + analysisPath + 'BaseIosCrash.py' + ' -i ' + inputFile
        os.system(cmd_analysis)

    # 移动解析完成的crashreport和原始ips文件到新的文件夹
    f.MoveFile(find_str, format1, beforePath, afterPath)
    f.MoveFile(find_str, format2, beforePath, afterPath)
    print("============crashreport解析完成==========")

    # 删除所有解析之前的crash文件，若不想删除，注掉即可
    print("============删除所有解析之前的crash文件==========")
    f.DelFolder(beforePath)
    os.rmdir(beforePath)


if __name__ == '__main__':
    find_str = 'XiaoYing-'  # 待测app crashreport文件关键字
    file_format1 = [".ips"]  # 导出的crash文件后缀
    file_format2 = [".crash"]  # 解析后的crash文件后缀
    deviceID = 'e80251f0e66967f51add3ad0cdc389933715c3ed'
    deviceName = 'iPhone2140'

    CrashExport(deviceID,find_str,file_format1,file_format2)