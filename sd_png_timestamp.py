# coding: utf-8
# カレントフォルダの全PNGファイルに対して、
# ファイル名にある文字列をタイムスタンプとして、
# ファイルのタイムスタンプ（作成・更新日時）を書き換える

# モジュールをインポート
import sys
import os
import traceback
import datetime
import PySimpleGUI as sg

# from sd_png import sd_png_def as spgd

def edit_file_timestamp(source_path: str,delimiter: str, date_position: int = 0):
    """
    ファイルのタイムスタンプをファイル名で書き換えます
    YYYYMMDDHHIISS形式に対応
    Args:
        source_path: ファイルのフルパス文字列
        delimiter: 区切り文字
        date_position:
            delimiterで区切った時に前方から何番目にタイムスタンプ文字列があるか
            先頭の要素はゼロとする
    """
    file_name = os.path.basename(source_path)
    file_name_split = str.split(file_name, delimiter)
    file_timestamp = file_name_split[date_position]
    datetime_object = datetime.datetime.strptime(file_timestamp, '%Y%m%d%H%M%S')
    # t = os.path.getatime(file)
    # dt = datetime.datetime.fromtimestamp(t)
    # dt = datetime.datetime.now()
    # new_dt = dt + timedelta + timedelta2
    # new_timestamp = new_dt.timestamp()
    # ファイルのアクセス日時と更新日時をどちらも変更
    os.utime(source_path, (datetime_object.timestamp(), datetime_object.timestamp()))


def window(source_filepaths):
    try:
        # files = source_filepaths.split(";")
        num = 0
        for file in source_filepaths:
            edit_file_timestamp(file, "-", 1)
            num = num + 1

    except Exception as e:
        exec_type, exec_value, exec_traceback = sys.exc_info()
        exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
        sg.popup(f"例外が発生しました:{exec_type.__name__}\n\n{exec_message}")



current_path = os.path.dirname(__file__)
files = []

print(current_path)

# ファイルを取得
for file in os.listdir(current_path):
    file_path = os.path.join(current_path, file)
    # print(file_path)
    # print(str(os.path.splitext(file_path)[1]).lower())
    # ファイルかつ拡張子.pngなら処理対象にする
    if os.path.isfile(file_path) and str(os.path.splitext(file_path)[1]).lower() == ".png":  #isdirの代わりにisfileを使う
        files.append(file_path)
        # print(file_path)

window(files)
