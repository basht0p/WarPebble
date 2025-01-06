import time

def write(message):
    local_time = time.localtime()
    
    hours = str(local_time[3])
    minutes = str(local_time[4])
    seconds = str(local_time[5])
    
    if local_time[3] < 10: hours = "0" + hours
    if local_time[4] < 10: minutes = "0" + minutes
    if local_time[5] < 10: seconds = "0" + seconds
    
    time_stamp = hours + ":" + minutes + ":" + seconds
    log_line = " [" + time_stamp + "] : " + message
    print(log_line)