

* ダウンロード

getlogs.py

* 導線／合計数

cat 20120730152805_payment_track_result/summary.csv | ./tsv2csv.py | ./filter_columns.py | ./filter_rows.py -l safe_rows_normal.json | ./sum.py
cat 20120730152805_payment_track_result/summary.csv | ./tsv2csv.py | ./filter_columns.py | ./filter_rows.py -l safe_rows_premium.json | ./sum.py

* 行列変換

cat 20120802_userhistory_ja.csv | ./swap_rowcolumn.py 


以上
