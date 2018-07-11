### aliases ###
sudo nano /home/pi/.bash_aliases

alias led_server_log='sudo journalctl -e -f -n 50 -o cat -u led_server.service'
alias led_server_log_all='sudo journalctl --no-tail --no-pager -m -o cat -u led_server.service'
alias led_server_stop='sudo systemctl stop led_server.service'
alias led_server_restart='sudo systemctl restart led_server.service'
alias led_server_client='/home/pi/Public/infra/scripts/run_client.sh'

### systemd service ###
sudo sh -c "cat > /lib/systemd/system/led_server.service <<EOF
[Unit]
Description=Interactive Leds Server
After=multi-user.target
[Service]
Type=simple
ExecStart=/bin/bash /home/pi/Public/interactive_leds/run_game_server.sh catch_game.Catch
TimeoutSec=6
[Install]
WantedBy=multi-user.target
EOF"
# after changing led_server.service run daemon-reload
sudo chmod 644 /lib/systemd/system/led_server.service
sudo systemctl daemon-reload
sudo systemctl enable led_server.service
sudo systemctl start led_server.service
# save journalctl logs
sudo mkdir /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo sh -c "cat >> /etc/systemd/journald.conf <<EOF
SystemMaxUse=10M
EOF"
sudo systemctl restart systemd-journald

### wifi ###
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
network={
	ssid="Mada_WiFi_1"
	psk="********"
}
network={
	ssid="Mada_Bet_Melacha"
	psk="********"
}

### volume ###
amixer set PCM 96%
amixer set Speaker 96%
sudo nano /etc/asound.conf
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw           
    card 1
}
alsamixer

### python3 packages ###
sudo pip3 install --upgrade ipython rpyc smbus2 pyalsaaudio
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev python3-dev python3-numpy -y
sudo pip3 install --upgrade Pillow pygame
cd ~/Public && git clone https://github.com/arduino12/infra
git clone https://github.com/arduino12/rpi-rgb-led-matrix

cat <<EOF | sudo tee /etc/modprobe.d/blacklist-rgb-matrix.conf
blacklist snd_bcm2835
EOF

sudo update-initramfs -u
sudo reboot

/boot/cmdline.txt
isolcpus=3

sudo apt-get remove bluez bluez-firmware pi-bluetooth triggerhappy pigpio
sudo timedatectl set-ntp false
sudo systemctl stop cron

make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
cd ~/Public/rpi-rgb-led-matrix/utils
make led-image-viewer

sudo i2cdetect -y 1
sudo i2cset -y 1 0x70 0 1

sudo /home/pi/Public/rpi-rgb-led-matrix/examples-api-use/demo --led-rows 16 --led-cols 32 --led-chain 4 --led-brightness 90 --led-pwm-bits 8 --led-show-refresh --led-parallel 1 --led-gpio-mapping free-i2c --led-pixel-mapper 'Snake' --led-multiplexing 4 --led-slowdown-gpio 2 --led-pwm-dither-bits 0 -D9
