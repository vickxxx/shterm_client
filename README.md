# shterm_client
齐治堡垒机客户端

macbook pro 升级monterey后，齐治堡垒机的ShtermClient可能无法启动，使用该脚本替代

## 安装

1. 更改qzssh中path值为本项目的绝对路径

2. ln -s [绝对路径]/qzssh /usr/local/bin 

## 使用

2. 浏览器中，打开调试工具，获取/inflate.php接口响应

3. 执行qzssh shterm://[获取的base64串],即可唤起终端
