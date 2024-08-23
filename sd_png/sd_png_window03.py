# coding: utf-8
# 選択されたpng画像ファイルのpnginfoにもとづきファイルをフォルダ分けします
# 指定されたLora名称を使用しているファイルのみフォルダ分け対象になります。
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
    input_history = spgd.load_history()

    layout = [
        [sg.Text(spgd.SG_STR_INPUT_01), sg.Input(key=spgd.SG_KEY_INPUT_01, enable_events=True)],
        [sg.Checkbox(spgd.SG_STR_CHECKBOX_03, key=spgd.SG_KEY_CHECKBOX_03, default=False)],
        [sg.Text(spgd.SG_STR_HISTORY_01), sg.Combo(key=spgd.SG_KEY_HISTORY_01, size=(30, 1), enable_events=True, values=input_history)],
        [sg.Checkbox(spgd.SG_STR_CHECKBOX_01, key=spgd.SG_KEY_CHECKBOX_01, default=True)],
        [sg.Text(spgd.SG_STR_FILESELECT_01)],
        [sg.Button(spgd.SG_STR_EXECUTE_01, key=spgd.SG_KEY_EXECUTE_01), sg.Button(spgd.SG_STR_CANCEL_01, key=spgd.SG_KEY_CANCEL_01)],
    ]

    # ウィンドウを作成
    window = sg.Window(spgd.SG_WIN_03, layout)

    # イベントループ
    while True:
        event, values = window.read()    # イベントと入力値を取得

        if event == sg.WIN_CLOSED:  # ウィンドウが閉じられたら
            break   # ループ終了

        elif event == spgd.SG_KEY_CANCEL_01:  # キャンセルボタン
            break

        elif event == spgd.SG_KEY_HISTORY_01: # 履歴選択
            selected_text = values[spgd.SG_KEY_HISTORY_01]
            window[spgd.SG_KEY_INPUT_01].update(selected_text)

        elif event == spgd.SG_KEY_EXECUTE_01:   # 実行ボタン
            # 入力値の取得
            lora_name = values[spgd.SG_KEY_INPUT_01]
            additional_dir_name = values[spgd.SG_KEY_CHECKBOX_01]
            history_loop = values[spgd.SG_KEY_CHECKBOX_03]

            if history_loop == False :  # history使用なしなら
                if lora_name == "":
                    sg.popup(spgd.SG_EXCEPT_NOLORA)  # Lora名称指定は必須
                    break

                # 入力履歴に追加
                if lora_name not in input_history:
                    input_history.append(lora_name)
                    spgd.save_history(input_history)

            base_file = sg.popup_get_file(spgd.SG_STR_FILESELECT_01, title=spgd.SG_TTL_FILESELECT_01, multiple_files=False)  # 基準となるファイルを取得

            try:
                if os.path.isfile(base_file):
                    # 振分先ディレクトリパスを作成する為の親パスとして取得しておく
                    parent_path = os.path.dirname(base_file)

                    lora_list = []
                    if history_loop == False:
                        lora_list.append(lora_name)
                    else:
                        lora_list = input_history

                    for check_lora in lora_list:
                        files = [os.path.join(parent_path, file_name) for file_name in os.listdir(parent_path) if os.path.isfile(os.path.join(parent_path, file_name))]  # ディレクトリを取得してしまわないようisfileでファイルリストを取取得

                        for file in files:
                            # check_loraにもとづき読み込んだファイルから振分先ディレクトリ名を取得
                            model_name = spgd.get_png_input_lora_name(file, check_lora, additional_dir_name)
                            if model_name == "":    # Loraが見つからないファイルだったので次のファイルチェックへ
                                pass
                            else:
                                # YYYYmmdd_ をプレフィックスに付加したディレクトリを作成してファイルを移動する(やめた)
                                # model_name = f"{spgd.get_file_timestamp(file, 1)}_{model_name}"
                                model_dir = os.path.join(parent_path, model_name)
                                if not os.path.isdir(model_dir):
                                    os.makedirs(model_dir, exist_ok=True)
                                shutil.move(file, model_dir)
                    break   # ループ終了

            except Exception as e:
                exec_type, exec_value, exec_traceback = sys.exc_info()
                exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
                sg.popup(f"{spgd.SG_EXCEPT_ETC}:{exec_type.__name__}\n\n{exec_message}")
                break

    window.close()
