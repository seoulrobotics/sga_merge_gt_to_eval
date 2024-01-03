run:
	python3 csv_to_tsv.py sensys_gatso.csv 
	python3 add_time_offset.py sensys_gatso.tsv -h 2 -m 31 -s 6 --sub
	python3 merge_tsv.py sensys_gatso_with_offset_lane1.tsv gt_lane1.tsv radar_lane1.tsv 
	python3 merge_tsv.py sensys_gatso_with_offset_lane2.tsv gt_lane2.tsv radar_lane2.tsv 
