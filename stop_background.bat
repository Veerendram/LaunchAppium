@echo off
start "AppiumService" /MIN python LaunchAppium.py --option stop
exit 0