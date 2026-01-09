@echo off
cd /d C:\Users\LENOVO\Desktop\economic-data-pipeline

call C:\Users\LENOVO\anaconda3\Scripts\activate.bat

python scripts\run_pipeline.py >> logs\scheduler.log 2>&1
