import json
import requests, random 
import pyfiglet, concurrent.futures
from colorama import Fore as cl
def rando(length):
    limsta = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y x"
    sr = ""
    pp = limsta.split(" ")
    for i in range(int(length)):
        #print(i)
        
        sr += pp[random.randint(0,len(pp))-1]
    return sr
n = {
"green": cl.GREEN,
"red": cl.RED,
"blue": cl.BLUE,
"cyan": cl.CYAN,
"magenta": cl.MAGENTA,
"yellow": cl.YELLOW,
"white": cl.WHITE
}
varlist = {}
currvar = ""
dead = 0
live = 0
err = 0
reqlist = {}
def process(xp,xa,code,word,proy):
    global varlist, reqlist, dead, live, err, n
    dcx = xp["seperator"]
    laxa = xp["dataType"]
    if len(word.split(dcx)) == len(laxa.split(dcx)):
        a = word.split(dcx)
        b = laxa.split(dcx)
        for i in range(len(a)):
            varlist[b[i]] = a[i]
    else:
        err += 1
        print(f"{n[xp['ErrC'].lower()]}Live: {live} | dead: {dead} | Error: {err} | current : Error | Reason: Invalid Data")
        return
    session = requests.session()
    v = code.replace(xa,"").split("\n")
    #print(v)
    for line in v:
        if line == '':
            continue
        if line[:3] == "VAR":
            if len(line.split(" ")) > 3:
                name = line.split("VAR")[1].split("=")[0].replace(" ","")
                data = funct(line.split(f"VAR {name} = ")[1])
                #print(data)
                #print(f"VAR {name} =")
                
                varlist[name] = data
            else:
                print ("Undefined Syntax at Undefined")
                __import__("sys").exit()
        elif line[:3] == "REQ":
            try:
                url = line.split("`")[1]
                name = line.split(f"REQ `{url}` as ")[1]
                reqlist[name] = {}
                reqlist [name]["url"] = url
                reqlist [name]["headers"] = {}
                reqlist [name]["body"] = ""
                reqlist [name]["status"] = ""
                reqlist [name]["data"] = ""
            except Exception as e:
                print ("Undefined Syntax at Undefined",e)
                __import__("sys").exit()
        elif line[:2] == "-H":
            try:
                name = line.split(" ")[1]
                hname = line.split(f'"')[1]
                value = line.split("`")[1]
                reqlist[name]["headers"][hname] = funct(value,h="TRUE")
            except Exception as e:
                print ("Undefined Syntax at Undefined",e)
                __import__("sys").exit()
        elif line[:5] == "-body":
            try:
                name = line.split(" ")[1]
                value = line.split("`")[1]
                reqlist[name]["body"] = funct(value,h="TRUE")
            except Exception as e:
                print ("Undefined Syntax at Undefined",e)
                __import__("sys").exit()
        elif line[:2] == "-G":
            try:
                name = line.split(" ")[1]
                lista = reqlist[name]
                url = lista["url"]
                headers = lista["headers"]
                proxy = None
                if xp["Proxy"] == "True":
                    nga = proy.split("\n")
                    prox = nga[random.randint(0,len(nga))]
                    proxy = {http: prox,https: prox}
                data = session.get(url,headers=headers,proxies=proxy)
                reqlist [name]["status"] = data.status_code
                reqlist [name]["data"] = data.text
            except Exception as e:
                print ("Undefined Syntax at Undefined",e)
                __import__("sys").exit()
        elif line[:2] == "-P":
            try:
                name = line.split(" ")[1]
                lista = reqlist[name]
                url = lista["url"]
                headers = lista["headers"]
                body = lista["body"]
                proxy = None
                if xp["Proxy"] == "True":
                    nga = proy.split("\n")
                    prox = nga[random.randint(0,len(nga))]
                    proxy = {http: prox,https: prox}
                data = session.post(url,headers=headers,proxies=proxy,data=body)
                reqlist [name]["status"] = data.status_code
                reqlist [name]["data"] = data.text
            except Exception as e:
                print ("Undefined Syntax at Undefined",e)
                __import__("sys").exit()
        elif line[:8] == "KEYCHECK":
            try:
                np = line.split(" ")
                if len(np) >= 5:
                    name = funct("$'"+line.split("for")[1].split("$'")[1]+"$'")
                    #print("$'"+line.split("for")[1].split("$'")[1]+"$'")
                    #print(name)
                    erra = True
                    if "E_ALL" in np:
                        erra = True
                    
                    succ = json.loads(line.split("SUCC")[1].split("DEAD")[0])
                    
                    ded = json.loads(line.split("DEAD")[1].split("] ")[0]+"]")
                    #print(str(succ)+"\n"+str(ded))
                    for x in succ:
                        if x in name:
                            #print(x,".   ",name)
                            live += 1
                            print(f"{n[xp['HitC'].lower()]} Live: {live} | dead: {dead} | Error: {err} | current : Live")
                            with open("x-file-saves.txt","a") as file:
                                
                                
                                file.write("Data: ["+str(varlist)+"\n"+str(reqlist)+"]")
                            return
                    for x in ded:
                        if x in name or erra == True:
                            dead += 1
                            print(f"{n[xp['DeadC'].lower()]} Live: {live} | dead: {dead} | Error: {err} | current : Dead")
                            return
                    err += 1
                    print(f"{n[xp['ErrC'].lower()]} Live: {live} | dead: {dead} | Error: {err} | current : Error | Reason : No Keychain was found While checking")
                    return
                    #print(name)
                    
                else:
                    print("please recheck keychaning")
                    __import__("sys").exit()
            except Exception as e:
                print("Unknown Error:",e)
                __import__("sys").exit()
        
        
        
    
    
    
def funct(data,h="FALSE"):
    data = data
    global varlist, reqlist, currvar
    xp = data.split("$'")
    i = 1
    for code in xp:
        #print(i, i )
        #print(
        if i % 2 == 0:
            try:
                if code[:3].lower() == "req":
                    exec("varlist['xaxa'] = reqlist"+code.replace(code[:3],""))
                    
                    #print(code.replace(code[:3],""))
                    #print("xx"+currvar)
                    #print(akg())
                    data = data.replace(code,varlist["xaxa"])
                else:
                    exec("varlist['xaxa'] = varlist"+code.replace(code[:3],""))
                    
                    #print(code.replace(code[:3],""))
                    #print("xx"+currvar)
                    #print(akg())
                    data = data.replace(code,varlist["xaxa"])
            except Exception as e:
                print("Undefined Variable at Undefined ",e)
            
        i += 1
        data = data.replace("$'","")
    functable = data.split("@'f")
    k = 1
    for func in functable:
        if i % 2 == 0:
            try:
                iden = func.replace(" ",'')
                if iden[:6].lower() == "random":
                    if iden.replace(iden[:6],"")[:1] == "(":
                        reg1 = iden.split("(")[1].split(")")[0].split(",")
                        data = data.replace(func,str(random.randint(int(reg1[0]),int(reg1[1]))))
                    elif iden.replace(iden[:6],"")[:3].lower() == "str":
                        khe = rando(int(iden.split("str")[1]))
                        data = data.replace(func,khe)
                    else:
                        print("Undefined string")
                elif iden[:5] == "parse":
                    if len(iden.split("@'xfrom")) >= 2:
                        fro = iden.split("@'xfrom")
                        to = fro[1]
                        string = fro[0][5:]
                        #print(string)
                        delim = string.split("@',")
                        a1 = delim[0]
                        a2 = delim[1]
                        data = data.replace(func,varlist[to].split(a1)[1].split(a2)[0])
                    else:
                        print("Undefined Function String At Undefined Or Variable Error")
            except Exception as e:
                print("Undefined Function String At Undefined",e)
        data = data.replace("@'f","")
    return data
def run(code):
    
    global n
    xp = json.loads(code.split("[SETTINGS]")[1].split("[SCRIPT]")[0].replace("[\n","{\n").replace("\n]","\n}").replace("\n",""))
    #print(xp)
    color = n[xp["HitC"].lower()]
    print(color+pyfiglet.figlet_format(xp["Name"],"slant"))
    color = n[xp["MsgC"].lower()]
    print(color+xp["Version"]+" by "+xp["Author"])
    print("ProxyBased:",xp["Proxy"])
    #print("ProxyType:",xp["ProxyType"])
    proy = ""
    if xp["Proxy"] == "True":
        with open (input("ProxyList:"),"r") as file:
            proy = file.read()
    xa = "[SETTINGS]"+code.split("[SETTINGS]")[1].split("[SCRIPT]")[0]+"[SCRIPT]"
    #print(xa)
    wordlist = ""
    with open(input("Wordlist:\t"), "r") as file:
        wordlist = file.read()

    # Use ThreadPoolExecutor to process each line concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for line in wordlist.split("\n"):
            futures.append(executor.submit(process, xp, xa, code, line, proy))

        # Wait for all tasks to complete
        #concurrent.futures.wait(futures)
#This modification will execute the process .wait
