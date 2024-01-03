run:
	python3 add_time_offset.py sensys_gatso.csv -h 2 -m 31 -s 6 --sub
	python3 merge_tsv.py sensys_gatso_with_offset.tsv gt_data/gt_lane1.tsv ra_data/radar_lane1.tsv
	python3 merge_tsv.py sensys_gatso_with_offset.tsv gt_data/gt_lane2.tsv ra_data/radar_lane2.tsv
