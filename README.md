Project&nbsp;001&nbsp;制作日:2026年9月18日<br>
このプロジェクトは、
台湾中央気象署（CWA）のオープンデータAPIから地震情報を取得し、
MongoDBに同期した上で、
Tkinterを用いたGUIを通じて
データを簡単に照会できるようにする
デスクトップアプリケーションです。<br>
<br><br>
データソース<br>
提供元:交通部中央気象署（CWA）オープンデータプラットフォーム<br>
データセットID: E-A0015-002<br>
データセット名: 顕著有感地震報告データ（英語）<br>
<br>
事前準備<br>
1.パッケージのインストール<br>
ターミナルで以下のコマンドを実行し、必要なライブラリをインストールします。<br>
```pip install -r requirements.txt```<br>
2.APIキーの取得<br>
[こちら](https://opendata.cwa.gov.tw/userLogin)にアクセスし、アカウント登録・ログイン後、「Get Authorization Key」をクリックしてAPIキーをご取得ください。
3.環境変数の設定<br>
ルートディレクトリの .env に取得した APIキー と MongoDB Clusterの接続URL をそれぞれご記述ください。<br>
<br><br>
使い方<br>
データ取得・同期の実行<br>
``get_data.py``を実行します。APIからデータを取得・整形し、MongoDBのコレクションへアップロードします。<br>
検索ツールの起動<br>
``search_tool.py``を実行すると、検索画面（GUI）が立ち上がり、データの照会を開始できます。<br>








