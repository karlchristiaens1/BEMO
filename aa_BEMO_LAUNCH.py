import Command
import HMS
import raspi_ears_servo as rb
import time
import random

start_num = 300 # 5min
end_num = 480 # 8min
bemo_path = '/home/karlmarc/Desktop/BEMO/BEMO-main/'

while 1:
	pass
	time.sleep(random_num = random.randint(start_num, end_num)) # Between 5-8min
	arec.audio_play(bemo_path + 'Sounds/bemo_grunt.mp3') # Grunts to seek attention
	
	# ~ time.sleep(0.1)
	
