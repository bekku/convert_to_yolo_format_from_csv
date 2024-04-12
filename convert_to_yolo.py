import pandas as pd
import os
import shutil
from PIL import Image
from collections import defaultdict


def create_and_clean_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def convert_to_yolo_format(csv_file_path, base_dir):
    dataset_dir = os.path.join(base_dir, 'datasets')
    labels_dir = os.path.join(dataset_dir, 'labels')
    images_dir = os.path.join(dataset_dir, 'images')

    # datasets, labels, imagesディレクトリを作成または再作成
    create_and_clean_dir(labels_dir)
    create_and_clean_dir(images_dir)

    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    # 画像ごとにデータを格納するための辞書
    annotations = defaultdict(list)

    # 各行について処理を行う
    for index, row in df.iterrows():
        image_path = row['image']
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                width, height = img.size

                # バウンディングボックスの中心と幅・高さを計算
                xmin = row['xmin']
                ymin = row['ymin']
                xmax = row['xmax']
                ymax = row['ymax']

                x_center = ((xmin + xmax) / 2) / width
                y_center = ((ymin + ymax) / 2) / height
                bbox_width = (xmax - xmin) / width
                bbox_height = (ymax - ymin) / height

                # YOLO形式で文字列を生成
                yolo_format = f"0 {x_center} {y_center} {bbox_width} {bbox_height}"

                # 画像名に基づいて辞書に追加
                annotations[image_path].append(yolo_format)

    # ファイルをlabelsディレクトリに保存し、画像をimagesディレクトリにコピー
    for image_path, bbox_list in annotations.items():
        txt_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}.txt"
        label_path = os.path.join(labels_dir, txt_filename)
        with open(label_path, 'w') as file:
            file.write('\n'.join(bbox_list))
        # 画像をimagesディレクトリにコピー
        shutil.copy(image_path, images_dir)


if __name__ == "__main__":
    import sys
    csv_file_path = sys.argv[1]  # コマンドラインからCSVファイルパスを取得
    base_dir = os.path.dirname(csv_file_path)  # CSVファイルのあるディレクトリを基本ディレクトリとする
    convert_to_yolo_format(csv_file_path, base_dir)
