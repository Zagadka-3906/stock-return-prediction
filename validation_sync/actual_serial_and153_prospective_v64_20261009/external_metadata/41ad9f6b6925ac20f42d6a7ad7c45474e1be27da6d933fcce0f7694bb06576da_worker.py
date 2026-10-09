import sys,time,json,os
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
m=MainPublicationMutex('Local\\SaiTi5_MainMutex_actual_two_process_control_20261009');started=time.time();m.acquire();a=time.time();time.sleep(1.5);b=time.time();m.close();Path(sys.argv[2]).write_text(json.dumps({'pid':os.getpid(),'started':started,'acquired':a,'released':b,'events':m.events}))
