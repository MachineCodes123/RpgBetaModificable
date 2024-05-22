from comp.Enemigo.Maker import Enemigo
from comp.shop.shop import shopInst
from comp.shop.sell import sellInt
from comp.bag.view import bagInt


import os
import json
import time

osDetect = os.name

if osDetect == "posix":
    command = "clear"
elif osDetect == "nt":
    command = "cls"
    
EnemigoIst = Enemigo(command)
shopIst = shopInst(command)
bagIst = bagInt(command)
sellIst = sellInt(command)

def core():
    os.system(command)
    
    if os.path.exists("comp/User/stats.json"): 
        with open("comp/User/stats.json","r") as file:
            player = json.load(file)
        
        print(f"Lv: {player['lv']}")
        print(f"exp actual: {int(player['exp'])}")
        print(f"Money: {int(player['coin'])}")
        print("\n")
    
    print("0. Crear jugador")
    print("1. Pelear")
    print("2. Level Up")
    print("3. Agregar puntos")
    print("4. Tienda")
    print("5. Equipar item")
    print("6. Stats")
    print("7. Bolsa")
    print("8. Vender")
    
    op = input("entrada: ")
    
    #esto seria el stats de reinicio, puede ser modificado (para hacer sus Mod)
    #Lean el readme, en todo caso No Usen el codigo con fines de lucro para si mismos.
    #psdt: estoy en movimiento ya que ando en un transporte
    
    
    if op == "0":
        player = {
        "vida":100,
        "str":7,
        "exp":0,
        "lv":1,
        "coin":500,
        "expMax":100,
        "vidaMax":100,
        "point":0,
        "velocidad":5,
        "def":10
        }
        
        with open("comp/User/stats.json","w") as file:
            json.dump(player,file)
    
    if op == "1":
        if os.path.exists("comp/User/stats.json"): 
            with open("comp/User/stats.json","r") as file:
                player = json.load(file)
                
            EnemigoIst.crear(player)
        else:
            print("Error de lectura Prueba usar 0 (crear jugador)")
    
    if op == "2":
        if player["exp"] >= player["expMax"]:
            player["exp"]-=player["expMax"]
            player["expMax"]+= (player["expMax"] * 0.35)
            player["lv"]+=1
            player["point"]+=4
            print(f"Ganaste LV ahora eres {player['lv']} y ganaste 4 puntos actualmente posees {player['point']}")
            time.sleep(1.4)
            if os.path.exists("comp/User/stats.json"): 
                with open("comp/User/stats.json","w") as file:
                    json.dump(player,file)
                    
        else:
            print(f"te falta EXP alrededor de {int(player['expMax']-player['exp'])}")
            time.sleep(1.4)
    
    if op == "3":
        os.system(command)
        cat = ["atk","spd","hp"]
        
        print(f"puntos actuales: {player['point']}")
        
        print("hp")
        print("spd")
        print("atk")
        
        entrada = input("Categoria: ")
        try:
            cantidad = int(input("Puntos usados: "))
        except Exception as e:
            print("No es un int, se utilizara un punto para realizar esto.")
            cantidad = 1
        
        if player["point"] >= cantidad:
            if entrada.lower() in cat and os.path.exists("comp/User/stats.json"):
                with open("comp/User/stats.json","r") as file:
                    player = json.load(file)
                        
                if entrada == "hp":
                    player["vida"] += 5*cantidad
                    player["vidaMax"] += 5*cantidad
                    
                    mensaje = f"{5*cantidad} en vida maxima"

                    
                    player["point"] -= cantidad
                
                if entrada == "atk":
                    player["str"] += 2*cantidad
                    
                    mensaje = f"{2*cantidad} en ataque"
                    
                    player["point"] -= cantidad
                
                if entrada == "spd":
                    
                    mensaje = f"{5*cantidad} en velocidad"
                    
                    player["velocidad"] += 5*cantidad
                    
                    player["point"] -= cantidad
                
                if os.path.exists("comp/User/stats.json"): 
                    with open("comp/User/stats.json","w") as file:
                        json.dump(player,file)
                        
                print("Ganaste ",mensaje)
                time.sleep(1.4)
                
            else:
                print("No es una categoria...")
                time.sleep(1.4)
        else:
            print("No tienes puntos suficientes")
            time.sleep(1.4)
        
    if op == "4":
        shopIst.shop(player)
        
    if op == "5":
        os.system(command)
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json", "r") as file:
                data = json.load(file)
            
            bagIst.view(data,False,True)
            
            id = input("ID de item a equipar: ")                       
            
            if id in data and data[id]["count"] > 0:
                item = data[id]
                if item["type"] == "prot":
                    player["armadura"] = {"def": item["def"], "hpExtra": item["hp"],"name":item["name"],"id":id}
                    item["count"] -= 1
                if item["type"] == "arma":
                    player["arma"] = {"atk": item["atk"],"name":item["name"],"id":id}
                    item["count"] -= 1
                
                # Actualizar el archivo de inventario con los datos del inventario actualizados
                with open("comp/User/inventory.json", "w") as file:
                    json.dump(data, file)
                with open("comp/User/stats.json", "w") as file:
                    json.dump(player, file)
                print("Item equipado exitosamente.")
                time.sleep(1.4)
            else:
                print("ID de item no válido.")
                time.sleep(1.4)
        else:
            print("El archivo de inventario no existe.")
            time.sleep(1.4)
        
    if op == "6":
        os.system(command)
        armadura = ""
        armaduraDef = ""
        arma = ""
        
        if "armadura" in player:
            armadura = f"+ {player['armadura']['hpExtra']}"
            armaduraDef = f"+ {player['armadura']['def']}"
        if "arma" in player:
            arma =f"+ {player['arma']['atk']}"
            
        print("vida: ",player["vida"], armadura)
        print("def: ",player["def"], armaduraDef)
        print("atk: ",player["str"], arma)
        print("speed: ",player["velocidad"])
       
        input("")
    
    if op == "7":
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json", "r") as file:
                inv = json.load(file)   
            bagIst.view(inv,True,False)
        
    if op == "8":
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json", "r") as file:
                inv = json.load(file)   
            bagIst.view(inv,False,False)
            sellIst.sell(inv,player)

while True:
    core()