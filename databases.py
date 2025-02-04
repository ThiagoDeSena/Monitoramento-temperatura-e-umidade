import mariadb

class Database:

    # CONECTA AO BANCO
    def __init__(self,host,user,password,database):

        self.conecao = mariadb.connect(
            user=user,  #usuário criado no mariaDB
            password=password,  #Senha Criada no mariaDB para o usuário 'user01'
            host= host ,#host criado no mariadb para o usuário 'user01'
            database=database    #Nome do banco de teste criado no mariaDB
        )


    # ACESSA O CURSOR DO BANCO
    def get_cursor(self):
        return self.conecao.cursor()

    # FECHA O CURSOR DO BANCO
    def close_connection(self):
        self.conecao.close()


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
        else:
            print("Dado já existe no banco de dados!")