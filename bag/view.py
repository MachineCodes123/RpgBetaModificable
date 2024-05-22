import json
import os
import time

class bagInt:
    def __init__(self, command):
        self.command = command
        
    def view(self, inv, stopThread, AllowEquipType):
        os.system(self.command)
        if os.path.exists("comp/User/inventory.json"):
            with open("comp/User/inventory.json", "r") as file:
                inv = json.load(file)
            
            temp = {}
            
            for id in inv:
                print("")
                if inv[id]["count"] >= 1:
                    if AllowEquipType == True:
                        if inv[id]["type"] != "item":
                            print(f"nombre: {inv[id]['name']}")
                            print(f"id: {id}")
                            print(f"cantidad: {inv[id]['count']}")
                            print(f"grado: {inv[id]['grad']}")
                            print(f"tipo: {inv[id]['type']}")
                            if "price" in inv[id]:
                                price = inv[id]["price"]
                                print(f"Valor de venta: {price}")
                            
                            
                            if inv[id]['type'] != "item":
                                print("\n====[estadisticas]====")
                                listAtr = ["def", "hp", "atk"]
                                for atr in listAtr:
                                    if atr in inv[id]:
                                        print(f"su {atr}: {inv[id][atr]}")
                    else:
                        
                        print(f"nombre: {inv[id]['name']}")
                        print(f"id: {id}")
                        print(f"cantidad: {inv[id]['count']}")
                        print(f"grado: {inv[id]['grad']}")
                        print(f"tipo: {inv[id]['type']}")
                        if "price" in inv[id]:
                            price = inv[id]["price"]
                            print(f"Valor de venta: {price}")
                            
                        if inv[id]['type'] != "item":
                            print("\n====[estadisticas]====")
                            listAtr = ["def", "hp", "atk"]
                            for atr in listAtr:
                                if atr in inv[id]:
                                    print(f"su {atr}: {inv[id][atr]}")
                            
             
                            
                        
        if stopThread == True:
            input()
