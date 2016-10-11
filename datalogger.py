import e32, appuifw, graphics
import key_codes
import positioning
import sensor
import location
import audio
import sysinfo
import camera
import time


counter =0

def handle_redraw(rect):
    canvas.clear()
    canvas.blit(img)


def startrecording():
	global S
	global counter
	t=int(time.time())
	filename="e:\\datalogger\\snd_"+str(t)+".wav"
	S=audio.Sound.open(filename)
	S.record()
	img.point ((10,20),0xff0000,width=20)
	handle_redraw(())

def stoprecording():
	global S
	S.stop()
	S.close()
	


def fncSavedata (data):
   io=open("e:\\datalogger\\gps_travel.log",'a')
   io.write(data +'\n')
   io.close
   return


def cb(event):
    
    global counter
    counter = counter + 1
      
    t=int(time.time())
    sat=event["satellites"]
    tm=sat["time"]  
    tot=sat["satellites"]
    used=sat["used_satellites"]
    pos = event["position"]
    lat=pos["latitude"]
    lng=pos["longitude"]
    alt=pos["altitude"]
    vdop=pos["vertical_accuracy"]
    hdop=pos["horizontal_accuracy"]
    crse=event["course"]
    hdg=crse["heading"]
    hdgacc=crse["heading_accuracy"]
    spd=crse["speed"]
    
    sdb=sysinfo.signal_dbm()
    loc = location.gsm_location()
    sloc = str(loc)
    sloc = sloc.replace(',','/')

    global S
    sndtime=int(S.current_position() /1000)

    s = "gps:"+str(t)+","+str(sndtime)+','+str(tm)+","+str(tot)+"," +str(used)+","+str(lat)+","+str(lng)+ "," + str(alt)
    s = s +"," + str(vdop) + "," + str(hdop) + "," + str(hdg) + "," + str(hdgacc) + "," + str(spd) + "gsm:"+str(sloc)+","+str(sdb)
    fncSavedata(s)
    
    pic=camera.take_photo('RGB',(320,240),0,'none','auto','auto',1)
    sp="e:\\datalogger\\pic" + str(t) + '.jpg'
    pic.save(sp)
    
    
    img.clear()
    img.text((40,34),u'Log ID: ' + str(counter),0xff0000,font='normal')
    img.text((40,64),u'Sats: ' + str(used) + "/" + str(tot) ,0xff0000,font='normal')
    img.text((40,94),u'Spd: ' +  str(int(spd)),0xff0000,font='normal')
    img.text((40,124),u'Snd: ' +  str(sndtime),0xff0000,font='normal')
    handle_redraw(())


canvas = appuifw.Canvas(event_callback = None)
appuifw.app.body = canvas
appuifw.app.title = u"Data logger"
w,h = canvas.size
img=graphics.Image.new((w,h))

startrecording()

positioning.set_requestors([{"type":"service","format":"application","data":"test_app"}])
positioning.select_module(270526860)
positioning.position(course=1,satellites=1,callback=cb,interval=1000000,partial=1)

app_lock = e32.Ao_lock()
app_lock.wait()

stoprecording()
