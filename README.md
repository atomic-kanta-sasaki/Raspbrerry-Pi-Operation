## Raspberry Pi 4B CUI操作メモ

### bluetoothを接続する方法
#### SDPサービスの確認方法
 - sdptool browse local
エラーが出ている場合は権限が必要なため以下のコマンドを入力する<br />
 - sudo chmod 777 /var/run/sdp

#### bluetooth modeに入る方法
 - bluetoothctl

#### 周辺のBluetooth機器をScanする方法
 - scan on （これにより接続済みデバイスのRSSIも取得することができる）

#### 接続方法
 - pair device adress

#### bluetooth mode 終了
 - exit

### シリアル通信設定方法
以下のコマンドを叩いていきペアリングできる状態にする<br />
1. sudo bluetoothctl
2. power on
3. discoverable on
4. agent on
5. default-agent

#### bluetoothを起動する
 - sudo systemctl daemon-reload <br />
 - sudo systemctl restart bluetooth

#### RFCOMMセットアップ
 - sudo rfcomm listen /dev/rfcomm0 22 <br />
この後windowsのTera Termを使用し所定のポートで通信を開始する <br />
```
Press CTRL-C for hangup 
```
という表示がでればシリアル通信を行う準備が完了している <br />
can't create RFCOMM TTY: Adress already in use<br />
というエラーが発生した場合は
 - sudo rfcomm release hci0
を入力しアドレスを開放する

### シリアル通信の方法（CUIの場合）
#### Raspberry Pi 側でメッセージを確認する場合
 - sudo cat /dev/rfcomm0

#### Raspberry Pi側からWindowsPC側へデータを送信
 - sudo eco abcd > /dev/rfcomm0

#### windows側でcomポートを設定するときの注意点
 - 今現在の推測だが rfcomm listen /dev/rfcomm0 22を実行してRaspberry Pi側で待機をしていないとWindowsで仮想COMポートの設定ができないため注意が必要

### 参考文献
　https://qiita.com/oko1977/items/9f53f3b11a1b033219ea

#### 現在の状況
Raspberry Pi 4B上で/dev/rfcomm0 22のアドレスを開放しwindowsとCUIベースでのシリアル通信ができるという状況の下Pythonを使用してデータのやり取りが可能である.<br />
複数台のWindowsPCと接続した状態で選択的に接続するWindowsを選べるのかどうかはよくわかっていないため後日実験が必要.


