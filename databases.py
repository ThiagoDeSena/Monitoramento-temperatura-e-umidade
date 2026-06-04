import mariadb
import datetime
import time

class Database:

    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conexao = None
        self.insertion_count = 0
        self.max_insertions = 100
        self.connect()

    def connect(self):
        """Tenta se conectar ao banco com retry."""
        try:
            self.conexao = mariadb.connect(**self.config)
            print(f"{datetime.datetime.now()} - Conectado ao banco com sucesso")
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao conectar ao banco: {e}")
            print("Tentando reconectar em 5 segundos...")
            time.sleep(5)
            self.connect()

    def reconnect_if_needed(self):
        """Reconecta ao banco se a conexão estiver inativa."""
        try:
            self.conexao.ping()
        except mariadb.Error:
            print(f"{datetime.datetime.now()} - Conexão perdida. Reestabelecendo...")
            self.connect()

    def insert_into_database(self, temperatura, umidade, timestamp):
        """Insere dados no banco evitando duplicatas e tratando erros."""
        self.reconnect_if_needed()
        cursor = None
        try:
            cursor = self.conexao.cursor()

            # Verifica duplicidade
            cursor.execute(
                "SELECT 1 FROM valores WHERE temperatura=%s AND umidade=%s AND data=%s LIMIT 1",
                (temperatura, umidade, timestamp)
            )
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO valores (temperatura, umidade, data) VALUES (%s, %s, %s)",
                    (temperatura, umidade, timestamp)
                )
                self.conexao.commit()
                self.insertion_count += 1
                print(f"{datetime.datetime.now()} - Dado inserido: T={temperatura}, U={umidade}")

                if self.insertion_count >= self.max_insertions:
                    self.clean_duplicate_data()
                    self.insertion_count = 0
            else:
                print(f"{datetime.datetime.now()} - Dado duplicado ignorado")
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao inserir no banco: {e}")
            self.connect()
        finally:
            if cursor:
                cursor.close()

    def clean_duplicate_data(self):
        """Remove registros duplicados com base na coluna `data`."""
        self.reconnect_if_needed()
        cursor = None
        try:
            cursor = self.conexao.cursor()
            # Define timeout menor para não travar a aplicação
            cursor.execute("SET innodb_lock_wait_timeout = 5")
            cursor.execute("""
                DELETE t1
                FROM valores t1
                INNER JOIN (
                    SELECT data, MIN(id) as min_id
                    FROM valores
                    GROUP BY data
                    HAVING COUNT(*) > 1
                ) t2 ON t1.data = t2.data AND t1.id <> t2.min_id
            """)
            self.conexao.commit()
            print(f"{datetime.datetime.now()} - Duplicatas removidas com sucesso")
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao remover duplicatas (ignorado): {e}")
            try:
                self.conexao.rollback()  # Libera o lock imediatamente
            except:
                pass
        finally:
            if cursor:
                cursor.close()

    def clean_duplicate_data_started(self):
        if self.insertion_count == 0:
            self.clean_duplicate_data()

    def update_setpoint_histerese(self, setpoint=None, histerese=None):
        """Atualiza os valores de setpoint e/ou histerese na tabela configuracoes."""
        self.reconnect_if_needed()
        cursor = None
        try:
            cursor = self.conexao.cursor()
            if setpoint is not None and histerese is not None:
                cursor.execute(
                    "UPDATE configuracoes SET setpoint=%s, histerese=%s WHERE id=1",
                    (setpoint, histerese)
                )
            elif setpoint is not None:
                cursor.execute(
                    "UPDATE configuracoes SET setpoint=%s WHERE id=1",
                    (setpoint,)
                )
            elif histerese is not None:
                cursor.execute(
                    "UPDATE configuracoes SET histerese=%s WHERE id=1",
                    (histerese,)
                )
            self.conexao.commit()
            print(f"{datetime.datetime.now()} - Configurações atualizadas: setpoint={setpoint}, histerese={histerese}")
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao atualizar configurações: {e}")
        finally:
            if cursor:
                cursor.close()

    def get_latest_setpoint_histerese(self):
        """Recupera os últimos valores de setpoint e histerese."""
        self.reconnect_if_needed()
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT setpoint, histerese, data_atualizacao FROM configuracoes WHERE id=1")
            result = cursor.fetchone()
            if result:
                return {
                    "setpoint": result[0],
                    "histerese": result[1],
                    "data_atualizacao": result[2]
                }
            return {
                "setpoint": None,
                "histerese": None,
                "data_atualizacao": None
            }
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao recuperar configurações: {e}")
            return {
                "setpoint": None,
                "histerese": None,
                "data_atualizacao": None
            }
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.conexao:
            self.conexao.close()
