import pyaudio
import numpy as np
import pylab
import time
import cv2

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second

def soundplot(stream):
    t1=time.time()
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    pylab.plot(data)
    pylab.title("Audio")
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2,2**16/2])
    pylab.savefig("03.png",dpi=50)
    pylab.close('all')
    # print("took %.02f ms"%((time.time()-t1)*1000))
    

# if __name__=="__main__":
def audio():
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    # for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
    while True:
        soundplot(stream)
        # im = cv2.imread('03.png')
        # cv2.imshow("Audio", im)
        # if cv2.waitKey(1) == 27:
        #     break
    stream.stop_stream()
    stream.close()
    p.terminate()