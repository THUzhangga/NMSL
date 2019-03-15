# NMSL
Abstraction your words——never mind the scandal and liber

## 运行要求

Python3

需要的库包括：jieba、pandas、pinyin

## 抽象词典

在data/bible.xlsx中，部分词典如下：

| 笑     | 😁    |
| ------ | ---- |
| 笑哭   | 😂    |
| 色     | 😍    |
| 亲     | 💋    |
| 哭     | 😭    |
| 晕     | 😵    |
| 愤怒   | 👿    |
| 生气   | 👿    |
| 怒     | 👿    |
| 死     | 💀    |
| 鬼     | 👻    |
| 外星人 | 👽    |
| 屎     | 💩    |
| 男孩   | 👦    |
| 男生   | 👦    |
| 男人   | 👨    |
| 男     | 👨    |

## 抽象模式

### 轻度抽象

首先进行分词，然后对分词检索，替换为emoji。如果分词未找到emoji，再对单字检索。

### 深度抽象

步骤同上，但是会对字检索后，如未成功，会对拼音检索。

具体见：https://zhuanlan.zhihu.com/p/55175079