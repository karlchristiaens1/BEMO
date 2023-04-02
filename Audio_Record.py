def audio_rec(wav_output_filename):
    import pyaudio 
    import wave
    import raspi_ears_servo as rservo

    #Blinking eyes & raising ears
    rservo.thread_eyes_blink()
    rservo.thread_ears_up()
    
    # Setting initial parameters and sampling settings
    form_1 = pyaudio.paInt32 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 8 # seconds to record
    dev_index = 1 # device index found by p.get_device_info_by_index(ii)
    # wav_output_filename = 'test1.wav' # name of .wav file


    audio = pyaudio.PyAudio() # create pyaudio instantiation


    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
    #Lowering ears
    rservo.thread_ears_down()

def audio_play(path):
    # import required module
    from playsound import playsound
    
    # for playing note.wav file
    playsound(path)
    print('playing sound using  playsound') # "C:\Users\karlc\test1.wav"
#audio_play('/home/pi/Desktop/BEMO/BEMO-main/podcast.mp3')

def audio_play2(path):
    # import required modules
    from pydub import AudioSegment
    from pydub.playback import play
    
    # for playing wav file
    song = AudioSegment.from_wav(path)
    # print('playing sound using  pydub')
    play(song)

def audio_play3(path):
    import os
    import platform
    from pathlib import Path
    from pydub import AudioSegment
    from pydub.playback import play

    AudioSegment.ffmpeg = path_to_ffmpeg()
    platform_name = platform.system()
    if platform_name == 'Windows':
        os.environ["PATH"] += os.pathsep + str(Path(path_to_ffmpeg()).parent)
    else:
        os.environ["LD_LIBRARY_PATH"] += ":" + str(Path(path_to_ffmpeg()).parent)

    def path_to_ffmpeg():
        SCRIPT_DIR = Path(__file__).parent 
        if platform_name == 'Windows':
            return str(Path(SCRIPT_DIR, "win", "ffmpeg", "ffmpeg.exe"))
        elif platform_name == 'Darwin':
            return str(Path(SCRIPT_DIR, "mac", "ffmpeg", "ffmpeg"))
        else:
            return str(Path(SCRIPT_DIR, "linux", "ffmpeg", "ffmpeg"))

    song = AudioSegment.from_mp3('test')
    play(song)

    # # import required modules
    # from pydub import AudioSegment
    # from pydub.playback import play
    
    # # for playing wav file
    # song = AudioSegment.from_mp3(path)
    # # print('playing sound using  pydub')
    # play(song)

#audio_play2("/home/karlmarc/Desktop/BEMO/BEMO-main/command_rec.wav")
# ~ audio_play("/home/karlmarc/Desktop/BEMO/BEMO-main/command_rec.wav")


def audio_settings():
    import pyaudio 
    import wave

    p = pyaudio.PyAudio() # create pyaudio instantiation
    
    # Get all audio devicess
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i).get('name'))

    # Get the sample rate and the number of channels that the selected device supports
    sample_rate = (p.get_device_info_by_host_api_device_index(0, 2).get('defaultSampleRate'))
    device_channels = (p.get_device_info_by_host_api_device_index(0, 2).get('maxInputChannels'))

    print('Input device sample rate is ', sample_rate)
    print('Input device channels is ', device_channels)

# ~ audio_settings()
# ~ audio_rec('testing_audio.wav')
