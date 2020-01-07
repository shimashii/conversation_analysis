import glob
import numpy as np
import MeCab
import urllib
import gensim
import re
from operator import itemgetter, attrgetter

pro_noun = []

def _split_to_words(text, to_stem=False):
    """
    入力: 'すべて自分のほうへ'
    出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    """
    tagger = MeCab.Tagger('''任意のディレクトリ''')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(',')
        
        #固有名詞を取得して適当な変数に格納
        if info_elems[1] == "固有名詞":
            pro_noun.append(info_elems[0][:-3])
        
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == '*':
            # info_elems[0] => 'ヴァンロッサム\t名詞'
            words.append(info_elems[0][:-3])
            continue
        if to_stem:
            # 語幹に変換
            words.append(info_elems[6])
            continue
        # 語をそのまま
        words.append(info_elems[0][:-3])
    return words

def words(text):
    words = _split_to_words(text=text, to_stem=False)
    return words

def stems(text):
    stems = _split_to_words(text=text, to_stem=True)
    return stems

###########

text = open("./text.txt", 'r',encoding="utf-8_sig").read()
lda = gensim.models.LdaModel.load('blog_dictionary.model')
dictionary =  gensim.corpora.Dictionary.load_from_text('./blog_dictionary.txt')
vec = dictionary.doc2bow(stems(text))
lda_sims = lda[vec]

nihongo = re.compile('[ぁ-んァ-ン一-龥ー]+')  # 日本語をマッチさせたいときに使う

# 数値の高いトピックの単語を抽出するのと
text = []
standard_way = sorted(enumerate(lda_sims), key=itemgetter(0), reverse=True)
for a, b in standard_way:
    # トピック全体を見た時の類似度(b[1])が0.1を超えるものだけを抽出
    if b[1] > 0.1:
        print(lda.print_topic(b[0]))
        many_char = lda.print_topic(b[0]).split('\" +')
        # 類似度が0.1を超えたトピックの中文字を分解
        for char in many_char:
            # 個別の単語の類似度を見るため正規表現
            num_match = re.compile('.*(\d+)')
            num = num_match.match(char)
            word = nihongo.findall(char)
            # 類似度(num[0])が0.05を超えていれば追加
            if float(num[0]) > 0.05:
                text.append(word[0])

"""
def clean(list):
    sub_list = ""
    new_list = []
    for item in list:
        if nihongo.findall(item):
            sub_list += item
        else:
            if sub_list != "":
                new_list.append(sub_list)
                sub_list = ""
    return new_list

list = clean(text)  # 日本語ワードだけを含むリストを作成。
print(list)

固有名詞入ってる
print(pro_noun)
"""

pro_noun += text
print(pro_noun)