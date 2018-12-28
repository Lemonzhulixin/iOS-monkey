import mysql.connector

def upload_sql(sql, value):
    db_host = '10.0.32.xxx'
    port = 8060
    my_connect = mysql.connector.connect(
        host=db_host,
        port=port,
        db='qxxxx',
        user='rxxx',
        password='rxxx',
        charset='utf8'
    )
    my_cursor = my_connect.cursor()
    try:
        my_cursor.execute(sql, value)
        my_connect.commit()
    except mysql.connector.Error as err:
        print("Failed inserting by errorcode {}".format(err))
    my_cursor.close()
    my_connect.close()


def insert_record_to_phones(value):
    """
    插入数据到phones表
    :param value:
        value = {
            'name': 'NCE_TL10',
            'serial_number': 'BCD9XA1732301914',
            'version': '6.0',
            'status': 1,
            'tag': 'Android'
        }
    :return:
    """
    my_sql = "INSERT INTO monkey_phones (phone_id, name, serial_number, version, status, tag) " \
             "VALUES (NULL, %(name)s, %(serial_number)s, %(version)s, %(status)s, %(tag)s)"
    upload_sql(my_sql, value)
    return

def insert_record_to_apks(value):
    """
    插入数据到apks表
    :param value:
        value = {
            'app_name': 'com.quvideo.xiaoying',
            'ver_name': '7.5.5',
            'ver_code': '6705050',
            'file_name': 'XiaoYing_V7.5.5_0-xiaoyingtest-OthersAbroadDebug-2018-11-20_08_37_07.apk',
            'file_path': '/Users/iOS_Team/Desktop/QuTestMonkey/app/static/apks/xiaoying/XiaoYing_V7.5.5_0-xiaoyingtest-OthersAbroadDebug-2018-11-20_08_37_07.apk',
            'build_time': datetime.now().strftime('%Y%m%d%H%M%S'),
            'tag': 'Android'
        }
    :return:
    """
    my_sql = "INSERT INTO monkey_apks (apk_id, app_name, ver_name, ver_code, file_name, file_path, build_time, tag) " \
             "VALUES (NULL, %(app_name)s, %(ver_name)s, %(ver_code)s, %(file_name)s, %(file_path)s," \
             " %(build_time)s, %(tag)s)"
    upload_sql(my_sql, value)
    return

def insert_record_to_tasks(value):
    """
    插入数据到tasks表
    :param value:
        value = {
            'start_time': datetime.now().strftime('%Y%m%d%H%M%S'),
            'end_time': datetime.now().strftime('%Y%m%d%H%M%S'),
            'app_name': '小影',
            'devices': None
            'test_count': 1,
            'pass_count': 1,
            'fail_count': 0,
            'passing_rate': 1,
            'tag': datetime.now().strftime('%Y%m%d%H%M%S') + '-monkey',
            'info': None
        }
    :return:
    """
    my_sql = "INSERT INTO monkey_tasks (task_id, start_time, end_time, app_name, devices, test_count, pass_count," \
             " fail_count, passing_rate, info, tag) " \
             "VALUES (NULL, %(start_time)s, %(end_time)s, %(app_name)s, %(devices)s, %(test_count)s," \
             " %(pass_count)s, %(fail_count)s, %(passing_rate)s, %(info)s, %(tag)s)"
    upload_sql(my_sql, value)
    return

def insert_record_to_results(value):
    """
    插入数据到results表
    :param value:
         result_data = {
            'result_id': '20181208163031-monkey-小影-0',
            'start_time': '20181108163032',
            'end_time': None,
            'device_name': 'BIBEYDSCO7OBSWVW',
            #1 PASS
            'result': 1,
            'status': 0,
            'CRASHs': 0,
            'ANRs': 0,
            'tag': '20181108163031-monkey',
            'device_log': 'http://10.0.32.6:5100/static/logs/devicelogs/com.quvideo.xiaoying/device-BIBEYDSCO7OBSWVW-20181108163031-小影-0.log',
            'monkey_log': 'http://10.0.32.6:5100/static/logs/monkeylogs/com.quvideo.xiaoying/monkey-BIBEYDSCO7OBSWVW-20181108163031-小影-0.log',
            'monkey_loop': 10,
            'cmd': '--throttle 1000 --pct-touch 70 --pct-motion 5 --pct-trackball 5 --pct-appswitch 20 --kill-process-after-error --monitor-native-crashes --ignore-crashes --ignore-timeouts',
            'seed': 3905
         }
    :return:
    """
    my_sql = "INSERT INTO monkey_results (result_id, start_time, end_time, device_name, apk_id, result, status, CRASHs," \
             " ANRs, tag, device_log, monkey_log, monkey_loop, cmd, seed) " \
             "VALUES (%(result_id)s, %(start_time)s, %(end_time)s, %(device_name)s, %(apk_id)s, %(result)s," \
             " %(status)s, %(CRASHs)s, %(ANRs)s, %(tag)s, %(device_log)s, %(monkey_log)s, %(monkey_loop)s," \
             " %(cmd)s, %(seed)s)"
    upload_sql(my_sql, value)
    return