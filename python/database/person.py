import base64
import hashlib

from database import mysqldb
from database.config import settings

# extend mysql connection
class persondb(mysqldb.mysqldb):

    def __init__(self):
        # mysql connection
        super().__init__()

        self.__tablename = 'persons'
        # each database columns name
        self.__id = 'id'
        self.__name = 'name'
        self.__password = 'password'

        if self.get_conn is not None:
            # create persons table
            cursor = self.get_cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.__tablename}('
                           f'{self.__id} int NOT NULL AUTO_INCREMENT,'
                           f'{self.__name} varchar(14) NOT NULL,'
                           f'{self.__password} varchar(100) NOT NULL,'
                           f'PRIMARY KEY({self.__id}))')
            self.commit

    def insert(self, username, password):
        match_count = self.check_login(username, password)
        # check insert data
        if match_count == 0:
            # create password digest
            pw_digest = self.__digest(password)

            # execute insert sql
            cursor = self.get_cursor()
            sql = f'INSERT INTO {self.__tablename}({self.__name},{self.__password}) VALUES(%s, %s)'
            cursor.execute(sql, (username, pw_digest))
            self.commit

            return ''
        else:
            return 'Insert Error : Used Data'

    def update(self, username, befor_pw, after_pw):
        # check table data
        if self.check_login(username, befor_pw) != 0:
            # create befor and after digest
            befor_digest = self.__digest(befor_pw)
            after_digest = self.__digest(after_pw)

            # execute update sql
            cursor = self.get_cursor()
            sql = f'UPDATE {self.__tablename} SET {self.__password}=%s WHERE {self.__name}=%s AND {self.__password}=%s'
            cursor.execute(sql, (after_digest, username, befor_digest))
            self.commit

            return ''
        else:
            return 'Update Error : username or password Not Found'

    def __digest(self, password):
        # create configini class
        configini = settings.configini()
        # get salt and bytes encode
        salt = base64.b64encode(bytes(configini.Salt, 'utf-8'))
        password = bytes(password, 'utf-8')
        digest = hashlib.sha256(salt + password).hexdigest()
        # stretching
        for _ in range(1000):
            digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()

        # 上の処理と同じ：hashlib.pbkdf2_hmac('sha256', bytes(digest, 'utf-8'), salt, 1000)
        return digest

    def check_login(self, username, password):
        """
        MysqlのDBを参照し値が登録されているか確認する。

        Parameters
        ----------
        username : string
            ユーザ名。
        password : string
            パスワード。

        Returns
        -------
        cursor.rowcount : int
            Select SQLで一致した件数。
        """
        # create password digest
        create_digest = self.__digest(password)

        # execute select sql
        cursor = self.get_cursor()
        sql = f'SELECT * FROM {self.__tablename} WHERE {self.__name}=%s AND {self.__password}=%s'
        cursor.execute(sql, (username, create_digest))
        cursor.fetchall()

        return cursor.rowcount
