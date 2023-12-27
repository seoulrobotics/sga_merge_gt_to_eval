import re
import sys
import datetime

filename, h, m, s, sign = sys.argv

f_in = open(filename, "r")
f_out = open(f"result_with_offset.tsv", "a")

offset = datetime.timedelta(hours=h, minutes=m, seconds=s)

# Skip header line
f_in.readline()

sign = -1 if sign == '-' else 1

for line in f_in:
    line = re.split('\t', line)
    if '.' in line[1]:
        time = datetime.datetime.strptime(line[1],"%H%M%S.%f")
    else:
        time = datetime.datetime.strptime(line[1],"%H%M%S")
    newTime = time + (offset * sign)
    line[1] = newTime.strftime("%H%M%S.%f")[:10]
    line = '\t'.join(line)
    f_out.write(line)

f_in.close()
f_out.close()
