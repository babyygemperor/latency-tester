import datetime
import os
from time import sleep

from ping3 import ping

# SET YOUR PING RESPONSE TIME THRESHOLD HERE, IN SECONDS
THRESHOLD = 500  # 500 milliseconds is my tolerance

# SET YOUR PING INTERVAL HERE, IN SECONDS
INTERVAL = 1

# WHO SHOULD WE RUN THE PING TEST AGAINST
DESTINATION = "www.google.com"

# LOG TO WRITE TO WHEN PINGS TAKE LONGER THAN THE THRESHOLD SET ABOVE
i = datetime.datetime.now()
log_file = "logs/internet.log"


def write_to_file(file_to_write, message):
    os.makedirs(os.path.dirname(file_to_write), exist_ok=True)
    fh = open(file_to_write, "a")
    fh.write(message + "\n")
    fh.close()


count = 0
date_time = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
line = "--------------------------------------------"
header = f"{line}\nStarting logging\t{date_time}\n{line}"

print(header)
write_to_file(log_file, header)

while True:
    count += 1
    latency = ping(DESTINATION)

    if latency is not None:
        latency = round(ping(DESTINATION) * 1000, 3)
        if latency < THRESHOLD:
            INTERVAL = 1
            write_log = "No"
        else:
            INTERVAL = 2
            write_log = "Yes"
        latency_text = f"{latency}ms"
    else:
        INTERVAL = 5
        write_log = "Yes"
        latency_text = "PACKET DROPPED"

    # Use better text is packet is dropped

    line = f"{datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}:\tlatency: {latency_text}"
    print(f"{line}; logging: {write_log}")

    if write_log == "Yes":
        write_to_file(log_file, line)
    sleep(INTERVAL)
