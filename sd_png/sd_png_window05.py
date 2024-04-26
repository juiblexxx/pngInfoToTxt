# coding: utf-8
# 指定したLoRA/Lyco名のblock weight指定をファイル名に追加します
# 既にファイル名に追加されていたらスキップしたい

# モジュールをインポート
import sys
import traceback
import os
import re
import PySimpleGUI as sg

from sd_png import sd_png_def as spgd


# ファイルのリネーム処理
def rename_file(old_name:str, new_name: str) :
    try :
        os.rename(old_name, new_name)
    except:
        sg.popup(f"既に同名のファイルがあるのでスキップします\n{old_name}\n{new_name}")


def window():
    # ウィンドウに配置する要素を定義
    input_history = spgd.load_history()

    # sg_key_input01 = "-INPUT-"
    # sg_key_checkbox01 = "-CHECKBOX-"
    # sg_key_history01 = "-HISTORY-"
    # sg_key_button01 = "-EXECUTE-"
    # sg_key_button02 = "-CANCEL-"

    layout = [
        [sg.Text(spgd.SG_STR_INPUT_01), sg.Input(key=spgd.SG_KEY_INPUT_01, enable_events=True)],
        [sg.Text(spgd.SG_STR_HISTORY_01), sg.Combo(key=spgd.SG_KEY_HISTORY_01, size=(30, 1), enable_events=True, values=input_history)],
        [sg.Text(spgd.SG_STR_FILESELECT_01)],
        [sg.Button(spgd.SG_STR_EXECUTE_01, key=spgd.SG_KEY_EXECUTE_01), sg.Button(spgd.SG_STR_CANCEL_01, key=spgd.SG_KEY_CANCEL_01)],
    ]

    # ウィンドウを作成
    window = sg.Window(spgd.SG_WIN_05, layout)

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

            if lora_name == "":
                sg.popup(spgd.SG_EXCEPT_NOLORA)  # Lora名称指定は必須
                break

            # 入力履歴に追加
            if lora_name not in input_history:
                input_history.append(lora_name)
                spgd.save_history(input_history)

            try:
                base_file = sg.popup_get_file(spgd.SG_STR_FILESELECT_01, title=spgd.SG_TTL_FILESELECT_01, multiple_files=False)  # 基準となるファイルを取得

                if os.path.isfile(base_file):
                    parent_path = os.path.dirname(base_file)  # 選択されたファイルからディレクトリパスを取得
                    files = [os.path.join(parent_path, file_name) for file_name in os.listdir(parent_path) if os.path.isfile(os.path.join(parent_path, file_name))]  # ディレクトリ配下からファイルのみを取得

                    for file in files:
                        new_file_head = spgd.get_png_lbw(file, lora_name)   # 読み込んだファイルから、lora_nameの層別情報の文字列を取得
                        if new_file_head == "":    # 戻り値が何もなければ次へ
                            pass
                        else:
                            # 情報は見つかったけど、既にファイルにセットされている文字列なら処理をスキップしたい
                            match = re.search(new_file_head, file)
                            if match is None :
                                # ファイルのリネーム
                                new_basename = f"{new_file_head}_{os.path.basename(file)}"
                                new_file_name = os.path.join(parent_path, new_basename)
                                rename_file(file, new_file_name)
                    break   # ループ終了

            except Exception as e:
                exec_type, exec_value, exec_traceback = sys.exc_info()
                exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
                sg.popup(f"{spgd.SG_EXCEPT_ETC}:{exec_type.__name__}\n\n{exec_message}")
                break

    window.close()

