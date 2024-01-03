import re
import argparse

from datetime import datetime
from datetime import timedelta

from csv_to_tsv import csv_to_tsv

def close_files_and_exit(f_in, f_out):
    f_in.close()
    f_out.close()
    exit()

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

offset = timedelta(hours=args.hours[0], minutes=args.minutes[0], seconds=args.seconds[0])

sign = -1 if args.sub else 1

# Find column containing timestamps
f_headers = f_in.readline()
f_out.write(f_headers)
f_headers = re.split('\t', f_headers)

col_with_timestamp = -1
if not f_headers[0].isdigit():
    for idx, col in enumerate(f_headers):
        if col.lower() == 'time':
            col_with_timestamp = idx
    if col_with_timestamp == -1:
        print("Cannot parse file: 'time' header missing.")
        close_files_and_exit(f_in, f_out)
else:
    print("Cannot parse file: header row missing.")
    close_files_and_exit(f_in, f_out)

# Parse timestamps
for line in f_in.readlines():
    line = re.split('\t', line)

    timestamp = line[col_with_timestamp]
    if '.' in timestamp:
        timestamp = re.split('\.', timestamp)[0]
    
    timestamp = datetime.strptime(timestamp, "%H%M%S")
    newTime = timestamp + (offset * sign)
    line[col_with_timestamp] = newTime.strftime("%H:%M:%S")
    line = '\t'.join(line)
    f_out.write(line)

close_files_and_exit(f_in, f_out)
