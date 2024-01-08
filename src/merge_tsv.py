import argparse
import re

from csv_to_tsv import csv_to_tsv

def closeFiles(files):
    for f in files:
        f.close()

def parseTimestamp(timestamp):
    if 'T' in timestamp:
        timestamp = re.split('T|\.', timestamp)[1]
    return int(timestamp.replace(':', ''))

def hasLine(lines, count):
    return count < len(lines)

parser = argparse.ArgumentParser(description='Script for merging .tsv files.')

parser.add_argument('file1', type=str, nargs=1)
parser.add_argument('other', type=str, nargs='+')
    
args = parser.parse_args()

# Convert input files from .csv -> .tsv if applicable
files = args.file1 + args.other
for i, f in enumerate(files):
    if '.csv' in f:
        csv_to_tsv(f)
    files[i] = open(f"{f.replace('.csv', '.tsv')}", "r")

# Extract header row information
headers = [f.readline().upper().strip() for f in files]
columns = [h.split('\t') for h in headers]
time_idxs = [c.index('TIME') for c in columns]
lane_idxs = [c.index('LANE') for c in columns]

# Extract data rows
f_data = [f.readlines() for f in files]

# EOF counters
eof_c = [0] * len(files)

# Output file
filename_without_extension = args.file1[0].split('.')[0]
out_f = open(f"{filename_without_extension}_merged.tsv", "a")
out_h = '\t\t'.join(headers)
out_f.write(f"{out_h}\n")

f_hasLine = [hasLine(f_data, eof_c) for f_data, eof_c in zip(f_data, eof_c)]
while (True in f_hasLine):
    timestamps = [float('inf')] * len(files)
    lanes = [float('inf')] * len(files)

    # Extract timestamp and lane number of current row
    for i in range(len(files)):
        if f_hasLine[i]:
            cols = re.split(r'\t+', f_data[i][eof_c[i]])
            timestamps[i] = parseTimestamp(cols[time_idxs[i]])
            lanes[i] = int(cols[lane_idxs[i]])

    # Calculate minimum timestamp, lane number
    minTime, minLane = min(zip(timestamps, lanes))
    
    # Write row to output file
    res = ''
    for i in range(len(files)):
        if (f_hasLine[i] and
            timestamps[i] - minTime <= 1 and
            lanes[i] == minLane):
            res += f_data[i][eof_c[i]].strip() + '\t\t'
            eof_c[i] += 1
        elif i < len(files):
            res += (len(columns[i]) + 1) * '\t'
    out_f.write(res + '\n')

    f_hasLine = [hasLine(f_data, eof_c) for f_data, eof_c in zip(f_data, eof_c)]

files.append(out_f)
closeFiles(files)
