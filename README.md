# VoTTで出力したCSVからYOLO形式に変換

## versions
```
pandas==1.4.1

Pillow==9.0.1
```
## 実行方法
1. ターゲット接続下(vott-csv-exportがある場所)に移動

2. git cloneで変換コードを取得
```
git clone https://github.com/bekku/convert_to_yolo_format_from_csv.git
```

3. [~export.csv]を出力されたcsvのpathに書き換えて実行. []は不要。
```
python convert_to_yolo_format_from_csv/convert_to_yolo.py [~export.csv]
```
4. ターゲット接続下に、imagesとlabelsを含むdatasetが作成される

