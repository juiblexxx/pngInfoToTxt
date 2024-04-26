# coding: utf-8
# pngファイルのメタデータからプロンプト情報等を文字列で返す

# モジュールをインポート
import sys
import traceback

import PySimpleGUI as sg
# import flet as ft

from sd_png import sd_png_def as spgd


def window():
    filespaths = sg.popup_get_file(spgd.SG_STR_FILESELECT_02, title=spgd.SG_TTL_FILESELECT_02, multiple_files=True)
    outfile = spgd.PNGINFO_FILE

    try:
        files = filespaths.split(";")
        with open(outfile, "w") as f:
            for file in files:
                prompt_text = spgd.get_png_metatext(file)
                f.write(prompt_text)

    except Exception as e:
        exec_type, exec_value, exec_traceback = sys.exc_info()
        exec_message = traceback.format_exception_only(exec_type, exec_value)[-1]
        sg.popup(f"{spgd.SG_EXCEPT_ETC}:{file}->{exec_type.__name__}\n\n{exec_message}")
