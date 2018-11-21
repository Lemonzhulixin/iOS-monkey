# -*- coding: UTF8 -*-

import os
import time
import subprocess
from iOSCrashAnalysis import FileOperate


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def dirlist(path, allfile):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            allfile.append(filepath)
    return allfile

def get_ipa(path,file_format):
    files = dirlist(path, [])
    ipa_list = []
    for ipa in files:
        if (os.path.splitext(ipa)[1] in file_format):
            t = os.path.getctime(ipa)
            ipa_list.append([ipa, t])
    order = sorted(ipa_list, key=lambda e: e[1], reverse=True)
    ipa_path = order[0][0]
    return ipa_path

def install(path,file_format,duid):
    ipa_path = get_ipa(path,file_format)
    cmd = 'ios-deploy –r -b ' + '"' + ipa_path + '"' + ' -i ' + duid
    print('安装待测试的app', cmd)
    try:
        os.system(cmd)
    except Exception as msg:
        print('error message:', msg)
        raise

def monkey(devicename):
    cmd_monkey = "xcodebuild -project /Users/zhulixin/Desktop/iOS-monkey/XCTestWD/XCTestWD/XCTestWD.xcodeproj " \
                 "-scheme XCTestWDUITests " \
                 "-destination 'platform=iOS,name=" + devicename + "' " + \
                 "XCTESTWD_PORT=8001 " + \
                 "clean test"

    print(cmd_monkey)
    try:
        os.system(cmd_monkey)
    except Exception as msg:
        print('error message:', msg)
        raise

if __name__ == '__main__':
    # cmd_login = 'sshpass -p ios ssh iOS_Team@10.0.35.21'
    cmd_copy = 'sshpass -p ios scp -r iOS_Team@10.0.35.21:/Users/iOS_Team/XiaoYing_AutoBuild/XiaoYing/XiaoYingApp/fastlane/output_ipa/ ~/Desktop'

    # print('登录到远程pc')
    # os.system(cmd_login)

    print('远程复制ipa文件到本地')
    os.system(cmd_copy)

    path = "/Users/zhulixin/Desktop/output_ipa/"
    file_format = ['.ipa']
    duid = 'abab40339eaf2274aaf1ef068e11d6f85d84aae1'
    devicename = 'iPhone2146'
    ipa = get_ipa(path, file_format)
    print(ipa)
    
    install(path, file_format, duid)
    print("start monkey")
    monkey(devicename)

    print("============开始导出crashreport==========")
    find_str = 'XiaoYing-'  # 待测app crashreport文件关键字
    file_format1 = [".ips"]  # 导出的crash文件后缀
    file_format2 = [".crash"]  # 解析后的crash文件后缀

    reportPath = PATH("/Users/zhulixin/Desktop/iOS-monkey/CrashInfo/")
    beforePath = os.path.join(reportPath + '/Before')
    if not os.path.exists(beforePath):
        os.makedirs(beforePath)

    afterPath = os.path.join(reportPath + '/After')
    if not os.path.exists(afterPath):
        os.makedirs(afterPath)

    # 导出设备中的所有crash文件
    exportReport = 'idevicecrashreport -u ' + duid + ' ' + beforePath + '/'
    print(exportReport)
    os.system(exportReport)  # 导出设备中的crash

    print("============开始过滤并解析待测app相关crashreport==========")
    f = FileOperate.FileFilt()
    f.FindFile(find_str, file_format1, beforePath)

    if len(f.fileList) > 0:
        mailpath = '/Users/zhulixin/Desktop/UItest/iOS/Base/crash_mail.py'
        cmd_mail = 'python ' + mailpath + ' "fail" "VivaVideo iOS Monkey test failed" "出现了新的crash，查看地址: http://10.0.35.21:8080/ ，路径:' + afterPath + '"'
        print('发送邮件')
        os.system(cmd_mail)

    for file in f.fileList:
        inputFile = os.path.abspath(file)  # 绝对路径
        analysisPath = PATH("/Users/zhulixin/Desktop/iOS-monkey/iOSCrashAnalysis/")
        cmd_analysis = 'python3 ' + analysisPath + '/BaseIosCrash.py' + ' -i ' + inputFile
        print(cmd_analysis)
        os.system(cmd_analysis)

    # 移动解析完成的crashreport到新的文件夹
    f.MoveFile(find_str, file_format1, beforePath, afterPath)

    f.MoveFile(find_str, file_format2, beforePath, afterPath)
    print("============crashreport解析完成==========")

    # 删除所有解析之前的crash文件，若不想删除，注掉即可
    print("============删除所有解析之前的crash文件==========")
    f.DelFolder(beforePath)