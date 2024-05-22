import json
import os
import time


class shopInst:
    def __init__(self,command):
        temp = {}
        a = 0
        self.command = command
        for dirAct, _, archivos in os.walk("comp/shop/item/"):
            max = len(archivos)
            for archivo in archivos:
                with open(dirAct + "/" + archivo, "r") as file:
                    data = json.load(file)
                    temp[data["id"]] = data
                    file.close()
                    a += 1
                print("Cargando Items: ",archivo)
                if a >= max:
                    print("carga Terminada")             
        time.sleep(1)
                
        self.data = temp
        inventory = {}
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json","r") as file:
                inventory = json.load(file)
        self.inv = inventory
                
        
    def shop(self,player):
        os.system(self.command)
        print("Dinero actual: ",player["coin"],"\n")
        for item in self.data:
            print(f"ID de item: {self.data[item]['id']} Precio: {self.data[item]['price']}$")
            if "atk" in self.data[item]:
                print(f"Ataque del item: {self.data[item]['atk']}")
            if "def" in self.data[item]:
                print(f"Defensa del item: {self.data[item]['def']}")
            if "hp" in self.data[item]:
                print(f"Vida que otorga el item: {self.data[item]['hp']}")
            print("\n")
        
        id = input("ID del item a comprar: ")
        count = input("Cantidad: ")
        
        if not count.isdigit():
            count = 1
        else:
            count = int(count)
            
        if id in self.data:
            op = input("Comprar Y/n: ")
            
            if op.lower() == "y":
                if player["coin"] >= self.data[id]["price"]*count:
                    player["coin"] -= self.data[id]["price"]*count
                    data = self.inv
                    item = self.data[id]
                    
                    if id in data:
                        data[id]["count"] += count
                    else:
                        data[id] = {"name":item["name"],"id":item["id"],"count":count,"grad":item["grad"],"type":item["type"]}
                        
                        if "atk" in item:
                            data[id]["atk"] = item["atk"]
                        if "def" in item:
                            data[id]["def"] = item["def"]
                        if "hp" in item:
                            data[id]["hp"] = item["hp"]
                        if "value" in item:
                            data[id]["value"] = item["value"]
                            
                    print(f'Compra exitosa gastado {self.data[id]["price"]} x {count}')
                    
                    with open("comp/User/inventory.json","w") as file:
                        json.dump(data,file)
                    with open("comp/User/stats.json","w") as file:
                        json.dump(player,file)
                    
                    
                else:
                    print(f"No posees dinero cantidad necesaria para completar el pago {player['coin'] - self.data[id]['price'] }")
            else:
                print("Opcion invalida")
            time.sleep(1.4)
            with open("comp/User/stats.json","w") as file:
                json.dump(player,file)
        