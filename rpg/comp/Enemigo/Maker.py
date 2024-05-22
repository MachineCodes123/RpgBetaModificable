import json
import random
import os
import time



class Enemigo:
    def __init__(self,command):
        a = 0
        
        #configuracion interna de probabilidad
        ProbabilidadDeTabla = 3000
        self.prob = ProbabilidadDeTabla
        
        
        
        #cargar datos en memoria de arranque del juego
        temp = []
        for dirAct, _, archivos in os.walk("comp/Enemigo/Enemigos/"):
            max = len(archivos)
            for archivo in archivos:
                with open(dirAct + "/" + archivo, "r") as file:
                    data = json.load(file)
                    temp.append(data)
                    a += 1
                print("Cargando Enemigos: ",archivo)
                if a >= max:
                    print("carga Terminada")             
        time.sleep(1)
                
        self.data = temp
        self.commandClear = command 
        
    def crear(self,player):
        self.dataInv = {}
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json","r") as file:
                self.dataInv = json.load(file)
                
        dataUnq = random.choice(self.data)
        
        self.player = player
        armadura = 0
        
        if "armadura" in self.player:
            self.player["vida"]+=player["armadura"]["hpExtra"]
            armadura = player["armadura"]["def"] * 0.75
        self.playerDefensa = (armadura + player["def"]*0.25)
        
        DropMul = 1.20
        StrMul = 1.25
        DefMul = 1.25
        HpMul = 1.25
        
        
        self.dataU = {
        "name":dataUnq["name"],
        "str":random.randint(dataUnq["strMin"]*(player["lv"]*0.25),dataUnq["strMax"]+ int(dataUnq["strMax"]*(player["lv"]*StrMul))),
        "vida":random.randint(dataUnq["vidaMin"]*(player["lv"]*0.25),dataUnq["vidaMax"]+ int(dataUnq["vidaMax"]*(player["lv"]*HpMul))),
        "exp":random.randint(dataUnq["expMin"],dataUnq["expMax"]+int(dataUnq["expMax"]*(player["lv"]*DropMul))),
        "velocidad":random.randint(dataUnq["velocidadMin"]*(player["lv"]*0.25),dataUnq["velocidadMax"]+int(dataUnq["velocidadMax"]*(player["lv"]*0.05))),
        "coin":random.randint(dataUnq["coinMin"]*(player["lv"]*0.25),dataUnq["coinMax"]+int(dataUnq["coinMax"]*(player["lv"]*DropMul))),
        "def":random.randint(dataUnq["defMin"]*(player["lv"]*0.25),dataUnq["defMax"]+int(dataUnq["defMax"]*(player["lv"]*DefMul)))
        }
        if "tableID" in dataUnq:
            self.dataU["tableID"] = dataUnq["tableID"]
            
        self.batalla()
        
        
    def sacarTabla(self):
        if os.path.exists("comp/Enemigo/drop/" + self.dataU["tableID"] + ".json"):
            with open("comp/Enemigo/drop/" + self.dataU["tableID"] + ".json","r") as file:
                tabla = json.load(file)
            
            
            Probabilidad_de_tabla_maxima = self.prob
            randNum = random.randint(1,Probabilidad_de_tabla_maxima)
            
            if randNum >= 1 and randNum <= 2000:
                type = "normal"
            if randNum >= 2001 and randNum <= 3000:
                type = "epic"
            
            
            self.tabla = random.choice(tabla[type])
            
            
    #sector de batalla
    
    def batalla(self): 
        
        while True:
            
            #Perdido
            os.system(self.commandClear)
            if self.player["vida"] < 1:
                print("Perdiste")
                time.sleep(0.5)
                break
            
            #Ganado
            elif self.dataU["vida"] < 1:
                print("*"*5,"Ganaste ","*"*5)
                self.player["exp"]+=self.dataU["exp"]
                self.player["vida"]=self.player["vidaMax"]
                self.player["coin"]+=self.dataU["coin"]
                print(f"Exp reunido {self.dataU['exp']}")
                
                if os.path.exists("comp/User/inventory.json"):
                    with open("comp/User/inventory.json","r") as file:
                        self.dataInv = json.load(file)

                
                if "tableID" in self.dataU:
                    self.sacarTabla()
                    name = self.tabla["name"]
                    id = self.tabla["id"]
                    grad = self.tabla["grad"]
                    price = self.tabla["price"]
                    type = self.tabla["type"]
                    
                    print(f"Ganaste un {type} de grado {grad} llamado {name} su id es {id}")          
                    cantidad = random.randint(self.tabla["countMin"], self.tabla["countMax"])
                    print(f"cantidad x" + str(cantidad))
                        
                    
                    if id in self.dataInv:
                        self.dataInv[id]["count"] += cantidad
                    else:
                        self.dataInv[id] = {"count":cantidad,"name":name,"id":id,"grad":grad,"type":type,"price":price}

                        if "def" in self.tabla:
                            self.dataInv[id]["def"] = self.tabla["def"]
                        if "hp" in self.tabla:
                            self.dataInv[id]["hp"] = self.tabla["hp"]
                        if "atk" in self.tabla:
                            self.dataInv[id]["atk"] = self.tabla["atk"]
                            
                            
                    with open("comp/User/inventory.json","w") as file:
                        json.dump(self.dataInv,file)
   
                    
                with open("comp/User/stats.json","w") as file:
                    json.dump(self.player,file)
                time.sleep(3)
                break
                
            #Centro grafico a texto enemigo
            print("Nombre enemigo: ",self.dataU["name"])
            print("Fuerza enemiga: ",self.dataU["str"])
            print("Vida enemiga: ",self.dataU["vida"])
            print("Defensa enemiga:",self.dataU["def"])
            print("Velocidad enemiga: ",self.dataU["velocidad"])
            
            #centro grafico player
            print("\nvida: ",self.player["vida"])
            print("Fuerza: ",self.player["str"])
            print("Velocidad: ",self.player["velocidad"])
            print("Defensa: ",self.player["def"])
            if "armadura" in self.player:
                print("Defensa de armadura: ",self.player["armadura"]["def"])
            print(f"Defensa calculada: {self.playerDefensa}")
            
            print("\n1. Atacar")
            if self.dataInv:
                if "POC" in self.dataInv:
                    print("2. Curar con pocion")
                    
                    
            
            op = input("Entrada: ")
            
            #operar opcion
            if op == "1":
                
                arma = 0
                if "arma" in self.player:
                    arma = self.player["arma"]["atk"]*0.25
                    
                
                dañoCalculado = max(0,self.player["str"]-(self.dataU["def"]*0.35)+arma)
                
                dañoRecibido = max(0,self.dataU["str"]-self.playerDefensa)
                
                print("daño recibido: ",dañoRecibido)
                
                if self.player["velocidad"] > self.dataU["velocidad"]:
                    self.player["vida"]-=dañoRecibido
                    self.dataU["vida"]-=dañoCalculado
                else:
                    self.dataU["vida"]-=dañoCalculado
                    self.player["vida"]-=dañoRecibido
                
                time.sleep(0.4)
            
            if os.path.exists("comp/User/inventory.json"):
                with open("comp/User/inventory.json","r") as file:
                    self.dataInv = json.load(file)
                    
                if "POC" in self.dataInv and self.dataInv["POC"]["count"] and self.player["vida"] <= self.player["vidaMax"]:
                    if op == "2":
                        self.dataInv["POC"]["count"]-=1
                        self.player["vida"]+=self.dataInv["POC"]["hp"]
                
                if os.path.exists("comp/User/inventory.json"):
                    with open("comp/User/inventory.json","w") as file:
                        json.dump(self.dataInv,file)
   