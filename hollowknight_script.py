import pymem
import pymem.process
import multiprocessing
import time
import os
import sys

# --- CONFIGURATION ---
process_name = "hollow_knight.exe"
module_name = "UnityPlayer.dll"

pm = pymem.Pymem(process_name)
module_base = pymem.process.module_from_name(pm.process_handle, module_name).lpBaseOfDll

pointer_offsets = [0x0, 0xD8, 0x268, 0xC8]
base_address = module_base + 0x019B8900
current_address = base_address
pointer_value = pm.read_longlong(base_address)

for i in pointer_offsets:
    current_address = pointer_value + i
    pointer_value = pm.read_longlong(current_address)

current_address = pointer_value


def get_health(health_offset=0x190):
    return pm.read_int(current_address + health_offset)


def set_geo(new_geo):
    geo_offset = 0x1C4
    pm.write_int(current_address + geo_offset, new_geo)
    print("Geo successfully set")


def unlimited_soul(run_flag):
   
    while run_flag:
        soul_offset = 0x1CC
        soul = pm.read_int(current_address + soul_offset)
        if soul < 66:
            pm.write_int(current_address + soul_offset, 66)
        time.sleep(0.3)

def god_mode(god_flag):
    invincibilit_offset = 0xBF3
    if god_flag:
        pm.write_bytes(current_address+invincibilit_offset,b'\x01',1)
    else:
        pm.write_bytes(current_address+invincibilit_offset,b'\x00',1) 

def infinite_jump(infijump_flag):
    infinityjump_offset = 0xBF4
    if infijump_flag:
        pm.write_bytes(current_address+infinityjump_offset,b'\x01',1)
    else:
        pm.write_bytes(current_address+infinityjump_offset,b'\x00',1)  

def keys_inventory():

    os.system('cls')

    keys_dictionary  = {
        
        "city_crest" : [0x28D,0],
        "shopkeepers_key":[0x28E,0],
        "elegant_key":[0x290,0],
         "love_key":[0x295,0],
         "kings_brand":[0x296,0],
    }
    keys_list = list(keys_dictionary.keys())


    while True:
        os.system('cls')
        print("Choose Toggle Options")
        print("Press 99 to go back")

        for i in keys_dictionary.keys():
           keys_dictionary[i][1] = int.from_bytes(pm.read_bytes(current_address+keys_dictionary[i][0],1),'little')

        for i,(key,value) in enumerate(keys_dictionary.items()):
            print(f"{i+1}. {key}(Current: {value[1]})")

        choice = int(input("Enter Your Choice: "))

        if choice == 99:
            os.system('cls')
            break

        offset_current_values = keys_dictionary[keys_list[choice-1]]

        pm.write_bytes(current_address+offset_current_values[0],b'\x00' if offset_current_values[1] == 1 else b'\x01',1)
        print("-------------------")
    




if __name__ == "__main__":
    print(f"Reached Player Base at address {hex(current_address)}\n")

    run_flag = False 
    god_flag = pm.read_bytes(current_address+0xBF3,1)
    god_flag = int.from_bytes(god_flag,'little')
    print(f"god: {god_flag}")
    infijump_flag = pm.read_bytes(current_address+0xBF4,1)
    infijump_flag = int.from_bytes(infijump_flag,'little')
    print(f"jump:{infijump_flag}")
    process_soul = None

    while True:
        os.system('cls')
        print("")
        print(f"1. Set Geo (Current: {pm.read_int(current_address+0x1C4)})")
        print(f"2. Toggle Unlimited Soul (Current: {'ON' if run_flag else 'OFF'})")
        print(f"3. Invincibility Mode (Current: {'ON' if god_flag else "OFF"}) ")
        print(f"4. Infinite Jump (Current: {'ON' if infijump_flag else "OFF"}) ")
        print(f"5. Set Nail Damage (Current: {pm.read_int(current_address+0x24C)})")
        print(f"6. Unlock Keys in Inventory")
        print(f"9. Close the Program")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_geo = int(input("Enter the amount: "))
            set_geo(new_geo)

        elif choice == 2:
            if not run_flag:
                run_flag = True
                process_soul = multiprocessing.Process(target=unlimited_soul, args=(run_flag,))
                process_soul.start()
                print("Unlimited Soul ON")
            else:
                run_flag = False
                process_soul.terminate()
                print("Unlimited Soul OFF")

        elif choice == 3:
            if god_flag:
                god_flag = False  
                god_mode(god_flag) 
            else:
                god_flag = True
                god_mode(god_flag)   

        elif choice == 4:
            if infijump_flag:
                infijump_flag = False  
                infinite_jump(infijump_flag) 
            else:
                infijump_flag = True
                infinite_jump(infijump_flag)   

        elif choice == 5:
            pm.write_int(current_address+0x24c,int(input("--->Enter the value: ")))   

        elif choice == 6:
            keys_inventory()  

        elif choice == 9:
            sys.exit()     

        else:
            os.system('cls')
            print("Enter Valid Choice")   
            time.sleep(0.5)               
        print("-------------------------")
        print("")        
