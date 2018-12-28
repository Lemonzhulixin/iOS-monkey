## 1228  新增内容
 1.自动获取真机设备名及duid
 2.iOS crashreport解析优化及测试结果DB存储
 3.测试失败邮件通知
 4.Web页面结果展示及支持crash log下载

## 1.环境
 Mac mini：10.12.6 
 xcode：9.2
 python：python3.6

## 2.备注
 a.FastMonkey相关问题参照@zhangzhao_lenovo 大神的帖子：https://testerhome.com/topics/9524，此处不再赘述！
 b.相关扫盲贴：
   https://testerhome.com/topics/9810        
   http://cdn2.jianshu.io/p/2cbdb50411ae
 c.ios-deploy，用于命令安装iOS app ，https://www.npmjs.com/package/ios-deploy
 d.FastMonkey设置为非sevrer模式

## 3.简单说明下脚本流程
自动化打包机打包->定时检测最新安装包->自动安装待测app->执行monkey->解析crashreport->DB存储->Web展示

## 4.脚本：
https://github.com/Lemonzhulixin/iOS-monkey.git

```javascript
# -*- coding: UTF8 -*-
from iOSCrashAnalysis.CrashExport import CrashExport
from iOSCrashAnalysis.getPakeage import getPakeage
from iOSCrashAnalysis import mysql_monkey
from iOSCrashAnalysis.FileOperate import *
from iOSCrashAnalysis.BaseIosPhone import get_ios_devices,get_ios_PhoneInfo
from iOSCrashAnalysis.FileOperate import FileFilt


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

def monkey(devicename):
    cmd_monkey = "xcodebuild -project /Users/iOS_Team/.jenkins/workspace/iOS_Monkey_VivaVideo/XCTestWD/XCTestWD/XCTestWD.xcodeproj " \
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
    print('获取设备信息')
    # dev_list = []
    # devices = get_ios_devices()
    # for i in range(len(devices)):
    #     duid = get_ios_devices()[i]
    #     dev = get_ios_PhoneInfo(duid)
    #     dev_list.append(dev)
    # print(dev_list)

    deviceName = 'iPhone2140'
    deviceID = 'e80251f0e66967f51add3ad0cdc389933715c3ed'
    release = '9.3.2'

    print('远程复制ipa文件到本地')
    start_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    cmd_copy = 'sshpass -p ios scp -r iOS_Team@10.0.35.xx:/Users/iOS_Team/XiaoYing_AutoBuild/XiaoYing/XiaoYingApp/fastlane/output_ipa/ ~/Desktop'
    os.system(cmd_copy)

    print('安装ipa测试包到设备')
    path = "/Users/iOS_Team/Desktop/output_ipa/"
    file_format = ['.ipa']
    ipa_path = getPakeage().get_ipa(path, file_format)
    getPakeage().install(path, file_format, deviceID)

    print("启动monkey")
    monkey(deviceName)

    print('解析crash report')
    find_str = 'XiaoYing-'  # 待测app crashreport文件关键字
    file_format1 = [".ips"]  # 导出的crash文件后缀
    file_format2 = [".crash"]  # 解析后的crash文件后缀
    CrashExport(deviceID, find_str, file_format1, file_format2)
    end_time = time.strftime('%Y%m%d%H%M%S', time.localtime())

    print('测试结果数据解析并DB存储')
    loacl_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    iOS_tag = 'iOS_' + loacl_time

    print('插入数据到device表')
    deviceData = {
        'name': deviceName,
        'serial_number': deviceID,
        'version': release,
        'status': 1,
        'tag': 'iOS'
    }

    print('插入数据到apk信息表')
    # ipa_path = '/Users/zhulixin/Desktop/output_ipa/day_inke_release_xiaoying.ipa'
    ipainfo = getPakeage().getIpaInfo(ipa_path)
    apkData = {
        'app_name': ipainfo[0],
        'ver_name': ipainfo[2],
        'ver_code': ipainfo[3],
        'file_name': 'day_inke_release_xiaoying.ipa',
        'file_path': ipa_path,
        'build_time': start_time,
        'tag': iOS_tag
    }

    print('插入数据到task表')
    taskData = {
        'start_time': start_time,
        'end_time': end_time,
        'app_name': ipainfo[0],
        'devices': 1,
        'test_count': None,
        'pass_count': None,
        'fail_count': None,
        'passing_rate': None,
        'tag': iOS_tag,
        'info': None
    }

    print('插入数据到results表')
    # f = FileFilt()
    # f.FindFile(find_str, file_format1, './CrashInfo/')
    # crash_count = len(f.fileList)
    # result = 1
    # if crash_count:
    #     result = 0

    resultData = {
        'result_id': start_time + '-monkey-' + ipainfo[0],
        'start_time': start_time,
        'end_time': end_time,
        'device_name': deviceName,
        'apk_id': None,
        'result': None,
        'status': None,
        'CRASHs': None,
        'ANRs': None,
        'tag': iOS_tag,
        'device_log':None,
        'monkey_log': None,
        'monkey_loop': None,
        'cmd':None,
        'seed': None
    }

    # print('deviceData:', deviceData)
    # mysql_monkey.insert_record_to_phones(deviceData)

    print('apkData:', apkData)
    mysql_monkey.insert_record_to_apks(apkData)

    print('taskData:', taskData)
    mysql_monkey.insert_record_to_tasks(taskData)

    print('resultData:', resultData)
    mysql_monkey.insert_record_to_results(resultData)

    print("压缩测试结果并传")
    f = FileFilt()
    results_file = f.zip_report(loacl_time, './CrashInfo/', './Results_ZIP/')
    url = 'http://10.0.32.xx:5100/api/v1/iOS-monkey'
    files = {'file': open(results_file, 'rb')}
    response = requests.post(url, files=files)
    json = response.json()

    print("删除本次的测试结果")
    f.DelFolder('./CrashInfo/')
    print("xxxxxxxxxxxxxxxxxxxxxxxxx Finish Test xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
```

## 5.Jenkins 部署定时任务

## 6.待优化
     a.多设备执行
     b.设备系统日志获取及web展示
     c.操作日志获取及web展示

最后感谢@zhangzhao_lenovo 开源的FastMonkey工具，赞！
