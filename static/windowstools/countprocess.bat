@echo off

set user=jaoliu

FOR /L %%A IN (1,1,21) DO (
  tasklist /FO csv > "C:\Users\%user%\Documents\HpRockets\systemprocess\tasklist_%%A.csv"
  timeout 180 /nobreak
)

pause