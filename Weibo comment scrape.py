# -*- coding:utf-8 -*-

import requests
import re
import time
import pandas as pd

# 把id替换成你想爬的地址id
urls = 'https://m.weibo.cn/api/comments/show?id=4073157046629802&page={}'

headers = {'Cookies':'your cookie',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

# 找到html标签
tags = re.compile('</?\w+[^>]*>')

def get_comment(url):
    j = requests.get(url, headers=headers).json()
    comment_data = j['data']['data']
    for data in comment_data:
        try:
            comment = tags.sub('', data['text']) # 去掉html标签
            reply = tags.sub('', data['reply_text'])
            weibo_id = data['id']
            reply_id = data['reply_id']

            comments.append(comment)
            comments.append(reply)
            ids.append(weibo_id)
            ids.append(reply_id)

        except KeyError:
            pass

comments, ids = [], []
for i in range(1, 101):
    url = urls.format(str(i))
    get_comment(url)
    time.sleep(2)

df = pd.DataFrame({'ID': ids, '评论': comments})
df = df.drop_duplicates()
df.to_csv('file.csv', index=False, encoding='gb18030')
