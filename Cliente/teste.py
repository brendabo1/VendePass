def login():
    invalido = True
    while invalido: 
        print("---------------------LOGIN---------------------\n\n")
        print("\033[31m" +"Para Sair insira 'x'" +"\033[0m") 
        user_id = input("ID: ")
        if user_id == 'x' or user_id == 'X':
            break
        password = input("Senha: ")
        
    
login()

 
 