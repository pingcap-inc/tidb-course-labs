# TiDB Database Administration for Self-Hosted Deployments 学生向けラボ環境設定ガイド

## 前提条件
1. ラップトップとインターネット接続がインターネット ホストのポート 22、ポート 2379、およびポート 3000 にアクセスできることを確認してください。

## ラップトップのセットアップと SSH ログイン (Linux または macOS)
1. 事前設定は必要ありません。
   
2. トレーニング当日、ラボ ガイドに従って、秘密キー ファイル (`*.pem`) をダウンロードし、その権限を `400` に設定するように指示されます。例:
   ```
   $ mv <key_file> ~/.ssh/ 
   $ chmod 400 ~/.ssh/<key_file>
   ``` 

3. ラボガイドに従って EC2 インスタンスに接続します。

## ラップトップのセットアップと SSH ログイン (Windows)
Windows ユーザーは、Windows WSL またはターミナル エミュレーターの使用を検討できます。推奨されるターミナル エミュレーターは PuTTY です。PuTTY を使用して EC2 に接続する手順は、以下に記載されています。 

1. [PuTTY](https://www.putty.org/)をコンピュータにインストールします。
   
   [PuTTY](https://www.putty.org/) 公式ページから PuTTY をダウンロードしてインストールします。古いバージョンの PuTTY がすでにインストールされている場合は、最新バージョンをダウンロードすることをお勧めします。必ずスイート全体をインストールしてください。

2. トレーニング当日、ラボ ガイドに従って秘密キー ファイル (`*.pem`) をダウンロードします。[PuTTYgen](https://www.puttygen.com/) を使用して、秘密キー ファイル (`*.pem`) を `*.ppk` 形式に変換する必要があります。

   AWS の [ガイド](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/connect-linux-inst-from-windows.html) の「PuTTYgen を使用して秘密鍵を変換する」セクションに従ってください。

3. PuTTY を使用して Windows から EC2 インスタンスに接続します。

   AWS の [ガイド](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/connect-linux-inst-from-windows.html) の「Linux インスタンスへの接続」セクションに従ってください。

4. このガイドはここで終了します。インストラクターの指示とラボ ガイドに従って演習を完了してください。