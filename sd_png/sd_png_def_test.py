import unittest
import tempfile

import os
import datetime

import sd_png_def

class TestGetFileTimestamp(unittest.TestCase):  #このクラスは、unittest.TestCaseを継承します。
    # unittest.TestCaseクラスは、Pythonのunittestモジュールが提供するクラスで、ユニットテストのための各種機能（アサーションメソッドなど）を提供します。

    # Pythonのクラスメソッドの最初の引数としてselfが使用されます。
    # selfは、現在のクラスインスタンス（オブジェクト）を参照します。
    #   つまり、selfを通じて、クラスの属性（変数）やメソッド（関数）にアクセスできます。

    # テストメソッドにおけるselfも同様で、unittest.TestCaseのインスタンスを参照します。
    # selfを通じて、TestCaseクラスのメソッド（例えばassertEqualやassertAlmostEqualなどのアサーションメソッド）や属性にアクセスできます。

    # test_dirやtest_fileをselfのプロパティ（属性）として設定する理由は、
    # setUpメソッドとtearDownメソッド、そしてテストメソッド間でこれらの値を共有するためです。
    # setUpメソッドでself.test_dirやself.test_fileを設定すると、これらの値はtearDownメソッドやテストメソッドからアクセスできます。
    # これにより、テストの初期化と後処理、そしてテストの実行を一貫して行うことができます。

    def setUp(self):    #setUPは、各テストメソッドの前に実行される
        # テストメソッドは、頭に「test_」をつける

        # テスト用のディレクトリとファイルを作成
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, 'test_file.txt')
        with open(self.test_file, 'w') as f:
            f.write('test')

    def tearDown(self): #tearDownは、各テストメソッドの終了後に実行される
        # # テスト用のファイルを削除
        # os.remove(self.test_file)
        # テスト用のディレクトリを削除（中のファイルもすべて削除されます）
        self.test_dir.cleanup()

    def test_get_file_timestamp_format0(self):
        timestamp = sd_png_def.get_file_timestamp(self.test_file, 0)
        dt = datetime.datetime.now()
        expected = dt.strftime("%Y/%m/%d %H:%M")
        # 秒までの比較は難しいため、分までの比較とする
        self.assertEqual(timestamp[:16], expected)

    def test_get_file_timestamp_format1(self):
        timestamp = sd_png_def.get_file_timestamp(self.test_file, 1)
        dt = datetime.datetime.now()
        expected = dt.strftime("%Y%m%d")
        self.assertEqual(timestamp, expected)

    def test_get_file_timestamp_invalid_file(self):
        timestamp = sd_png_def.get_file_timestamp('invalid_file.txt', 0)
        self.assertEqual(timestamp, '0000/00/00 00:00:00')

    def test_add_file_timestamp(self):
        # テスト前のタイムスタンプを取得
        timestamp_before = os.path.getmtime(self.test_file)

        # timedeltaを作成
        timedelta1 = datetime.timedelta(seconds=1)
        timedelta2 = datetime.timedelta(seconds=2)

        # 関数を実行
        sd_png_def.add_file_timestamp(self.test_file, timedelta1, timedelta2)

        # テスト後のタイムスタンプを取得
        timestamp_after = os.path.getmtime(self.test_file)

        # タイムスタンプが正しく加算されたことを確認
        self.assertAlmostEqual(timestamp_after, timestamp_before + 3, delta=1)
        # `assertAlmostEqual`はPythonの`unittest`モジュールの`TestCase`クラスのメソッドです¹³⁴⁵⁶。このメソッドは、2つの値がほぼ等しいかどうかをテストします¹³⁴⁵⁶。

        # 具体的には、以下の手順でテストを行います¹⁴⁵：
        # 1. まず、2つの値の差を計算します¹⁴⁵。
        # 2. 次に、その差を指定された小数点以下の桁数（デフォルトは7）で四捨五入します¹⁴⁵。
        # 3. 最後に、四捨五入した値がゼロと等しいかどうかを比較します¹⁴⁵。

        # このメソッドは、浮動小数点数の比較に便利です。浮動小数点数は誤差が生じやすいため、完全に等しいかどうかを比較するのではなく、ほぼ等しいかどうかを比較することが多いです。

        # テストコード中の`self.assertAlmostEqual(timestamp_after, timestamp_before + 3, delta=1)`は、`timestamp_after`と`timestamp_before + 3`がほぼ等しいことを確認しています。ここで、`delta=1`は許容誤差を1秒に設定しています。つまり、`timestamp_after`と`timestamp_before + 3`の差が1秒以内であれば、テストはパスします。

        # 以上が、`assertAlmostEqual`メソッドの説明です。ご質問がありましたら、お気軽にどうぞ。😊

        # ソース: Bing との会話 2023/11/16
        # (1) unittest — Unit testing framework — Python 3.12.0 .... https://docs.python.org/3/library/unittest.html.
        # (2) Python unittest - assertAlmostEqual() function - GeeksforGeeks. https://www.geeksforgeeks.org/python-unittest-assertalmostequal-function/.
        # (3) Python assertAlmostEqual. https://www.pythontutorial.net/python-unit-testing/python-assertalmostequal/.
        # (4) Python assertAlmostEqual() - python tutorials. https://python-tutorials.in/python-assertalmostequal/.
        # (5) Python unittest assertAlmostEqual()用法及代码示例 - 纯净天空. https://vimsky.com/examples/usage/python-unittest-assertalmostequal-function.html.
        # (6) [py2rb] assertAlmostEqual #Python - Qiita. https://qiita.com/superrino130/items/9393113c4b204ef7f8d7.
        # (7) undefined. https://docs.python.org/ja/3.7/library/unittest.html.

if __name__ == '__main__':
    # __main__は、直接コール（コマンドラインから実行された）場合に動くメソッド
    unittest.main() # テストを実行する関数

    # unittest.TestCaseを継承した全てのクラスを見つけ、
    # それらクラスの中の「test_」から始まる全てのメソッドをテストメソッドとして実行する。
