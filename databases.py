import mariadb
import datetime

class Database:

    # CONECTA AO BANCO
    def __init__(self,host,user,password,database):
        self.conecao = mariadb.connect(
            user=user,  #usuário criado no mariaDB
            password=password,  #Senha Criada no mariaDB para o usuário 'user01'
            host= host ,#host criado no mariadb para o usuário 'user01'
            database=database    #Nome do banco de teste criado no mariaDB
        )
        self.insertion_count = 0
        self.max_insertions = 100 # Número máximo de inserções antes da limpeza


    # ACESSA O CURSOR DO BANCO
    def get_cursor(self):
        return self.conecao.cursor()

    # FECHA O CURSOR DO BANCO
    def close_connection(self):
        self.conecao.close()

    #Limpar dados duplicados de data na tabela
    def clean_duplicate_data(self):
        try:
            cursor = self.conecao.cursor()

            cursor.execute("""
                DELETE t1
                FROM valores t1
                INNER JOIN (
                    SELECT data, MIN(id) AS min_id
                    FROM valores
                    GROUP BY data
                    HAVING COUNT(*) > 1
                ) t2 ON t1.data = t2.data AND t1.id <> t2.min_id;
            """)
            self.conecao.commit()
            print(f"{datetime.datetime.now()} - Dados duplicados removidos com sucesso")
        except mariadb.Error as e:
            print(f"{datetime.datetime.now()} - Erro ao remover dados duplicados: {e}")


    # Inserir valores no banco
    def insert_into_database(self,temperatura,umidade,timestamp):
        cursor = self.conecao.cursor()

        #Verifica se o dado já existe
        cursor.execute("SELECT * FROM valores WHERE temperatura=%s AND umidade=%s AND data=%s",(temperatura,umidade,timestamp))
        resultado = cursor.fetchone()

        if not resultado:
            #Insere o dado se ele não existe
            cursor.execute("INSERT INTO valores (temperatura,umidade, data) VALUES (%s,%s,%s)",(temperatura,umidade,timestamp))
            self.conecao.commit()   #Salva as alterações no banco
            self.insertion_count += 1
        else:
            print("Dado já existe no banco de dados!")

        if self.insertion_count >= self.max_insertions:
            self.clean_duplicate_data()
            self.insertion_count = 0 #Reinicia o contador

    def clean_duplicate_data_started(self):
        if self.insertion_count == 0:
                self.clean_duplicate_data()