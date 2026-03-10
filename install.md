main.c	logica principale, loop menu, chiamata alle funzioni dei moduli
disk.c / disk.h	funzioni per rilevare dischi, selezione disco
partition.c / partition.h	struct Partition, creazione partizioni, formattazione
keyboard.c / keyboard.h	gestione layout tastiera
install.c / install.h	montaggio, pacstrap, generazione fstab
utils.c / utils.h	funzioni di supporto, ad esempio run_cmd() per eseguire comandi shell

# cat /sys/firmware/efi/fw_platform_size
res 64, 32 efi

non == bios


/////////////////////
guida per l'installazione

lsblk

partizione disco selezionato

//BOOT
bios:
+2M = if on bios
code = ef02

efi:
+2G
code = EF00

<!-- //swapp -->
<!-- n  -->
<!-- enter -->
<!-- +ram / 2 = half ram | ram + halfram -->
<!-- code = 8200 -->

//Root
tutto lo spazio
code = 

///////////////////////////////
//FARE file system

//BOOt

//efi
mkfs.fat -F 32 /dev/sda1 

//bios
non server



//ROOT
mkfs.ext4 /dev/<partizione> -> ext4 


//SWAP

<!-- mkswap /dev/<p swap> -->
<!-- swapon /dev/<p swap> -->


//////////////////////////////////

//DISK MOUNTING

//root
mount /dev/<rootpart> /mnt/

if efi
mkdir -p /mnt/boot
mount /dev/<efi part> /mnt/boot

if bios
don't mount


////////////////////////////

//reflecotr per pacchetti pacman
reflector --country IT --latest 5 --sort rate --save /etc/pacman.d/mirrorlist


//install the linux kernel
pacstrap -K /mnt base linux linux-firmware base-devel networkmanager

//make fstaba

genfstab -U  /mnt >> /mnt/etc/fstab

//////////////////

//chroot
arch-chroot /mnt

// da qui in poi fare i comnadi con arch-chroot /mnt <comando>




PARTE DIFFICILE
///////////////////////////////
//info zone
ln -sf /usr/share/zoneinfo/Europe/Rome /etc/localtime

hwclock --systohc


//localization | timezone

vim /etc/locale.gen

locale-gen

en_US.UTF-8
en_US.ISO-8859-1

i can just lunch them in the file no need to uncomment them

/////


//lengage
echo "LANG=en_US.UTF-8" > /etc/locale.conf





////////////////////////////////////////

echo "<hostname>" >> /etc/hostname

//////////////////utenti
root pw/

useradd -m -G wheel,users <user>
passwd <user>
////////////////////////////////////






////////////////
//network enable
systemctl enable NetworkManager

/////////
//bootloader


pacman -S grub man-db man-pages efibootmgr 

///install grub efi


grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB


/////install grub bios


////making grub conf
grub-mkconfig -o /boot/grub/grub.cfg

//////////
FINE
/////////

/// smonto tutto
umount -R /mnt 


reboot

///////////// FINE TUTTA INSTALLAZIONE


//post installation guide

/to enable sudo on out user
EDITOR=vim visudo


uncomment 

## Uncomment to allow members of group wheel to execute any command
%wheel ALL=(ALL:ALL) ALL --uncoment this line 

## Same thing without a password
# %wheel ALL=(ALL:ALL) NOPASSWD: ALL

## Uncomment to allow members of group sudo to execute any command
# %sudo ALL=(ALL:ALL) ALL


//update

sudo pacman -Syu

//download git for yay

sudo pacman -S git

//install yay

git clone https://aur.archlinux.org/yay

cd yay

makepkg -si

//remove the dir if u want

rm -rf yay


