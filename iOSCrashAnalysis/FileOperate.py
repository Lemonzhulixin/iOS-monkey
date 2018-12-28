import os
import shutil
import re
import zipfile
import time
import requests

class FileFilt:
    fileList = []
    counter = 0
    def __init__(self):
        pass

    def FindFile(self, find_str, file_format, path, filtrate=1):
        for s in os.listdir(path):#返回指定目录下的所有文件和目录名
            newDir = os.path.join(path, s) #将多个路径组合后返回，第一个绝对路径之前的参数将被忽略；os.path.join('路径','文件名.txt')
            if os.path.isfile(newDir): #如果path是一个存在的文件，返回True。否则返回False。
                if filtrate:
                    if newDir and (os.path.splitext(newDir)[1] in file_format) \
                            and (find_str in os.path.splitext(newDir)[0]): #os.path.splitext():分离文件名与扩展名
                        self.fileList.append(newDir)
                        self.counter += 1
                else:
                    self.fileList.append(newDir)
                    self.counter += 1

    def MoveFile(self, find_str, file_format, path, newpath, filtrate=1):
        for s in os.listdir(path):
            newDir = os.path.join(path, s)
            if os.path.isfile(newDir):
                if filtrate:
                    if newDir and (os.path.splitext(newDir)[1] in file_format) \
                            and (find_str in os.path.splitext(newDir)[0]):
                        self.fileList.append(newDir)
                        self.counter += 1
                        shutil.move(newDir, newpath)
                else:
                    self.fileList.append(newDir)
                    self.counter += 1

    def DelFolder(self, delDir):
        delList = os.listdir(delDir)
        for f in delList:
            filePath = os.path.join(delDir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
                print(filePath + " was removed!")
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath, True)
                print("Directory: " + filePath + " was removed!")

    def FilePath(self, file_path):
        for cur_dir, included_file in os.walk(file_path):
            if included_file:
                for file in included_file:
                        print(cur_dir + "\\" + file)

    def zip_report(self,loacl_time, path, newpath):
        '''压缩TestReport文件夹
        path = "./TestReport"  # 要压缩的文件夹路径
        newpath = './TestReport_ZIP/' # 压缩后输出文件路径
        '''
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        zipName = newpath + 'iOS_' + loacl_time + '.zip'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(path):
            fpath = dirpath.replace(path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                # z.write(os.path.join(dirpath, filename))
        z.close()
        print('Generate zip_report file %s completed........ ' % zipName)
        return zipName


if __name__ == "__main__":
    pass

    # afterPath = '/Users/zhulixin/Desktop/UItest/Results/crashInfo/Before'
    # # f = FileFilt()
    # # f.FilePath(afterPath)
    #
    # os.rmdir(afterPath)

    # find_str = 'XiaoYing-'
    # file_format = '.ips'
    # b = FileFilt()
    # b.FindFile(find_str,file_format, path="/Users/zhulixin/new")
    # for file in b.fileList:
    #     filepath = os.path.abspath(file) #绝对路径
    #     print(filepath)


    url = 'http://10.0.34.xxx:5100/api/v1/report'
    files = {'file': open('/Users/iOS_Team/.jenkins/workspace/iOS_UI_VivaVideo/UItest/Results_ZIP/iOS_20181127171700.zip', 'rb')}
    response = requests.post(url, files=files)
    json = response.json()

