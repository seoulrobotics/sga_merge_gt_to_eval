import argparse

def csv_to_tsv(filename):

    in_f = open(f"{filename}", "r")
    out_f = open(f"{filename.replace('.csv', '.tsv')}", "a")

    for line in in_f:
        out_f.write(line.replace(',', '\t'))

    in_f.close()
    out_f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert .csv format to .tsv format.')

    parser.add_argument('filename')

    args = parser.parse_args()
    
    csv_to_tsv(args.filename)
