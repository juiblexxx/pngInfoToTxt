# coding: utf-8
# 選択されたpng画像ファイルのpnginfoにもとづきファイルをフォルダ分けします
# 基準ファイルを選択すると、そのファイルが存在するフォルダ階層のファイル群を処理します

# モジュールをインポート
import sys
import traceback
import os
import shutil
import PySimpleGUI as sg

from sd_png import sd_png_def as spgd


def window():
    # ウィンドウに配置する要素を定義
    layout = [
        [sg.Checkbox(spgd.SG_STR_CHECKBOX_02, key=spgd.SG_KEY_CHECKBOX_02, default=False)],
        [sg.Text(spgd.SG_STR_FILESELECT_01)],
        [sg.Button(spgd.SG_STR_EXECUTE_01, key=spgd.SG_KEY_EXECUTE_01), sg.Button(spgd.SG_STR_CANCEL_01, key=spgd.SG_KEY_CANCEL_01)],
    ]

    # ウィンドウを作成
    window = sg.Window(spgd.SG_WIN_02, layout)

    # イベントループ
    while True:
        event, values = window.read()    # イベントと入力値を取得

        if event == sg.WIN_CLOSED:  # ウィンドウが閉じられたら
            break   # ループ終了

        elif event == spgd.SG_KEY_CANCEL_01:  # キャンセルボタン
            break

        elif event == spgd.SG_KEY_EXECUTE_01:   # 実行ボタン
            date_dir_name = values[spgd.SG_KEY_CHECKBOX_02]
            base_file = sg.popup_get_file(spgd.SG_STR_FILESELECT_01, title=spgd.SG_TTL_FILESELECT_01, multiple_files=False)  # 基準となるファイルを取得

            if base_file == None:
                sg.popup(spgd.SG_EXCEPT_NOFILE)  # ファイル指定は必須
                break

            try:
                if os.path.isfile(base_file):
                    base_extention = os.path.splitext(base_file)[1]  # ドットを含む拡張子を取得
                    parent_path = os.path.dirname(base_file)    # 振分先ディレクトリパスを作成する為の親パスとして取得しておく
                    files = [os.path.join(parent_path, file_name) for file_name in os.listdir(parent_path) if os.path.isfile(os.path.join(parent_path, file_name))]  # ディレクトリ配下からファイルのみを取得

                    for file in files:
                        # ファイルの移動（基準ファイルと拡張子が同一なら）
                        # file = file.replace('/', os.sep)
                        file_extention = os.path.splitext(file)[1]

                        if file_extention == base_extention:
                            model_name = spgd.get_png_model_name(file)  # 読み込んだファイルからモデル名を取得
                            if date_dir_name == True:
                                # YYYYmmdd_ をプレフィックスに付加
                                model_name = f"{spgd.get_file_timestamp(file, 1)}_{model_name}"
                            model_dir = os.path.join(parent_path, model_name)   # 振分先ディレクトリ名を作成
                            # model_dir = model_dir.replace('/', os.sep)
                            os.makedirs(model_dir, exist_ok=True) if not os.path.isdir(model_dir) else None  # ディレクトリがなければ作成
                            shutil.move(file, model_dir)    # 作成したディレクトリにファイルを移動
                    break   # ループ終了

            except Exception as e:
                exec_type, exec_value, exec_traceback = sys.exc_info()
                exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
                sg.popup(f"{spgd.SG_EXCEPT_ETC}:{exec_type.__name__}\n\n{exec_message}")
                break

    window.close()


