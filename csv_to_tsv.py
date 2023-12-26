in_f = open("output2.csv", "r")
out_f = open("output2.tsv", "a")

for line in in_f:
    out_f.write(line.replace(',', '\t'))

in_f.close()
out_f.close()
