# Introduction
For the purposes of this I successfully tested installed this on the OrangePi 3B running Ubuntu 20.04, using the device NI-USB-HS

# Step 1: Head over to linux-gpib and download the latest version
1. [https://sourceforge.net/projects/linux-gpib/files/](https://sourceforge.net/projects/linux-gpib/files/)
2. Click download latest version

# Step 2: Download your device's kernel headers
1. This will be dependent on the device your using, for a Raspberry Pi you can use this repo and [guide](https://github.com/JoshHarris2108/NI-GPIB-USB-HS-PyVisa-install-on-Raspberry-Pi-4)
2. For the OrangePi 3B you can find the kernel headers [here](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-Pi-3B.html) under official tools>linux kernel header>linux-header-legacy
3.  Install the file
```bash
sudo apt install ./linux-headers-legacy-rockchip-rk356x_1.0.0_arm64
```

# Step 3: Install dependencies and unzip linux-gpib
1. Install make tools
```bash
sudo apt-get install tk-dev build-essential texinfo texi2html libcwidget-dev libncurses5-dev libx11-dev binutils-dev bison flex libusb-1.0-0 libusb-dev libmpfr-dev libexpat1-dev tofrodos subversion autoconf automake libtool mercurial
```
2. cd into the folder you downloaded linux-gpib and unzip it
```bash
cd <directory containing linux-gpib>
tar xzf linux-gpib-4.3.4.tar.gz 
```
3. Inside the unzipped linux-gpib folder contains two more zipped files for the kernel and user
4. Unzip both
```bash
cd linux-gpib-4.3.4
tar xzf linux-gpib-kernel-4.3.4.tar.gz
tar xzf linux-gpib-user-4.3.4.tar.gz
```
# Step 4: Configure using linux-gpib-user
If you get lost you can also read the install file inside linux-gpib-user
1. cd into linux-gpib-user-4.3.4
```bash
cd linux-gpib-user-4.3.4
```
2. Configure the directory to your architechure
```bash
./bootstrap
./configure --sysconfdir=/etc
```
3. Build
```bash
make
sudo make install
sudo ldconfig #updates libraries
```
# Step 5: Install kernel part using linux-gpib-user
1. cd into the other unzipped directory linux-gpib-kernel-4.3.4
```bash
cd linux-gpib-kernel-4.3.4
```
2. Make and install
```bash
make
make install
```
3. Check if Check NI-GPIB-USB-HS is detected
```bash
lsusb | grep GPIB
```
Expected output: ```Bus 001 Device 005: ID 3923:709b National Instruments Corp. GPIB-USB-HS```

4. Load kernel module
```bash
sudo modprobe ni_usb_gpib
sudo ldconfig
lsmod |grep gpib
```
Expected outcome:
```bash
ni_usb_gpib            36864  0
gpib_common            45056  1 ni_usb_gpib
```

# Step 6: Configure the gpib.conf
This depends on your use case for this I'll be configuring for NI-usb-gpib-hs
1. Create and edit config file, if it already exists remove everything and put only this (if ur using just the ni_usb_gpib)
```bash
sudo nano /usr/local/etc/gpib.conf
```

File contents
```
interface {
        minor = 0
        board_type = "ni_usb_b"
        pad = 0
        master = yes
}
```
Save and exit Ctrl+X, Y, enter

2. Test GPIB config
```bash
sudo gpib_config
```
Expected outcome: no output/ error
3. Test communication with device
```bash
sudo ibtest
```
```bash
- d 
- Enter device address 0
- w
- *IDN?
- r 
- 100
```

# Step 7: Create user group with permission to interact with gpib
1. Create new group and join it
```bash
whoami #to get username
sudo groupadd gpib
sudo usermod -aG gpib yourusername
```
2. Set group for gpib devices
```bash
sudo chgrp gpib /dev/gpib*
sudo chmod 660 /dev/gpib*
```
3. Persist rule on reboot
```bash
sudo nano /etc/udev/rules.d/99-gpib.rules
```
insert this line
```
KERNEL=="gpib*", SUBSYSTEM=="misc", GROUP="gpib", MODE="0660"
```

save the file (Ctrl+X, Y, enter)

4. Reload rules
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```
5. Verify changes
```bash
ls -l /dev/gpib*
```
Expected outcome: You should see the group set to gpib and the permissions set to `crw-rw----`.

6. Verify Group membership
```bash
groups yourusername
```
7. Reboot and reverify membership, group rules and `lsusb | grep GPIB`

# Testing with PyVisa
1. Clone this repo and cd in `git clone https://github.com/ryryry-3302/linux-gpib.git && cd linux-gpib`
2. Install requirements `pip install -r requirements.txt`
3. Run test.py `python test.py`

 
