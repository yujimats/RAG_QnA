# 概要
Q&A集からRAG検索を行うプログラム。  

# 事前準備
## データの準備
データをダウンロードし、[`./data/`](./data/)に`data.jsonl`ファイルを保存する。  
ダウンロード元は以下。  
<https://huggingface.co/datasets/matsuxr/JaGovFaqs-22k>  
手動でダウンロードするか、['get_data.sh'](./get_data.sh)を実行する。  
## Dockerの準備
[`./docker/README.md`](./docker/README.md)を参照し、準備する。  
## APIキーの準備
OpenAIの任意のアカウントにて、APIキーを取得する。  
APIキーは、[`./src/.ENV`](./src/.ENV)ファイルに以下のフォーマットで保存する。  
```.env
API_KEYS=**********
```

# 実行方法
Dockerコンテナ内で以下を実行する。  
```bash
$ python3 main.py
```
jupyter notebookを実行する場合は、[`http://localhost:8888`](http://localhost:8888)二アクセスし実行すること。  
「異常気象」に関連するQ&Aが出力されればOK。

プロンプトは[`./src/main.py`](./src/main.py)の以下の部分で設定している。  
ここを任意で変更すると、応答も変化する。  
```python
# response
strings, relatednesses = query_collection(
    collection=stevei_collection,
    query='昨今の異常気象の原因を教えて下さい',
    max_results=3,
)
```


