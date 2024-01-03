import argparse

parser = argparse.ArgumentParser(description='Script for splitting .tsv files by lane number.')

parser.add_argument('filename')
    
args = parser.parse_args()

# filename_without_extension = args.filename.split('.')[0]
f_in = open(f'{args.filename}', "r")
f_lane1 = open(f'output_files/sg_lane1.tsv', "w+")
f_lane2 = open(f'output_files/sg_lane2.tsv', "w+")

headers = f_in.readline().strip()
LANE_IDX = headers.split('\t').index('LANE')

f_lane1.seek(0)
f_lane2.seek(0)

f_lane1.write(headers + '\n')
f_lane2.write(headers + '\n')

lines = f_in.readlines()

for line in lines:
    lane = line.split('\t')[LANE_IDX]
    if lane == '1':
        f_lane1.write(line)
    elif lane == '2':
        f_lane2.write(line)
        
f_lane1.truncate()
f_lane2.truncate()

f_lane1.close()
f_lane2.close()
f_in.close()
