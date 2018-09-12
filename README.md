## 0912  新增iOS crashreport解析

## 1.环境
 Mac mini：10.12.6 
 xcode：9.2
 python：python3.6

## 2.备注
 a.FastMonkey相关问题参照@zhangzhao_lenovo 大神的帖子：https://testerhome.com/topics/9524，此处不再赘述！
 b.相关扫盲贴：
*https://testerhome.com/topics/9810        
*http://cdn2.jianshu.io/p/2cbdb50411ae
 c.ios-deploy，用于命令安装iOS app ，https://www.npmjs.com/package/ios-deploy
 d.FastMonkey设置为非sevrer模式

## 3.简单说明下脚本流程
自动化打包机打包->定时检测最新安装包->自动安装待测app->执行monkey->解析crash report

## 4.脚本：
https://github.com/Lemonzhulixin/iOS-monkey.git

```javascript
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
    cmd_monkey = "xcodebuild -project /Users/xxxx/Desktop/iOS-monkey/XCTestWD-master/XCTestWD/XCTestWD.xcodeproj " \
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

#for AutoMonkey4IOS
# def monkey():
#     cmd_path = 'cd /Users/iOS_Team/.jenkins/workspace/iOS_Monkey_VivaVideo/AutoMonkey4IOS'
#     cmd_monkey = './start_monkey.sh'

#     print(cmd_path)

#     try:
#         os.system(cmd_path)
#     except Exception as msg:
#         print('error message:', msg)
#         raise

#     time.sleep(3)

#     print(cmd_monkey)
#     try:
#         # os.system(cmd_monkey)
#         subprocess.run(cmd_monkey, shell=True)
#         # monkeylog = open('/Users/iOS_Team/QA/Monkey/AutoMonkey4IOS/output/' + 'monkeylog.txt', 'w')
#         # subprocess.Popen(cmd_monkey, shell=True, stdout=monkeylog)
#     except Exception as msg:
#         print('error message:', msg)
#         raise


if __name__ == '__main__':
    path = "/Users/iOS_Team/XiaoYing_AutoBuild/XiaoYing/XiaoYingApp/fastlane/"
    file_format = ['.ipa']
    duid = '4c4ebeb44e5312c50c54b274a9145ebf89dce686'
    devicename = '5s2094'
    ipa = get_ipa(path, file_format)
    print(ipa)
    install(path, file_format, duid)
    print("start monkey")
    monkey(devicename)

    print("============开始导出crashreport==========")
    find_str = 'XiaoYing-'  # 待测app crashreport文件关键字
    file_format1 = [".ips"]  # 导出的crash文件后缀
    file_format2 = [".crash"]  # 解析后的crash文件后缀

    reportPath = PATH("/Users/xxxx/Desktop/iOS-monkey/CrashInfo/")
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
    for file in f.fileList:
        inputFile = os.path.abspath(file)  # 绝对路径
        # print(inputFile)
        analysisPath = PATH("/Users/xxxx/Desktop/iOS-monkey/iOSCrashAnalysis/")
        cmd_export = 'export DEVELOPER_DIR="/Applications/XCode.app/Contents/Developer"'
        cmd_analysis = 'python3 ' + analysisPath + '/BaseIosCrash.py' + ' -i ' + inputFile
        # print(cmd_analysis)
        os.system(cmd_analysis)

    # 移动解析完成的crashreport到新的文件夹
    f.MoveFile(find_str, file_format2, beforePath, afterPath)
    print("============crashreport解析完成==========")

    # 删除所有解析之前的crash文件，若不想删除，注掉即可
    print("============删除所有解析之前的crash文件==========")
    f.DelFolder(beforePath)

```

# 5.Jenkins 部署定时任务


# 6.踩了个小坑
```javascript
#安装app
def install(path,file_format,duid):
    ipa_path = get_ipa(path,file_format)
    cmd = 'ios-deploy –r -b ' + '"' + ipa_path +'"' + ' -i ' + duid
    try:
        os.system(cmd)
    except Exception as msg:
        print('error message:', msg)
        raise
```

这里ipa_path因为开发自动化打包的脚本生成的文件夹是带有空格的（eg.xxxx 2018-03-30 22-04-54），所以在组装命令的时候，加了俩双引号

# 7.待优化
 a.自动获取连接的真机设备名及duid
 b.多设备执行

最后感谢@zhangzhao_lenovo 开源的FastMonkey工具，赞！
