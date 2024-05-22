import json
import os
import time


class sellInt:
    def __init__(self,command):
        
        self.clear = command
        
        inventory = {}
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json","r") as file:
                inventory = json.load(file)
        self.inv = inventory
                
        
    def sell(self,inv,player):
        
        id = input("\n\nColoque la ID: ")
        
        if id in inv:
            try:
                cantidad = int(input("Cantidad a vender: "))
            except Exception as e:
                print("No es un int, se utilizara un item para realizar esto.")
                cantidad = 1
                
            if inv[id]["count"] >= cantidad:
                if "price" in inv[id]:
                    inv[id]["count"] -= cantidad
                    player["coin"] += inv[id]["price"] * cantidad
                    time.sleep(1.2)
                    
                    with open("comp/User/inventory.json","w") as file:
                        json.dump(inv,file)
                    with open("comp/User/stats.json","w") as file:
                        json.dump(player,file)
                    
                else:
                    print("No es un articulo vendible")
                    time.sleep(1.2)
            else:
                print("No posees dicha cantidad")
                time.sleep(1.2)
        else:
            print("No es un item que este en tu inventario.")
            time.sleep(1.2)