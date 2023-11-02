from ftplib import FTP
import os
import openai

def login():
    ftp_host = input('Insira o endereço IP: ')
    ftp_user = input('Insira o nome de usuário: ')
    ftp_pass = input('Insira a senha: ')

    global ftp
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)

choice = 1
        
def dir_choices():
    print("""
    1 - Listar arquivos e diretórios
    2 - Alterar diretório
    3 - Voltar para a pasta anterior
    4 - Baixar arquivo
    5 - Reescrever arquivo utilizando ChatGPT
    0 - Sair
    """)
    choice = input("Insira um número: ")
    if not choice.isdigit():
        print("""
              Você inseriu um valor inválido!
              Lembre-se de que as opção são de 0 à 5.
              Tente novamente...
              """)
    else:
        return int(choice)

def error_msg():
    os.system('cls')
    print("Opa, algo de errado aconteceu!\nTente novamente...\n")

def FileToText(FileName):
    data = []
    texto = ''

    nome_arquivo = str(FileName)
    ftp.retrlines('RETR ' + nome_arquivo, lambda x, y=data: y.append(x))

    for i in data:
        texto += i + '\n'
        
    return texto

def SendFileToGPT(FileName):
    FileToSend = FileToText(str(FileName))
    api_key = input("Cole aqui a sua chave da API do OpenAI: ")
    api_key = str(api_key)
    pergunta = input("""
                     Modelos de Requisição
                     
                     'Traduza para inglês'
                     'Altere a programação para Python'
                     'Conte quantas letras "A" têm'
                     
                     Insira o que quer fazer com ele: """)
    
    GPTQuestion = str(pergunta)
    GPTQuestion += ":\n"
    GPTQuestion += FileToSend
    
    IDModel = 'gpt-3.5-turbo'
    
    messages = [{
        "role": "user",
        "content": GPTQuestion
    }]
    
    openai.api_key = api_key
    chat_completion = openai.ChatCompletion.create(model= IDModel, messages=messages)
    return chat_completion.choices[0].message["content"]
def CreateDownloadDirectory():
    try:
        download_folder = "./downloads"
        if not os.path.exists(download_folder):
            os.mkdir(download_folder)
    except:
        pass

try:
    login()
    print('Login realizado com sucesso!')
except:
    error_msg()
    login()

path = ftp.pwd()

while choice != 0:
    choice = dir_choices()
    
    if choice == 1:
        try:
            print("===== Arquivos e diretórios =====")
            ftp.dir()
        except:
            error_msg()

    elif choice == 2:
        try:
            ftp.dir()
            directory = input("Insira o nome do diretório: ")
            ftp.cwd(directory)
            path += ""
        except:
            error_msg()
            
    elif choice == 3:
        try:
            print("Menu Inicial")
            ftp.cwd(path)
        except:
            error_msg()
        
    elif choice == 4:
        try:
            CreateDownloadDirectory()
            ftp.dir()
            nome_arquivo = input("Insira o nome do arquivo: ")
            arquivo = open(nome_arquivo, 'wb')
            ftp.retrbinary('RETR ' + nome_arquivo, arquivo.write)
            arquivo.close()
        except:
            error_msg()
    
    elif choice == 5:
        try:
            print("Ainda em fase de testes...")
            print("Aqui estão os arquivos disponíveis: ")
            ftp.dir()
            nome_arquivo = input("Insira o nome do arquivo: ")
            SimOuNao = input("Deseja baixar a resposta?(Y/N): ")
            Resposta = SendFileToGPT(nome_arquivo)
            if SimOuNao in ["Y", "y", "Yes", "yes"]:
                CreateDownloadDirectory()
                NewFile = open("./downloads/{filename}".format(filename=nome_arquivo), "x")
                NewFile.write(Resposta)
                NewFile.close() 
            print(Resposta)
            
        except:
            error_msg()

    elif choice == 0:
        ftp.quit()
