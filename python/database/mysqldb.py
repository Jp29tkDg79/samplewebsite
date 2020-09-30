import mysql.connector
import time

from database.config import settings

class mysqldb(object):

    def __init__(self, hostname='mysql', portno='3306'):
        # import settings mysql.env file
        mysqlenv = settings.mysqlenv()

        # get now time
        start_time = time.time()

        # connecting 30 sec wait
        while time.time() - start_time < 30:
            # 無理やり処理してすみません <(_ _)>
            try:
                print('connecting Database...')
                # connect mysql
                conn = mysql.connector.connect(
                        host=hostname,
                        user=mysqlenv.user,
                        password=mysqlenv.password,
                        port=portno,
                        database=mysqlenv.databasename)

                if conn.is_connected():
                    # 再接続設定
                    conn.ping(reconnect=True)
                    break
            except mysql.connector.Error as err:
                # wait 5s
                time.sleep(5)

        self.__conn = conn

    @property
    def get_conn(self):
        return self.__conn

    @property
    def get_cursor(self):
        return self.__conn.cursor

    @property
    def commit(self):
        self.__conn.commit()

    def __del__(self):
        # unconnect mysql
        if self.__conn is not None:
            self.__conn.close()
