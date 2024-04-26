# coding: utf-8
# automatic1111から出力されたpngファイルに対して色々な処理をします

# モジュールをインポート
import PySimpleGUI as sg

from sd_png import sd_png_def as spgd
from sd_png import sd_png_window01 as win1
from sd_png import sd_png_window02 as win2
from sd_png import sd_png_window03 as win3
from sd_png import sd_png_window04 as win4
from sd_png import sd_png_window05 as win5
from sd_png import sd_png_window06 as win6


def main_window():
    # メインウィンドウに配置する要素を定義
    sg_button_w = 20
    sg_button_h = 1

    layout = [
        [sg.Button(spgd.SG_WIN_01, size=(sg_button_w, sg_button_h))],
        [sg.Button(spgd.SG_WIN_02, size=(sg_button_w, sg_button_h))],
        [sg.Button(spgd.SG_WIN_03, size=(sg_button_w, sg_button_h))],
        [sg.Button(spgd.SG_WIN_04, size=(sg_button_w, sg_button_h))],
        [sg.Button(spgd.SG_WIN_05, size=(sg_button_w, sg_button_h))],
        [sg.Button(spgd.SG_WIN_06, size=(sg_button_w, sg_button_h))],
    ]

    # ウィンドウを作成
    window = sg.Window("選択してください", layout)

    while True:
        event, values = window.read()    # イベントと入力値を取得
        if event == sg.WIN_CLOSED:  # ウィンドウが閉じられたら
            break   # ループ終了
        elif event == spgd.SG_WIN_01:
            win1.window()
            # break
        elif event == spgd.SG_WIN_02:
            win2.window()
            # break
        elif event == spgd.SG_WIN_03:
            win3.window()
            # break
        elif event == spgd.SG_WIN_04:
            win4.window()
            # break
        elif event == spgd.SG_WIN_05:
            win5.window()
            # break
        elif event == spgd.SG_WIN_06:
            win6.window()
            # break

if __name__ == '__main__':
    main_window()
