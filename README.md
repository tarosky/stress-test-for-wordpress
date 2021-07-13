# Stress Test for WordPress

WordPressに負荷テストを与えるためのツールです。[locust](https://docs.locust.io/en/stable/index.html) をベースにしています。WordPress以外でも実は動きます ;)

## Installation

Locust をシステムにインストールします。現時点（2021/06）ではPython 3.8のpipで `v1.5.3` がインストールされます。

```
pip install locust
```

このリポジトリをクローンします。

```
git clone git@github.com:tarosky/stress-test-for-wordpress.git
```

これで準備は完了です。

## Configuration

設定の前にテストの項目を決定しましょう。

- 対象となるベースURL
- Basic認証の有無
- テストすべきページ
- 耐えられるべき同時接続ユーザー数

### テスト対象ページ

- トップページ
- アーカイブページ2種類からランダムに1ページ
- シングルページ10種類からランダムに1ページ

今回はニュースポータルを想定し、トップページ、カテゴリーページ、記事ページという同線を想定します。これらのページパターンはサイトによって異なるので、余すことなく含めるようにしましょう。負荷の高いページ（例・画像が多くスライドショーが入っている）などを含めると、よりリアルなテストになります。

### 同時接続ユーザー数

同時にアクセスするユーザー数ですが、どれだけの数があればよいかというのは、現在のサイトのリクエスト数から算出するとよいでしょう。たとえば、Google Analyticsの同時接続数でピークの値がわかっていれば、それは直近5分でのユーザー数なので、その倍のユーザー数をlocustで設定すれば、十分満たすはずです。

今回は同時接続 **ユーザー数として1,000人** を想定しましょう。Google Analyticsで同時接続500人程度であれば、十分しのげる計算になります。

### 設定ファイルの編集

テストすべき値が決まったらこのリポジトリにある設定ファイル `setings.example.json` をコピーして `settings.json` として保存してください。

```json
{
	"requests": {
		"archives": [
			"/category/news",
			"/category/sports"
		],
		"singles": [
			"/article/1",
			"/article/2",
			"/article/3",
			"/article/4"
		]
	},
	"auth": {
		"user": "admin",
		"pass": "password"
	},
	"wait": {
		"min": 2,
		"max": 4
	}
}
```

それでは、この `settings.json` を編集して保存しましょう。省略し値は無視されるので、たとえばBasic認証がかかっていないなら `auth` はなくしてしまって大丈夫です。

ページリストとして現在のところ許容される値は `singles` と `archives` のみです。これにルートページへのアクセスが追加されます。

後述するように複数の環境を含めたい場合は `setting-dev.json` のように `settings-*.json` という名前で保存してください。

## Run Test

```
locust
```

環境を指定して実行する場合は環境変数 `WP_STRESS_TEST` を指定して実行してください。以下の例では `settings-dev.json` が利用されます。

```
export WP_STRESS_TEST=dev && locust
```

実行すると、Web UI（e.g. `http://localhost:8089/` ）が生成されるのでアクセスします。

- Number of total users to simulate = テストする合計人数
- Hatch rate = 1秒あたりに増えていく人数の増加率
- Host = ベースURL

上記を入力して実行すると、テスト結果が得られます。

## Lisence

このリポジトリはMITライセンスで提供されています。