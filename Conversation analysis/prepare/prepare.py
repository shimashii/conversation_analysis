import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
import MeCab
import urllib
import gensim

np.random.seed(0) 
 
text_paths = glob.glob('''任意のテキストファイル''')    
 
def analyzer(text, mecab, stopwords=[], target_part_of_speech=['proper_noun', 'noun', 'verb', 'adjective']):
    
    node = mecab.parseToNode(text)
    words = []
    
    while node:
        
        features = node.feature.split(',')
        surface = features[6]
        
        if (surface == '*') or (len(surface) < 2) or (surface in stopwords):
            node = node.next
            continue
            
        noun_flag = (features[0] == '名詞')
        proper_noun_flag = (features[0] == '名詞') & (features[1] == '固有名詞')
        verb_flag = (features[0] == '動詞') & (features[1] == '自立')
        adjective_flag = (features[0] == '形容詞') & (features[1] == '自立')
        
        if ('proper_noun' in target_part_of_speech) & proper_noun_flag:
            words.append(surface)
        elif ('noun' in target_part_of_speech) & noun_flag:
            words.append(surface)
        elif ('verb' in target_part_of_speech) & verb_flag:
            words.append(surface)
        elif ('adjective' in target_part_of_speech) & adjective_flag:
            words.append(surface)
        
        node = node.next
        
    return words


### ストップワードを指定　stopwordsに入ってる
# ストップワードは以下のページから拝借
req = urllib.request.Request('http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt') 
with urllib.request.urlopen(req) as res:
    stopwords = res.read().decode('utf-8').split('\r\n')
while '' in stopwords:
    stopwords.remove('')
 

### すべての文章を読み込んで分かち書きをする
mecab = MeCab.Tagger("-O wakati")#'-d  C:/Program Files/MeCab/dic/ipadic/')
titles = []
texts = []
for text_path in text_paths:
    
    text = open(text_path, 'r',encoding="utf-8_sig").read()
    text = text.split('\n')
    title = text[2]
    text = ' '.join(text[3:])
    words = analyzer(text, mecab, stopwords=stopwords, target_part_of_speech=['noun', 'proper_noun'])
    texts.append(words)

# 辞書作成    
dictionary = gensim.corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=3, no_above=0.8)
dictionary.save_as_text('blog_dictionary.txt')
# コーパス作成
corpus = [dictionary.doc2bow(t) for t in texts]

# 学習
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, 
                                      num_topics=1000, 
                                      id2word=dictionary, 
                                      random_state=1)

lda.save('blog_dictionary.model')
#rint('topics: {}'.format(lda.show_topics()))
##################################################


import utils

rows = "カブスのダルビッシュ有投手が29日（日本時間30日）、自身のツイッターを更新し、日本ハムの清宮幸太郎内野手、ヤクルトの村上宗隆内野手、ロッテの安田尚憲内野手を「とんでもない」と絶賛した。【PR】今季は国内外合わせて1450試合以上を配信！　ダルビッシュ有を観るなら「DAZN」、”初月無料キャンペーン”実施中　ダルビッシュはツイッターで、村上が4番で起用されることを伝える日本のメディアの記事を紹介。そして、「清宮、村上、安田選手と最近の若い選手はとんでもないですよね」とつぶやいた。さらに「ピッチャーもそうだけど、自分がデビューした時からは考えられないような選手がどんどん増えてきていますね^_^」と、自身と同じピッチャーについても言及している。ダルビッシュは2004年ドラフト1位で日本ハムに入団し、1年目の2005年に1軍デビュー。2年目の2006年に12勝を挙げると、そこから6年連続2桁勝利をマークし、2012年にポスティングシステム（入札制度）でレンジャーズに移籍した。3年目の2007年には最多奪三振のタイトルを獲得し、沢村賞とMVPに輝いている。"
vec = dictionary.doc2bow(utils.stems(rows))
print(lda[vec])
print(lda.print_topic(144))
print(lda.print_topic(289))
#print(lda.print_topic(128))
#
"""
corpus2 = [dictionary.doc2bow(text) for text in docs]

for topics_per_document in lda[corpus2]:
        print(topics_per_document)
        print(lda.print_topic(254))

"""