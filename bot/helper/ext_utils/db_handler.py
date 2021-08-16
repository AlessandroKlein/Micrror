import psycopg2
from psycopg2 import Error
from bot import AUTHORIZED_CHATS, SUDO_USERS, DB_URI, LOGGER

class DbManger:
    def __init__(self):
        self.err = False

    def connect(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as error :
            LOGGER.error("Error en dbMang : ", error)
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_auth(self,chat_id: int):
        self.connect()
        if self.err :
            return "Hay un registro de verificación de errores para obtener más detalles"
        else:
            sql = 'INSERT INTO users VALUES ({});'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.add(chat_id)
            return 'Authorized successfully'

    def db_unauth(self,chat_id: int):
        self.connect()
        if self.err :
            return "Hay un registro de verificación de errores para obtener más detalles"
        else:
            sql = 'DELETE from users where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.remove(chat_id)
            return 'No autorizado con éxito'

    def db_addsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "Hay un registro de verificación de errores para obtener más detalles"
        else:
            if chat_id in AUTHORIZED_CHATS:
                sql = 'UPDATE users SET sudo = TRUE where uid = {};'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                SUDO_USERS.add(chat_id)
                return 'Exitosamente promovido como Sudo'
            else:
                sql = 'INSERT INTO users VALUES ({},TRUE);'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                SUDO_USERS.add(chat_id)
                return 'Autorizado y promocionado con éxito como Sudo'

    def db_rmsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "Hay un registro de verificación de errores para obtener más detalles"
        else:
            sql = 'UPDATE users SET sudo = FALSE where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.remove(chat_id)
            return 'Eliminado con éxito de Sudo'
