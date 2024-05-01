# coding: utf-8
# カレントディレクトリのpng画像ファイルのpnginfoにもとづき
# ファイルをモデル名のフォルダに移動します

# モジュールをインポート
import os
import shutil
import re

from PIL import Image

def get_file_metadata(file: str) -> dict:
    """
    Args:
        str: ファイルのフルパス文字列
    Returns:
        ファイルから取得できたpngメタデータ
    """
    img = Image.open(file)   # PNG画像ファイルを読み込む
    img.load()  # load()メソッドでメタデータがinfo属性に格納されることを保証する
    return (img.info)  # info属性からメタデータを取得する


def get_png_model_name(png_file: str) -> str:
    """
    pngファイルのメタデータから生成に使用されたモデル名を取得します

    Args:
        png_file: pngファイルのフルパス文字列

    Returns:
        pngファイルから取得できたpnginfo文字列

    Raises:

    """
    # モデルハッシュ値からモデル名を定義する為の変数
    hash_dict = {
        "925997e9": "NovelAI_animefull-final-pruned",
        "38c1ebe3": "Anything-V3.0-pruned-fp16",
        "4a4a52c4": "7th_anime_v1.1",
        "4de704d8": "almond_cinamon_basil",
        "4f906d95": "bloodcina0.3",
        "58841f67": "almond_fix_basil_fix",
        "5ad7e928": "anyblood0.5",
        "71931526": "yuzuchai3.5_yuzuchai9.5",
        "8bcc83d5": "7th_anime_v2_A",
        "8f370490": "Almond grape mix",
        "931f9552": "AbyssOrangeMix2_hard",
        "97779618": "dall666",
        "a87fd7da": "AbyssOrangeMix2_sfw",
        "c5b48204": "bloodany0.3",
        "cc44dbff": "BloodOrangeMix",
        "cf8527ef": "AbyssOrangeMix_half",
        "d4148d5d": "7th3a_7th3b",
        "de2f2560": "AbyssOrangeMix_Night",
        "feabede1": "anyanygape0.5",
        "ffa7b160": "Abyss_7th_layer_blood_0.0_blood_0.5"}

    model_name = f""    # 戻り値
    model_hash_name = f"#NONEINFO"  # モデル名もhash値も取得できなかった時の為のディレクトリ名

    try:
        if os.path.isfile(png_file):
            pass
        else:
            return (model_name)

        metadata = get_file_metadata(png_file)

        # メタデータからディレクトリ名に使用する要素を抜き出して文字列化する
        # start_pattern = r"^.*Model: "   # Model名を取得する版
        # start_hash_pattern = r"^.*Model hash: "   # Modelハッシュ名を取得する版
        # end_pattern = r", .+$"

        for mkey, mvalue in metadata.items():
            # 改行で分割してリスト化する
            # lines = mvalue.splitlines()
            # 0:prompt
            # 1:ng
            # 2:Steps: 20, Sampler: DPM++ 2M Karras, CFG scale: 7, Seed: 632811559, Size: 512x768, Model hash: 3e45450e39, Model: 3D_chilled_remixr_v1vae, Clip skip: 2, ENSD: 31337
            # 2から抜き出す要素
            #  Model名
            # 作成するディレクトリ名
            #  日付_Model名
            for line in mvalue.splitlines():    # (改行でループ)どの行にモデル情報があるか不明なので見つかるまで検索する
                match = re.search(f"Model: (.*?), ", line)
                if match:
                    model_name = f"{match.group(1)}"
                    break   # モデル名が見つかったら抜ける
                # ハッシュ値が見つかるまで検索する
                match = re.search(f"Model hash: ([a-z0-9]+)", line)
                if match:
                    hash_name = hash_dict.get(match.group(1), match.group(1))   # モデル名が空だったらモデルハッシュ名を入れる
                    model_hash_name = f"{hash_name}"
                    # モデル名を優先したいのでマッチしても抜けない
    except:
        pass

    model_name = model_hash_name if model_name == f"" else model_name   # モデル名が空だったらモデルハッシュ名を入れる
    model_name = model_name[:50]    # 先頭50文字だけにする

    return (model_name)


def window(source_filepaths, current_path: str):
    for file in source_filepaths:
        model_name = get_png_model_name(file)  # 読み込んだファイルからモデル名を取得
        model_dir = os.path.join(current_path, model_name)   # 振分先ディレクトリ名を作成
        os.makedirs(model_dir, exist_ok=True) if not os.path.isdir(model_dir) else None  # ディレクトリがなければ作成
        shutil.move(file, model_dir)    # 作成したディレクトリにファイルを移動


current_path = os.path.dirname(__file__)
files = []

# ファイルを取得
for file in os.listdir(current_path):
    file_path = os.path.join(current_path, file)
    # ファイルかつ拡張子.pngなら処理対象にする
    if os.path.isfile(file_path) and str(os.path.splitext(file_path)[1]).lower() == ".png":  #isdirの代わりにisfileを使う
        files.append(file_path)

window(files, current_path)
