<div id="top"></div>

# 献血ナビプロジェクト

## 概要

このプロジェクトは、献血者数の推移を予測するモデルの開発とWebサイトの運営を通じて、必要な血液量の適切な確保に貢献することを目指しています。

予測結果は [GitHub Pages](https://ren-h129.github.io/kenketsu-navi/) で公開しています。


## 使用技術
<p style="display: inline">
    <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
    <img src="https://img.shields.io/badge/-Jupyter-FFFFFF.svg?logo=jupyter&style=popout">
    <img src="https://img.shields.io/badge/-sklearn-F37626.svg?logo=&style=popout">
    <img src="https://img.shields.io/badge/pandas-005d8b?style=flat&logo=pandas&logoColor=fffefe" alt="Badge">
    <img src="https://img.shields.io/badge/NumPy-1e89c0?style=flat&logo=numpy&logoColor=fffefe" alt="Badge">
    <img src="https://img.shields.io/badge/-Javascript-F7DF1E.svg?logo=javascript&style=popout">
    <img src="https://img.shields.io/badge/-Jquery-0769AD.svg?logo=jquery&style=popout">
    <img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
    <img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
    <img src="https://img.shields.io/badge/-Github%20Actions-181717.svg?logo=github&style=popout">
    <img src="https://img.shields.io/badge/-GitHub%20Pages-222222.svg?logo=githubpages&style=popout">
</p>

## 動作環境
| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.12        |
| beautifulsoup4        | 4.12.3     |
| Jinja2                | 3.0        |
| Jmap                  | 0.0.1      |
| matplotlib            | 3.8.4      |
| numpy                 | 1.26.4     |
| pandas                | 2.2.2      |
| PyPDF2                | 3.0.1      |
| python-dotenv         | 1.0.1      |
| requests              | 2.32.2     |
| statsmodels           | 0.14.2     |

その他のパッケージのバージョンは [requirements.txt](./requirements.txt) を参照してください。

## ディレクトリ構成
```txt
./
├─ .github/                               # GitHub関連の設定ファイルやワークフロー
├─ data/                    
│   ├─ BloodDonation.csv                  # 献血者数のデータ
│   ├─ BloodRoom.csv                      # 各献血ルームのデータ
│   ├─ BloodStock_.csv                    # 最新の血液在庫データ
│   ├─ graph.csv                          # 可視化用に加工されたデータ
│   └─ jrc_blood_donation_report_raw.pdf  # 日本赤十字社が公開している献血速報のPDF（オープンデータ）
├─ module/
│   ├─ download.py                        # 献血者数速報PDFのダウンロード
│   ├─ ocr.py                             # PDFからテキストを抽出するOCR処理           
│   ├─ predict.py                         # 献血者数の予測モデル
│   └─ scrape.py                          # 最新の献血在庫のスクレイピング
├─ notebooks/                             # データ分析とモデル検証用ファイル
│   ├─ analyze.ipynb                      # 変動成分、定常性、相関分析と結果の作図
│   ├─ model.ipynb                        # SARIMAモデルの構築と評価
│   └─ visualization.ipynb                # データの可視化と結果の作図
├─ static/                                # 静的ファイル
│   ├─ css/                 
│   ├─ images/              
│   └─ scripts/            
├─ templates/                             # HTMLテンプレートファイル
├─ build_static_site.py                   # GitHub Pages用の静的HTML生成
├─ site_data.py                           # ページ生成で使うデータ処理
├─ README.md                
└─ requirements.txt                       # ライブラリのリスト
```

## データファイル
- [BloodDonation.csv](./data/BloodDonation.csv) :　2017年1月からの47都道府県ごとの献血者数

    これらのデータは[日本赤十字社 | 献血者数・供給本数速報
](https://www.jrc.or.jp/donation/blood/data/)より取得しています。

    また、[2025年3月分のデータ](https://github.com/5522079/kenketsu-navi/commit/a419b87af7b663257f3195598095b9b47240773c)からAzure Document Intelligenceを導入し、手動でのデータ追加ではなくOCRによる自動インポートを行っています（完全なファクトチェックは実施していません）。

    ![BloodDonation.csv_header](https://github.com/user-attachments/assets/980fdd2a-f60d-4f1b-81c7-ff6d273791a0)

  1. `year`：西暦<br>
    2017 から 2025 までの値。

  2. `month`：月<br>
    1 から 12 までの値。

  3. `prefecture_id`：各都道府県に割り当てた固有の識別番号。<br>
    1 から 47 の値。各都道府県のコードは[都道府県コードの早見表](https://tundra-bugle-bc4.notion.site/2f462cc8750948878dbfe143640f33ab?pvs=4)を参照してください。

  4. `blood_donors`：総献血者数

  5. `whole_blood_donation`：全血献血（200mL・400mL 献血）の献血者数<br>

  6. `200mL_blood_donation`：200mL 献血者数

  7. `400mL_blood_donation`：400mL 献血者数

  8. `component_blood_donation`：成分献血（血漿成分・血小板成分献血）の献血者数<br>

  9. `PPP_blood_donation`：血漿成分献血献血者数

  10. `PC_blood_donation`：血小板成分献血者数

- [BloodStock_.csv](./data/) :　最新の血液在庫状況

    各地域ごとの赤十字血液センターの公式ウェブサイトより献血状況を取得しています。

    北海道ブロック : [日本赤十字社 | 北海道赤十字血液センター](https://www.bs.jrc.or.jp/hkd/hokkaido/index.html)<br>
    東北ブロック : [日本赤十字社 | 東北ブロック血液センター](https://www.bs.jrc.or.jp/th/bbc/index.html)<br>
    関東甲信越ブロック : [日本赤十字社 | 関東甲信越ブロック血液センター](https://www.bs.jrc.or.jp/ktks/bbc/index.html)<br>
    近畿ブロック : [日本赤十字社 | 近畿ブロック血液センター](https://www.bs.jrc.or.jp/kk/bbc/index.html)<br>
    中四国ブロック : [日本赤十字社 | 中四国ブロック血液センター](https://www.bs.jrc.or.jp/csk/bbc/index.html)<br>
    九州ブロック : [日本赤十字社 | 九州ブロック血液センター](https://www.bs.jrc.or.jp/bc9/bbc/index.html)<br>

- [jrc_blood_donation_report_raw.pdf](./data/jrc_blood_donation_report_raw.pdf) :　日本赤十字社が公開している最新の全国血液センター献血者数速報の1ページ目（献血方法別献血者数）

    このPDFファイルは[日本赤十字社 | 献血者数・供給本数速報
](https://www.jrc.or.jp/donation/blood/data/)より取得しています。


<p align="right">(<a href="#top">トップへ</a>)</p>