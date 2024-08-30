# coding: utf-8
# 変数等を取得する処理

# モジュールをインポート
import os
import datetime
import re

# ライブラリをインポート
from PIL import Image

HISTORY_FILE = "input_history.txt"
PNGINFO_FILE = "pnginfo.txt"

SG_WIN_WIDTH = 600
SG_WIN_HEIGHT = 300

SG_WIN_01 = "pnginfo.txt作成"
SG_WIN_02 = "model別ディレクトリ振分"
SG_WIN_03 = "lora別ディレクトリ振分"
SG_WIN_04 = "seed別ディレクトリ振分"
SG_WIN_05 = "層別ウェイトリネーム"
SG_WIN_06 = "タイムスタンプ変更"

SG_TTL_FILESELECT_01 = "ファイル選択"
SG_STR_FILESELECT_01 = "基準となるファイルを選択して下さい"

SG_TTL_FILESELECT_02 = "ファイル選択"
SG_STR_FILESELECT_02 = "ファイルを選択して下さい(複数化)"

SG_STR_INPUT_01 = "LoRA:"
SG_KEY_INPUT_01 = "-INPUT01-"

SG_STR_HISTORY_01 = "履歴:"
SG_KEY_HISTORY_01 = "-HISTORY01-"

SG_STR_EXECUTE_01 = "ファイル選択"
SG_KEY_EXECUTE_01 = "-EXECUTE01-"

SG_STR_EXECUTE_02 = "実行"
SG_KEY_EXECUTE_02 = "-EXECUTE02-"

SG_STR_CANCEL_01 = "キャンセル"
SG_KEY_CANCEL_01 = "-CANCEL01-"

SG_STR_CHECKBOX_01 = "ディレクトリ名にモデル名を含める？"
SG_KEY_CHECKBOX_01 = "-CHECKBOX01-"

SG_STR_CHECKBOX_02 = "ディレクトリ名に日付を含める？"
SG_KEY_CHECKBOX_02 = "-CHECKBOX02-"

SG_STR_CHECKBOX_03 = "履歴一括処理"
SG_KEY_CHECKBOX_03 = "-CHECKBOX03-"

SG_EXCEPT_NOFILE = "ファイルの指定がないのでキャンセルします"
SG_EXCEPT_NOLORA = "Lora名の指定がないのでキャンセルします"

SG_EXCEPT_ETC = "例外が発生しました"


def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = file.readlines()
            history = [line.strip() for line in history]
            return history
    except FileNotFoundError:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        file.write("\n".join(history))


def get_file_timestamp(file: str, format: int) -> str:
    """
    Args:
        file: ファイルのフルパス文字列
        format: 0 YYYY/mm/dd HH:MM:SS
                1 YYYYmmdd
    Returns:
        ファイルから取得できたタイムスタンプ
    """
    try:
        t = os.path.getmtime(file)
        dt = datetime.datetime.fromtimestamp(t)
        if format == 0:
            ft = dt.strftime("%Y/%m/%d %H:%M:%S")
        elif format == 1:
            ft = dt.strftime("%Y%m%d")
    except:
        ft = f"0000/00/00 00:00:00"
    return (ft)

def add_file_timestamp(file:str, timedelta:datetime.timedelta, timedelta2:datetime.timedelta):
    """
    Args:
        file: ファイルのフルパス文字列
        timedelta: 加算する時刻
    """
    # t = os.path.getatime(file)
    # dt = datetime.datetime.fromtimestamp(t)
    dt = datetime.datetime.now()
    new_dt = dt + timedelta + timedelta2
    new_timestamp = new_dt.timestamp()
    # ファイルのアクセス日時と更新日時をどちらも変更
    os.utime(file, (new_timestamp, new_timestamp))

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


def get_png_metatext(png_file: str) -> str:
    """
    pngファイルをImage.openし、pnginfoを取得します。
    取得できたpnginfoを数行の文字列にして返します。

    Args:
        str: pngファイルのフルパス文字列

    Returns:
        pngファイルから取得できたpnginfo文字列

    Raises:

    """
    metatext = f"{png_file}のpnginfoは読み取れませんでした。\n\n"
    try:
        if os.path.isfile(png_file):
            pass
        else:
            return f"{png_file}は見つかりませんでした。ファイル名にセミコロンがあると読み込みできません。\n\n"

        ft = get_file_timestamp(png_file, 0)
        base_name = os.path.basename(png_file)
        metadata = get_file_metadata(png_file)

        # メタデータをTXTファイルに書き込む用の文字列を作成
        for mkey, mvalue in metadata.items():
            lines = mvalue.splitlines()  # 改行で分割して文字列化する
            # metatext = f"{ft}  {base_name}\n{lines[0]}\n{lines[1]}\n{lines[2]}\n\n"
            metatext = f"{ft}  {base_name}\nキー：{mkey}\n値：{mvalue}\n\n"
    except:
        pass

    return (metatext)


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


def get_png_input_lora_name(png_file: str, input_input_lora_name: str, additional_dir_name: bool) -> str:
    """
    pngファイルのメタデータからLora名を返す
    限りなく先頭に近い方を取得する
    マッチしなければ空欄を返す

    Args:
        png_file: pngファイルのフルパス文字列
        input_input_lora_name: 検索対象のLora名称
        additional_dir_name: Trueならモデル名をディレクトリ名に含める(モデル名_Lora名)

    Returns:
        pngファイルから取得できたpnginfo文字列

    Raises:

    """
    model_name = f""

    try:
        if os.path.isfile(png_file):
            pass
        else:
            return(model_name)

        metadata = get_file_metadata(png_file)

        # メタデータから検索名に使用する要素を抜き出して文字列化する
        # start_pattern = r"^.*<(lora|lyco):"
        # end_pattern = r":-?\d.*>.*$"

        for mkey, mvalue in metadata.items():
            for line in mvalue.splitlines():    # どの行に情報があるか不明なので見つかるまで検索する
                match = re.search(f"<(lora|lyco):{input_input_lora_name}:-?\d.*>", line)

                if match:
                    if additional_dir_name == True:
                        model_name = f"{get_png_model_name(png_file)}_{input_input_lora_name}"  # ディレクトリ名にモデル名も含める場合
                    else:
                        model_name = f"{input_input_lora_name}"
                    break

    except:
        pass

    return (model_name)


def get_png_seed(png_file: str) -> str:
    """
    Args:
        str: ファイルのフルパス文字列
    Returns:
        ファイルから取得できたseed値
    """

    seed = f"#NONEINFO"

    try:
        if os.path.isfile(png_file):
            pass
        else:
            return(seed)

        metadata = get_file_metadata(png_file)

        # メタデータから検索名に使用する要素を抜き出して文字列化する
        # start_pattern = r"^.*Seed: "
        # end_pattern = r", .+$"

        for mkey, mvalue in metadata.items():
            for line in mvalue.splitlines():    # どの行に情報があるか不明なので見つかるまで検索する
                match = re.search(f"Seed: ([0-9]+), ", line)
                if match:
                    seed = f"{match.group(1)}"
    except:
        # seed = f"".rjust(keta)
        pass
    return (seed)


def get_png_lbw(png_file: str, input_lora_name: str) -> str:
    """
    指定されたファイルのpnginfoからinput_lora_nameで指定されたLoRA/Lyco名を取得し
    そのタグの階層構造指定の値をファイル名に追加した文字列を返す
    loraの場合はlora_name:(.+):(.+)>
    lycoの場合はlyco_name:(.+):lbw=(.+)>

    Args:
        png_file: ファイルのフルパス文字列
        input_lora_name: 検索対象のLora名称
    Returns:
        ファイルから取得できたseed値
    """
    model_name = f""
    try:
        if os.path.isfile(png_file):
            pass
        else:
            return f"{png_file}は見つかりませんでした。ファイル名にセミコロンがあると読み込みできません。\n\n"

        metadata = get_file_metadata(png_file)

        # メタデータから検索名に使用する要素を抜き出して文字列化する
        # start_pattern_lora = r"^.*<(lora):"
        # start_pattern_lyco = r"^.*<(lyco):"
        match_pattern = r"[a-zA-Z0-9,-\.]+"
        # end_pattern = r":-?\d.*>.*$"

        for mkey, mvalue in metadata.items():
            for line in mvalue.splitlines():    # どの行に情報があるか不明なので見つかるまで検索する
                match = re.search(f"<lora:{input_lora_name}:.+:({match_pattern})>", line)
                if match:
                    model_name = f"{match.group(1)}"
                    break   # 見つかったら抜けてよい

                match = re.search(f"<lyco:{input_lora_name}.+:lbw=({match_pattern})>", line)
                if match:
                    model_name = f"{match.group(1)}"
                    break   # 見つかったら抜けてよい
    except:
        pass
    return (model_name)