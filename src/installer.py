import time
import subprocess

def clear():
    subprocess.run(["clear"])

def timer():
    for i in range(1, 4):
        time.sleep(1)
        print("." * i)


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
        

def part(disk, n):
    if disk[-1].isdigit():
        return f"/dev/{disk}p{n}"
    else:
        return f"/dev/{disk}{n}"


def main():
    EFI_BOOT = False
    

    menu()
    start_script = start()

    if not start_script:
        return

    clear()

    #ask for the disk to partition

    #DISK SELECT
    menu()
    subprocess.run(["lsblk"])
    while True:
        DISK = input("\nselect the this we are going to be using => ")
        confirm_disk = input(f"is this the right disk: {DISK} [y/n] => ").lower()
    
        if confirm_disk == "y":
            break
    
    BOOT = part(DISK, 1)
    ROOT = part(DISK, 2)


    is_efi = int(subprocess.run(
        ["cat", "/sys/firmware/efi/fw_platform_size"],
        capture_output=True,
        text=True
        ).stdout.strip())

    if is_efi in (32, 64):
        EFI_BOOT = True

    #DISK PARTITIONING
    
    print("startig the disk partiton")
    timer()

    # deleting old partition
    # sgdisk --zap-all /dev/<disk>

    print("deleting older partition")
    subprocess.run([
        "sgdisk",
        "--zap-all",
        f"/dev/{DISK}"
        ], check=True)
    timer()
    print("done\n")
    

    #making boot partition
    # EFI 
    # sgdisk --new=1:0:+2G --typecode=1:ef00 --change-name=1:"EFI System" /dev/<disk>
    # BIOS
    #sgdisk --new=3:0:+2M --typecode=3:ef02 --change-name=3:"BIOS Boot" /dev/<disk>

    print("making BOOT partiton")
    if EFI_BOOT:
        subprocess.run([
            "sgdisk",
            "--new=1:0:+2G",
            "--typecode=1:ef00",
            "--change-name=1:EFI System",
            BOOT
            ], check=True)

    else: #if yout on BIOS
        subprocess.run([
            "sgdisk",
            "--new=1:0:+2M",
            "--typecode=1:ef02",
            "--change-name=1:BIOS boot",
            BOOT
            ], check=True)

    timer()
    print("done\n")
    

    #making root partition
    # sgdisk --new=2:0:0 --typecode=2:8300 --change-name=2:"Linux Root" /dev/<disk>
    print("making root partition")
    subprocess.run([
        "sgdisk",
        "--new=2:0:0",
        "--typecode=2:8300",
        "--change-name=2:Linux ROOT",
        ROOT
        ], check=True)

    timer()
    print("done\n")
    
    #update the kernel to detect the new patiotion


    subprocess.run(["partprobe"], check=True)
        

    
    clear()
    menu()
    
    # MAKING THE FILE SYSTEM
    
    #making the efi file system | if you are on bios u don't need to make it
    # mkfs.fat -F 32 /dev/<disk>1 
    print("making file system")
    if EFI_BOOT:
        subprocess.run([
            "mkfs.fat",
            "-F",
            "32",
            BOOT

            ], check=True)
    
    # making root file sys
    # mkfs.ext4 /dev/<partizione> -> ext4 
    subprocess.run([
        "mkfs.ext4",
        ROOT
        ], check=True)

    timer()
    print("done\n")

    clear()
    menu()

    print("mounting the disks")
    
    #mounting root in /mnt
    #mount /dev/<disk>2 /mnt
    subprocess.run([
        "mount",
        ROOT,
        "/mnt"
        ], check=True)
    
    #if efi mkdir /mnt/boot and mount there

    if EFI_BOOT:

        subprocess.run([
            "mkdir",
            "-p",
            "/mnt/boot"
            ], check=True)

        subprocess.run([
            "mount",
            BOOT,
            "/mnt/boot"
            ], check=True)


    timer()
    print("done\n")

    clear()
    menu()

    # REFLECTOR
    #use reflector for pacman pkgs

    subprocess.run([
        "reflector",
        ""
        ],check=True)







if __name__ == "__main__":
    main()



# # Pulire la tabella delle partizioni esistente
# sgdisk --zap-all /dev/<disk>
#
# # Creare partizione EFI 512 MB
# sgdisk --new=1:0:+2G --typecode=1:ef00 --change-name=1:"EFI System" /dev/<disk>
#patizione bios
#sgdisk --new=3:0:+2M --typecode=3:ef02 --change-name=3:"BIOS Boot" /dev/<disk>

# # Creare partizione root con il resto del disco
# sgdisk --new=2:0:0 --typecode=2:8300 --change-name=2:"Linux Root" /dev/<disk>
#
# # Creare partizione swap di 4 GB alla fine
# sgdisk --new=3:0:+4G --typecode=3:8200 --change-name=3:"Linux Swap" /dev/<disk>
#
# # Scrivere le modifiche


#make at the start a promt for localization timezone user passwd.user passwd.root
