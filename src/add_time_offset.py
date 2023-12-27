import re
import argparse
import datetime
from csv_to_tsv import csv_to_tsv

parser = argparse.ArgumentParser(description='Add DateTime offset to a file.')

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('filename')
parser.add_argument('-h', '--hours', type=int, nargs=1, default=[0])
parser.add_argument('-m', '--minutes', type=int, nargs=1, default=[0])
parser.add_argument('-s', '--seconds', type=int, nargs=1, default=[0])
parser.add_argument('--sub', action='store_true')

args = parser.parse_args()

if '.csv' in args.filename:
    csv_to_tsv(args.filename)

filename_without_extension = args.filename.split('.')[0]
f_in = open(f'{filename_without_extension}.tsv', "r")
f_out = open(f'{filename_without_extension}_with_offset.tsv', "a")

offset = datetime.timedelta(hours=args.hours[0], minutes=args.minutes[0], seconds=args.seconds[0])

sign = -1 if args.sub else 1

col_with_timestamp = 1

for line in f_in:
    line = re.split('\t', line)
    
    if not line[0].isdigit():
        for idx, col in enumerate(line):
            if col.lower() == 'time':
                col_with_timestamp = idx
        continue

    if '.' in line[col_with_timestamp]:
        time = datetime.datetime.strptime(line[col_with_timestamp],"%H%M%S.%f")
    else:
        time = datetime.datetime.strptime(line[col_with_timestamp],"%H%M%S")
    newTime = time + (offset * sign)
    line[col_with_timestamp] = newTime.strftime("%H%M%S.%f")[:10]
    line = '\t'.join(line)
    f_out.write(line)

f_in.close()
f_out.close()
