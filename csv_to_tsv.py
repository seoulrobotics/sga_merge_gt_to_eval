in_f = open("result_with_offset_lane2.csv", "r")
out_f = open("result_with_offset_lane2.tsv", "a")

for line in in_f:
    out_f.write(line.replace(',', '\t'))

in_f.close()
out_f.close()
