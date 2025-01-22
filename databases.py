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

    # Inserir temperatura no banco
    def insert_temperatura(self,temperatura):
        cursor = self.conecao.cursor()
        cursor.execute("INSERT INTO valores (temperatura, data) VALUES (%s, NOW())",(temperatura,))
        self.conecao.commit()   #Salva as alterações no banco

    
    # Inserir umidade no banco
    def insert_umidade(self,umidade):
        cursor = self.conecao.cursor()
        cursor.execute("INSERT INTO valores (umidade, data) VALUES (%s, NOW())",(umidade,))
        self.conecao.commit()   #Salva as alterações no banco

    # Inserir valores no banco
    def insert_into_database(self,temperatura,umidade):
        cursor = self.conecao.cursor()
        cursor.execute("INSERT INTO valores (temperatura,umidade, data) VALUES (%s,%s, NOW())",(temperatura,umidade))
        self.conecao.commit()   #Salva as alterações no banco