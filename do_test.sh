nohup python ~/WorkStation/Test_1_RestFulApi/manage.py --port=5001 --mode=test > ~/WorkStation/Test_1_RestFulApi/nohup_output.log 2>&1 &
tail -f nohup_output.log
