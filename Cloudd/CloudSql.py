import pymysql
from datetime import datetime

class CloudSql():

    def HandleLogSql(self):
        self.CloudSqlDB = pymysql.connect('localhost', 'bingocloud', 'SL0Z7@OmJIJY', 'CloudOption', charset='utf8')
        self.CloudCursor = self.CloudSqlDB.cursor()
        NowTime=datetime.now()
        print(str(NowTime))
        try:
            AddLogSql='update CloudApp_service set ServiceProcess=%d where ServiceIMC="SIP"'
            self.CloudCursor.execute(AddLogSql,[12])
            self.CloudSqlDB.commit()
        except:
            self.CloudSqlDB.rollback()
        finally:
            self.CloudCursor.close()
            self.CloudSqlDB.close()

CloudSS=CloudSql()
CloudSS.HandleLogSql()