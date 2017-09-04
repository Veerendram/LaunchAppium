@echo off
start "AppiumService" /MIN python LaunchAppium.py --option status
exit 0