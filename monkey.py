# -*- coding: UTF8 -*-

import os
import time

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
    cmd = 'ios-deploy –r -b ' + '"' + ipa_path +'"' + ' -i ' + duid
    try:
        os.system(cmd)
    except Exception as msg:
        print('error message:', msg)
        raise

def monkey(devicename):
    cmd_monkey = "xcodebuild -project /Users/zhulixin/Desktop/Fastmonkey/XCTestWD-master/XCTestWD/XCTestWD.xcodeproj " \
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
    path = "/Users/iOS_Team/XiaoYing_AutoBuild/XiaoYing/XiaoYingApp/"
    file_format = ['.ipa']
    duid = '5214866ccb9342f87f4c2aab093c25f7e252fd85'
    devicename = '6s2050'
    # ipa = get_ipa(path,file_format)
    # print(ipa)
    # install(path,file_format,duid)
    print("start monkey")
    monkey(devicename)







