import re
import datetime

f_in = open("output2.tsv", "r")
f_out = open("new_output2.tsv", "a")

offset = datetime.timedelta(hours=2, minutes=19, seconds=14)

for line in f_in:
    line = re.split('\t', line)
    if '.' in line[1]:
        time = datetime.datetime.strptime(line[1],"%H%M%S.%f")
    else:
        time = datetime.datetime.strptime(line[1],"%H%M%S")
    newTime = time + offset
    line[1] = newTime.strftime("%H%M%S.%f")[:10]
    line = '\t'.join(line)
    f_out.write(line)

f_in.close()
f_out.close()
