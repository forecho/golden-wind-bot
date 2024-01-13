# golden-wind-bot

```
pip3 install requests
pip3 install pyyaml
pip3 install telepot --upgrade
```

## 使用方法

复制配置文件，并且修改

```
cp config.yml.example config.yml
```


获取 Telegram `chat_id` :

```
python3 test_telegram.py
```

然后给 telegram bot 发消息，查看终端，第三个参数就是。

初始化数据库：

```
python3 init.py
```

发送消息命令（加定时任务就可以实现定时推送了）：

```
python3 main.py
python3 ark.py
```
