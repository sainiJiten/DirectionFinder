from GPSlocations import LatLong
from Directions import guide
#from VoiceReco import Destination
import re
import time

def update_loc(direc,i):
    sl = [0.0,0.0]
    el = [0.0,0.0]
    sl[0] = float(direc[0]["legs"][0]["steps"][i]["start_location"]["lat"])
    sl[1] = float(direc[0]["legs"][0]["steps"][i]["start_location"]["lng"])
    el[0] = float(direc[0]["legs"][0]["steps"][i]["end_location"]["lat"])
    el[1] = float(direc[0]["legs"][0]["steps"][i]["start_location"]["lng"])
    return sl,el

def string2coord(s):
    sl = [0.0,0.0]
    l = s.split(",")
    sl[0] = float(l[0])
    sl[1] = float(l[1])
    return sl
    


instructions = []
clean = re.compile('<.*?>')
i = 0
guardian = LatLong()
guardian.connect()

org = guardian.values()
#print("Please mention your destination:")
#dst = Destination()
dst = "CN Tower"

direc = guide(org,dst)
#print("Finding path...................")
print("Total distance to be covered: ",direc[0]["legs"][0]["distance"]["text"])
print("Total time to cover the distance: ",direc[0]["legs"][0]["duration"]["text"])

j = 0
while(True):
    ins = direc[0]["legs"][0]["steps"][j]["html_instructions"]
    ins_clean = re.sub(clean, '', ins)
    if(ins_clean.find("Destination")>0):
        instructions.append(ins_clean[0:ins_clean.find("Destination")])
        instructions.append(ins_clean[ins_clean.find("Destination"):])
        break
    else:
        instructions.append(ins_clean)
    j += 1


print(instructions[0])
sl,el = update_loc(direc,i)

while i<(j+1):
    dist = guardian.distance(sl,el)
    print(dist*1000,"mts.")
    if dist < 0.010:
        i += 1
        sl,el = update_loc(direc,i)
        print(instructions[i])
    else:
        s_loc = guardian.values()
        sl = string2coord(s_loc) 
    time.sleep(2)


print(instructions[-1])
guardian.disconnect()
