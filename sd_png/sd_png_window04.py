# coding: utf-8
# 選択されたpng画像ファイルのseed値にもとづきファイルをフォルダ分けします
# 基準ファイルを選択すると、そのファイルが存在するフォルダ階層のファイル群を処理します

# モジュールをインポート
import sys
import traceback
import os
import shutil
import PySimpleGUI as sg

from sd_png import sd_png_def as spgd


def window():
    try:
        base_file = sg.popup_get_file(spgd.SG_STR_FILESELECT_01, title=spgd.SG_TTL_FILESELECT_01, multiple_files=False)  # 基準となるファイルを取得

        if os.path.isfile(base_file):
            base_extention = os.path.splitext(base_file)[1]  # ドットを含む拡張子を取得
            parent_path = os.path.dirname(base_file)    # 振分先ディレクトリパスを作成する為の親パスとして取得しておく
            files = [os.path.join(parent_path, file_name) for file_name in os.listdir(parent_path) if os.path.isfile(os.path.join(parent_path, file_name))]  # ディレクトリ配下からファイルのみを取得

            for file in files:
                if os.path.splitext(file)[1] == base_extention: # 基準ファイルと拡張子が同一なら実施
                    model_name = spgd.get_png_seed(file)  # 読み込んだファイルから振分先ディレクトリ名を取得
                    model_dir = os.path.join(parent_path, model_name)
                    os.makedirs(model_dir, exist_ok=True) if not os.path.isdir(model_dir) else None  # ディレクトリがなければ作成
                    shutil.move(file, model_dir)    # 作成したディレクトリにファイルを移動

    except Exception as e:
        exec_type, exec_value, exec_traceback = sys.exc_info()
        exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
        sg.popup(f"{spgd.SG_EXCEPT_ETC}:{exec_type.__name__}\n\n{exec_message}")
