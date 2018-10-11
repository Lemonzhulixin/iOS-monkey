## 0912  新增iOS crashreport解析

## 1.环境
 Mac mini：10.12.6 
 xcode：9.2
 python：python3.6

## 2.备注
 - FastMonkey相关问题参照@zhangzhao_lenovo 大神的帖子：https://testerhome.com/topics/9524
 - 相关扫盲贴：
   - https://testerhome.com/topics/9810        
   - http://cdn2.jianshu.io/p/2cbdb50411ae
 - ios-deploy，用于命令安装iOS app ，https://www.npmjs.com/package/ios-deploy
 - FastMonkey设置为非sevrer模式

## 3.简单说明下脚本流程
   自动化打包机打包->定时检测最新安装包->自动安装待测app->执行monkey->解析crash report

## 4.脚本：
- https://github.com/Lemonzhulixin/iOS-monkey.git

## 5.Jenkins 部署定时任务

## 6.待优化
 - 自动获取连接的真机设备名及duid
 - 多设备执行

## 最后感谢@zhangzhao_lenovo 开源的FastMonkey工具，赞！
