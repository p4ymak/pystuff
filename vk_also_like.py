# -*- coding: utf-8 -*-
import sys, os, json, operator
reload(sys) 
sys.setdefaultencoding('utf-8')
"""
Created on Sat Jan 21 15:32:42 2017

@author: p4ymak
"""
from urllib2 import Request, urlopen, URLError
from collections import Counter
dirname=os.path.dirname(os.path.realpath(sys.argv[0]))

os.system('clear')
print("")
print("----    <<Vk Also Like>> by Roman Chumak (www.p43d.com)..    ----")
print("")
print("Enter public name:")
groupid = raw_input("vk.com/")

pubmems = []
memcount = 0
groupcount = 0
repeat = 0
offset = 0
allgroups = []
num = 0

method = "groups.getMembers"

vkapi = str("https://api.vk.com/method/"+method+"?gid="+groupid)

request = Request(vkapi)

response = urlopen(request)
vkread = json.loads(response.read())
pubcount = vkread["response"]["count"]

repeat = int(pubcount/1000)

def getMembers(groupid, offset):
    vk = str("https://api.vk.com/method/groups.getMembers?gid="+groupid+"&count=1000&offset="+str(offset))
    reqvk = Request(vk)
    respvk = urlopen(reqvk)
    vkread = json.loads(respvk.read())
    mems = vkread["response"]["users"]
    for mem in mems:
        pubmems.append(mem)


for r in range(repeat+1):
    offset = r*1000
    getMembers(groupid, offset)

print(" ")
print("----Scanning members----")


def usersubs(mem):
    vkapiuser = str("https://api.vk.com/method/users.getSubscriptions?uid="+str(mem))

    requser = Request(vkapiuser)
    responuser = urlopen(requser)
    userread = json.loads(responuser.read())

    memgroups = userread["response"]["groups"]["items"]
    return(memgroups)

def ginfo(gid):
    vkapi = str("https://api.vk.com/method/groups.getById?gid="+str(gid))
    request = Request(vkapi)

    response = urlopen(request)
    vkread = json.loads(response.read())
    ginfo_name = vkread["response"][0]["name"]
    ginfo_site = vkread["response"][0]["screen_name"]
    
    output = str(ginfo_name) + " | " + "vk.com/" + str(ginfo_site)    
    return(output)
   

for mem in pubmems:
    memcount += 1
    print(str(memcount) + "/" + str(pubcount))
    for group in usersubs(mem):
        allgroups.append(group)

print("")
print("")
print("")
print("")


filename = str(str(dirname) + "/vk_also_liked/" + str(groupid) + ".txt")
filedir = os.path.dirname(filename)
if not os.path.exists(os.path.dirname(filename)):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as exc:
        raise
    
outfile = file(filename,'w')


print("------ TOP 100 -----")

allgroupsrated = dict(Counter(allgroups))

allgroupstop = sorted(allgroupsrated.items(), key=operator.itemgetter(1))
allgroupstop.reverse()


for i in range (1,101):
    gid = allgroupstop[i][0]
    gcount = allgroupstop[i][1]
    
    outfile.write(str(i)+ ": " + str(gcount) + " | " + ginfo(gid) + "\n")
    print(str(i)+ ": " + str(gcount) + " | " + ginfo(gid))

print("")
print("")
print("")
print("")
outfile.write("Total members: " + str(pubcount))
outfile.close()
sys.exit()