import threading
import time
import Audio_Record as arec

def threadOne():
    for i in range(0,7):
        print('LED on')
        time.sleep(1)
        print('LED off')

# def threadTwo():
    # arec.audio_rec('OneDrive - University College London/ELEC0036/IBM Project/Code/waisted_rec.wav')


# arec.audio_rec('OneDrive - University College London/ELEC0036/IBM Project/Code/command_rec.wav')
# x = threading.Thread(target = threadOne) #START JUST BEFORE REC
# y = threading.Thread(target = threadTwo) #START JUST BEFORE REC
# x.start()
# arec.audio_rec('OneDrive - University College London/ELEC0036/IBM Project/Code/waisted_rec.wav')
# print('here')

def Thread_BLINK_LED():
    x = threading.Thread(target = threadOne) #START JUST BEFORE REC
    x.start()



# print(threading.active_count())
# # while 1==1:
# #     pass

# print('finished')