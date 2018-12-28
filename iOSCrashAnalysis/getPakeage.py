import os
import zipfile, plistlib, re

class getPakeage:
    def __init__(self):
        pass

    def dirlist(self, path, allfile):
        filelist = os.listdir(path)
        for filename in filelist:
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                getPakeage().dirlist(filepath, allfile)
            else:
                allfile.append(filepath)
        return allfile

    def get_ipa(self, path,file_format):
        files =  getPakeage().dirlist(path, [])
        ipa_list = []
        for ipa in files:
            if (os.path.splitext(ipa)[1] in file_format):
                t = os.path.getctime(ipa)
                ipa_list.append([ipa, t])
        order = sorted(ipa_list, key=lambda e: e[1], reverse=True)
        ipa_path = order[0][0]
        return ipa_path

    def install(self,path,file_format,duid):
        ipa_path = getPakeage().get_ipa(path,file_format)
        cmd = 'ios-deploy –r -b ' + '"' + ipa_path + '"' + ' -i ' + duid
        print('安装待测试的app', cmd)
        try:
            os.system(cmd)
        except Exception as msg:
            print('error message:', msg)
            raise

    def find_plist_path(self,zip_file):
        name_list = zip_file.namelist()
        pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
        for path in name_list:
            m = pattern.match(path)
            if m is not None:
                return m.group()

    def getIpaInfo(self, ipa_path):
        ipa_file = zipfile.ZipFile(ipa_path)
        plist_path = getPakeage().find_plist_path(ipa_file)
        plist_data = ipa_file.read(plist_path)
        plist_root = plistlib.loads(plist_data)

        name = plist_root['CFBundleDisplayName']
        bundleID = plist_root['CFBundleIdentifier']
        version = plist_root['CFBundleShortVersionString']
        appKey = plist_root['XiaoYingAppKey']
        miniOSVersion = plist_root['MinimumOSVersion']
        print("=====getIpaInfo=========")
        print('appName: %s' % name)
        print('bundleId: %s' % bundleID)
        print('appVersion: %s' % version)
        print('appKey: %s' % appKey)
        print('miniOSVersion: %s' % miniOSVersion)
        return name, bundleID, version, appKey, miniOSVersion

if __name__ == '__main__':

    cmd_copy = 'sshpass -p ios scp -r iOS_Team@10.0.35.xx:/Users/iOS_Team/XiaoYing_AutoBuild/XiaoYing/XiaoYingApp/fastlane/output_ipa/ ~/Desktop'

    print('远程复制ipa文件到本地')
    os.system(cmd_copy)

    path = "/Users/zhulixin/Desktop/output_ipa/"
    file_format = ['.ipa']
    duid = 'abab40339eaf2274aaf1ef068e11d6f85d84aae1'
    devicename = 'iPhone2146'
    ipa_path = getPakeage().get_ipa(path, file_format)
    print(ipa_path)

    getPakeage().install(path, file_format, duid)

    getPakeage().getIpaInfo(ipa_path)

