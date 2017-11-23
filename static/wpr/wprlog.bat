@echo off

set path="C:\Users\t19RS3SKU1\Documents\WPR Files\dalforcenumofunderlaypipes_1_realtek_6.0.1.8219.etl"
echo WPA trace will be saved to %path%

set /p path_change="Do you need to change save location? (y/n)"

If /I "%path_change%"=="y" goto changepath
If /I "%path_change%"=="n" goto nochangepath

:changepath
set /p path="Enter save location: "
set /p duration="Enter logging duration in seconds: "

wpr -start GeneralProfile
timeout %duration% /nobreak
wpr -stop %path%
pause

:nochangepath
set /p duration="Enter logging duration in seconds: "

wpr -start GeneralProfile
timeout %duration% /nobreak
wpr -stop %path%
pause