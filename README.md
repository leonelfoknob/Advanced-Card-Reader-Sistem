# Advanced-Card-Reader-Sistem
Advanced Card Reader Sistem

##  all information about project will be share soon for any question feel free to contact me.


To make sistem run automaticaly after raspberry pi boot i use crontab -e command and in the bottom of file i add : @reboot sleep 10 && export DISPLAY=:0 && export XAUTHORITY=/home/leonel/.Xauthority && sudo /usr/bin/python3 /home/leonel/card_main/scripts/main_1.py >> /home/leonel/script_log.txt 2>&1

sleep 10 : is the delay that my app will wait after boot before running it is necesseray because raspberry pi take some time to boot and my app use user interface.
export DISPLAY=:0 && export XAUTHORITY=/home/leonel/.Xauthority : necessery to tell to raspberry pi that app will use gui
sudo /usr/bin/python3 : is the path to use python3
/home/leonel/card_main/scripts/main_1.py >> /home/leonel/script_log.txt 2>&1 : is the location of my app and also create log file for any mistake or issue when app begin.

## web gui
![registration_form](https://github.com/user-attachments/assets/74c56fb5-b4b7-4dae-be16-33417736798b)
![search_user_and_update_credit](https://github.com/user-attachments/assets/ccb168c8-6690-4b2e-bba8-f5b018c8d882)




