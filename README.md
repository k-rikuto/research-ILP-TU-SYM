# 概要
大学の研究に用いたコード（Python）

# 実行手順
1.  ローカル環境にプロジェクトフォルダを作成する。
2.  プロジェクト直下にpythonの仮想環境を構築する。
    (参考：https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e)
3.  リモートリポジトリのクローンをプロジェクト直下に取り込む
    (git clone https://github.com/k-rikuto/research.git)
4.  仮想環境を立ち上げる。
    (source .venv/bin/activate)
5.  このフォルダにあるrequirements.txtに記載してあるパッケージをインストールする。
    (pip3 install -r requirements.txt)
6.  ファイルを実行する。

# generate_request.py

def generate_request() -> list[int]:
    
    #data_05:request_04
    r_num = [1, 1, 0, 1, 2, 0, 1, 0, 0, 1, 2, 1, 0, 2, 0, 0, 1, 2, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 5, 0, 2, 0, 2, 1, 0, 4, 0, 2, 0, 2, 0, 1, 2, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2, 1, 0, 2, 0, 0, 2, 3, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 2, 1, 0, 5, 0, 1, 1, 1, 1, 2, 1, 0, 2, 0, 0, 0, 1, 4, 1]

    return r_num

よく変更する場所なのでgitに載せてないです。