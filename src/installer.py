import time
import os
import subprocess

def clear():
    os.system("clear")



def menu():

    print("""
======================================
=|  PIADI: ARCH-INSTALLATION SCRIPT |=
======================================
github: https://github.com/piadi-su


""")


def start():
    
    while True:
        script_starter = input("start the script[y/n]: ").lower()

        if script_starter == "y":
            return True

        elif script_starter == "n":
            return False
        

def main():
    EFI_BOOT = False
    BIOS_BOOT = False
    

    menu()
    start_script = start()

    if not start_script:
        return

    clear()

    #ask for the disk to partition
    menu()
    os.system("lsblk")
    while True:
        DISK = input("\nselect the this we are going to be using => ")
        confirm_disk = input(f"is this the right disk: {DISK} [y/n] => ").lower()
    
        if confirm_disk == "y":
            break
    

    is_efi = int(subprocess.run(
        ["cat", "/sys/firmware/efi/fw_platform_size"],
        capture_output=True,
        text=True
        ).stdout.strip())

    if is_efi == "64" or is_efi == "32":
        EFI_BOOT = True
    else:
        BIOS_BOOT = True



      

            
    
    




if __name__ == "__main__":
    main()


