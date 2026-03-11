import time
import subprocess
import os
import getpass

def clear():
    subprocess.run(["clear"])
    menu()



def menu():

    print("""
██████╗ ██╗   ██╗      █████╗ ██████╗  ██████╗██╗  ██╗██╗   ██╗
██╔══██╗╚██╗ ██╔╝     ██╔══██╗██╔══██╗██╔════╝██║  ██║╚██╗ ██╔╝
██████╔╝ ╚████╔╝█████╗███████║██████╔╝██║     ███████║ ╚████╔╝ 
██╔═══╝   ╚██╔╝ ╚════╝██╔══██║██╔══██╗██║     ██╔══██║  ╚██╔╝  
██║        ██║        ██║  ██║██║  ██║╚██████╗██║  ██║   ██║   
╚═╝        ╚═╝        ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   
                                                               
=================================================================
                github: https://github.com/piadi-su                       
=================================================================
""")


def start():
    
    while True:
        script_starter = input("start the script[y/n]=> ").lower()

        if script_starter == "y":
            return True

        elif script_starter == "n":
            return False
        

def part(disk, n):
    if disk[-1].isdigit():
        return f"/dev/{disk}p{n}"
    else:
        return f"/dev/{disk}{n}"

def start_user_h_passwd():

    user_name = input("Set your username: ")

    

    root_passwd = getpass.getpass("Set root password: ")
    user_passwd = getpass.getpass(f"Set password for {user_name}: ")

    hostname = input("Set hostname for your system: ")

    return hostname, user_name, root_passwd, user_passwd


def user_h_passwd_chroot(hostname, user_name, root_passwd, user_passwd):
    
    #adding user
    # useradd -m -G wheel,users <user>
    subprocess.run([
        "arch-chroot",
        "/mnt",
        "useradd",
        "-m",
        "-G",
        "wheel,users",
        user_name
        ], check=True)

    # decommenta la riga %wheel in /etc/sudoers
    subprocess.run([
        "arch-chroot", "/mnt",
        "sed", "-i",
        r"s/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/",
        "/etc/sudoers"
    ], check=True)

    # setting the hostname
    with open("/mnt/etc/hostname", "w") as f:
        f.write(hostname + "\n")

    # setting root passwd
    subprocess.run(
        ["arch-chroot", "/mnt", "chpasswd"],
        input=f"root:{root_passwd}\n", text=True, check=True
    )

    # setting root passwd
    subprocess.run(
        ["arch-chroot", "/mnt", "chpasswd"],
        input=f"{user_name}:{user_passwd}\n", text=True, check=True
    )
    


def localization_and_timezone_chroot(timezone, selected_locale):
    #--time-zone--
    # setting timezone
    
    # ln -sf /usr/share/zoneinfo/Europe/Rome /etc/localtime
    # hwclock --systohc
    subprocess.run(["arch-chroot", "/mnt", "ln", "-sf", f"/usr/share/zoneinfo/{timezone}", "/etc/localtime"], check=True)
    subprocess.run(["arch-chroot", "/mnt", "hwclock", "--systohc"], check=True)
    
    
    
    # write in locale.gen
    with open(f"/mnt/etc/locale.gen", "w") as f:
        f.write(f"{selected_locale} UTF-8\n")
    
    # generate the locale
    subprocess.run(["arch-chroot", "/mnt", "locale-gen"], check=True)
    
    # setting system local
    with open(f"/mnt/etc/locale.conf", "w") as f:
        f.write(f"LANG={selected_locale}\n")
    
    print(f"Locale set to {selected_locale} and timezone set to {timezone}")


def start_localization_info():
        # TIMEZONE
    # this is semplified list
    main_regions = ["Africa", "America", "Asia", "Europe", "Pacific", "Atlantic"]
    
    print("Available regions:")
    for i, r in enumerate(main_regions, start=1):
        print(f"{i}. {r}")
    
    # region chosing 
    while True:
        try:
            choice = int(input("Select a region (number)=> "))
            if 1 <= choice <= len(main_regions):
                region = main_regions[choice-1]
                break
            else:
                print("Number out of range, try again.")
        except ValueError:
            print("Invalid input, enter a number.")
    
    # list of the city of the region
    all_cities = [c for c in os.listdir(f"/usr/share/zoneinfo/{region}") if os.path.isfile(f"/usr/share/zoneinfo/{region}/{c}")]
    # print just the most important ones 
    # sample display
    sample_cities = all_cities[:20] if len(all_cities) > 20 else all_cities
    print("Some available cities (for reference):")
    for c in sample_cities:
        print(c)

    # user input
    while True:
        city_choice = input("Type the city name exactly as it appears in zoneinfo => ")
        if city_choice in all_cities:
            city = city_choice
            break
        else:
            print("City not found, try again.")    

    # Build timezone **after** valid city is selected
    timezone = f"{region}/{city}"
    print("Selected timezone:", timezone)
    
    #-----Secondo-part------

    # --- LOCALE ---
    available_locales = [
        "en_US.UTF-8",
        "it_IT.UTF-8",
        "de_DE.UTF-8",
        "fr_FR.UTF-8",
        "es_ES.UTF-8",
        "pt_BR.UTF-8",
        "zh_CN.UTF-8",
        "ja_JP.UTF-8",
        "ko_KR.UTF-8",
        "ru_RU.UTF-8"
    ]
    
    print("Available locales:")
    for i, local in enumerate(available_locales, start=1):
        print(f"{i}. {local}")
    
    while True:
        try:
            locale_choice = int(input("Select your language (number)=> "))
            if 1 <= locale_choice <= len(available_locales):
                selected_locale = available_locales[locale_choice-1]
                break
            else:
                print("Number out of range, try again.")
        except ValueError:
            print("Invalid input, enter a number.")

    return timezone, selected_locale

    
def install_utilities(EFI_BOOT):

    #enable networkmanager for an internet connection at start
    subprocess.run([
        "arch-chroot",
        "/mnt/",
        "systemctl",
        "enable"
        "NetworkManager"
        ], check=True)
    
    #installing boot loader and other pkgs
    subprocess.run([
        "arch-chroot",
        "/mnt/",
        "pacman",
        "-S",
        "grub",
        "man-db",
        "man-pages"
        ], check=True)
    
    if EFI_BOOT:
        subprocess.run([
            "arch-chroot",
            "/mnt/",
            "pacman",
            "-S",
            "efibootmgr"
            ], check=True)



def grub_install_chroot(EFI_BOOT,BIOS_boot_drive):
    
    #GRUB INSTALLATION

    # grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
    if EFI_BOOT:
        subprocess.run([
            "arch-chroot",
            "/mnt/",
            "grub-install",
            "--target=x86_64-efi",
            "--efi-directory=/boot",
            "--bootloader-id=GRUB"
            ], check=True)
    
    # grub-install --target=i386-pc /dev/<disk>
    else:
        subprocess.run([
            "arch-chroot",
            "/mnt/",
            "grub-install",
            "--target=i386-pc",
            BIOS_boot_drive
            ], check=True)

    # making grub config
    # grub-mkconfig -o /boot/grub/grub.cfg
    subprocess.run([
        "grub-mkconfig",
        "-o",
        "/boot/grub/grub.cfg"
        ],check=True)




def main():
    EFI_BOOT = False
    

    menu()
    start_script = start()

    if not start_script:
        return

    clear()
    hostname, user_name, root_passwd, user_passwd = start_user_h_passwd() 
    timezone, locale = start_localization_info()

    #ask for the disk to partition

    #DISK SELECT
    subprocess.run(["lsblk"])
    while True:
        DISK = input("\nselect the this we are going to be using => ")
        confirm_disk = input(f"is this the right disk: {DISK} [y/n] => ").lower()
    
        if confirm_disk == "y":
            break
    
    BOOT = part(DISK, 1)
    ROOT = part(DISK, 2)


    EFI_BOOT = os.path.exists("/sys/firmware/efi")

    #DISK PARTITIONING
    
    print("startig the disk partiton")
    

    # deleting old partition
    # sgdisk --zap-all /dev/<disk>

    print("deleting older partition")
    subprocess.run([
        "sgdisk",
        "--zap-all",
        f"/dev/{DISK}"
        ], check=True)
    
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
            f"/dev/{DISK}"
            ], check=True)

    else: #if yout on BIOS
        subprocess.run([
            "sgdisk",
            "--new=1:0:+2M",
            "--typecode=1:ef02",
            "--change-name=1:BIOS boot",
            f"/dev/{DISK}"
            ], check=True)

    
    print("done\n")
    

    #making root partition
    # sgdisk --new=2:0:0 --typecode=2:8300 --change-name=2:"Linux Root" /dev/<disk>
    print("making root partition")
    subprocess.run([
        "sgdisk",
        "--new=2:0:0",
        "--typecode=2:8300",
        "--change-name=2:Linux ROOT",
        f"/dev/{DISK}"
        ], check=True)

    
    print("done\n")
    
        

    
    clear()
    
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

    
    print("done\n")

    clear()

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


    
    print("done\n")

    clear()

    # REFLECTOR
    #use reflector for pacman pkgs
    # reflector --latest 10 --sort rate --save /etc/pacman.d/mirrorlist
    subprocess.run([
        "reflector",
        "--latest", "10",
        "--sort", "rate",
        "--save", "/etc/pacman.d/mirrorlist"
        ], check=True)
    
    #PACSTRAP
    # pacstrap -K /mnt base linux linux-firmware base-devel networkmanager vim
    # intalling kernle and other important things
    subprocess.run([
        "pacstrap",
        "-K",
        "/mnt",
        "base",
        "linux",
        "linux-firmware",
        "base-devel",
        "networkmanager",
        "vim"
        ], check=True)
    
    #FSTAB
    # genfstab -U  /mnt >> /mnt/etc/fstab
    with open("/mnt/etc/fstab", "w") as f:
        subprocess.run(["genfstab", "-U", "/mnt"], stdout=f, check=True)

    clear()

    print("changeing ROOT")
    

    #chroot gen localization
    localization_and_timezone_chroot(timezone, locale)
    
    #setting up ROOT passwd user passwd user and hostname
    user_h_passwd_chroot(hostname, user_name, root_passwd, user_passwd)
    
    #installer of grub and other software
    install_utilities(EFI_BOOT)

    #grub installation
    grub_install_chroot(EFI_BOOT,BOOT)
    
    clear()

    print("THE INSTALLATION is finish")
    reboot = input("do you want to reboot now[y/n]=> ").lower
    
    while True:
        if reboot == "y":
            #unmounting everithing 
            subprocess.run([
                "umount",
                "-R",
                "/mnt"
                ], check= True)

            subprocess.run([
                "reboot"
                ], check=True)

        if reboot == "n":
            break

    return
        
        



if __name__ == "__main__":
    main()



