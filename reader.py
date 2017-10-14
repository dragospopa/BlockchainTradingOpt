import time

count = 0
while (True):
    print("Running script in daemon mode")
    file = open("js/sb-admin-charts.min.js","r") 
    data = file.read()

    target = open("sentiment.js", "w")
    
    target.write("Hello World!\n")
    target.write(str(count))
    count = count + 1
    target.write(data)
    target.close()
    time.sleep(5)
