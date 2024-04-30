# coding: utf-8
# ファイル名にある文字列をタイムスタンプとして、
# ファイルのタイムスタンプ（作成・更新日時）を書き換える

# モジュールをインポート
import sys
import traceback
import PySimpleGUI as sg

from sd_png import sd_png_def as spgd


def window():
    try:
        filespaths = sg.popup_get_file(spgd.SG_STR_FILESELECT_02, title=spgd.SG_TTL_FILESELECT_02, multiple_files=True)
        files = filespaths.split(";")
        num = 0
        for file in files:
            spgd.edit_file_timestamp(file, "-", 1)
            num = num + 1

    except Exception as e:
        exec_type, exec_value, exec_traceback = sys.exc_info()
        exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
        sg.popup(f"{spgd.SG_EXCEPT_ETC}:{exec_type.__name__}\n\n{exec_message}")
