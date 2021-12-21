from pandas import DataFrame,read_csv
from re import sub
from jieba import lcut
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import ndarray
#读取从金十数据获取的文本记录
filename='text_analysis.csv'
# 待分词的 csv 文件中的列
document_column_name = 'content'
#预先定义正则表达式，去除所有的中文标点符号
pattern = u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+a-zA-Z，。\n《》、？：；“”‘’｛｝【】（）…￥！—┄－]+'
def top_words_data_frame(model: LatentDirichletAllocation,
                         tf_idf_vectorizer: TfidfVectorizer,
                         n_top_words: int) -> DataFrame:
    '''
    求出每个主题的前 n_top_words 个词
    Parameters
    ----------
    model : sklearn 的 LatentDirichletAllocation
    tf_idf_vectorizer : sklearn 的 TfidfVectorizer
    n_top_words :前 n_top_words 个主题词

    Return
    ------
    DataFrame: 包含主题词分布情况
    '''
    rows = []
    feature_names = tf_idf_vectorizer.get_feature_names()
    for topic in model.components_:
        top_words = [feature_names[i]
                     for i in topic.argsort()[:-n_top_words - 1:-1]]
        rows.append(top_words)
    columns = [f'topic {i+1}' for i in range(n_top_words)]
    df = DataFrame(rows, columns=columns)

    return df
def predict_to_data_frame(model: LatentDirichletAllocation, X:ndarray) -> DataFrame:
    '''
    求出文档主题概率分布情况

    Parameters
    ----------
    model : sklearn 的 LatentDirichletAllocation
    X : 词向量矩阵

    Return
    ------
    DataFrame: 包含主题词分布情况
    '''
    matrix = model.transform(X)
    columns = [f'P(topic {i+1})' for i in range(len(model.components_))]
    df = DataFrame(matrix, columns=columns)
    return df
#读取csv文件
df = (
    read_csv(
        filename,error_bad_lines=False)
    .drop_duplicates()
    .dropna()
    .rename(columns={
        document_column_name: 'text'
    }))

# 去重、去缺失、分词,以及使用jieba的精确模式，避免重读
df['cut'] = (
    df['text']
    .apply(lambda x: str(x))
    .apply(lambda x: sub(pattern, ' ', x))
    .apply(lambda x: " ".join(lcut(x,cut_all=False)))
)
print(df['cut'])
#
tf_idf_vectorizer= TfidfVectorizer()
tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])
# 获取特征词列表
feature_names = tf_idf_vectorizer.get_feature_names()
# 特征词 TF-IDF 矩阵
matrix = tf_idf.toarray()
# 指定 lda 主题数
n_topics =10
LDA = LatentDirichletAllocation(
    n_components=n_topics, max_iter=150,
    learning_method='online',
    learning_offset=50.,
    random_state=0)

n_top_words = 20
LDA.fit(tf_idf)
top_words_df = top_words_data_frame(LDA, tf_idf_vectorizer, n_top_words)

# 保存 n_top_words 个主题词到 csv 文件中
# 输出主题词的文件路径
top_words_csv_path = 'Top listed words.csv'
# 输出各文档所属主题的文件路径
predict_topic_csv_path = 'Probability of each topic.csv'
top_words_df.to_csv(top_words_csv_path, encoding='utf-8-sig', index=None)
X = tf_idf.toarray()
# 计算完毕主题概率分布情况
predict_df = predict_to_data_frame(LDA, X)
# 保存文本主题概率分布到 csv 文件中
predict_df.to_csv(predict_topic_csv_path, encoding='utf-8-sig', index=None)
print("dfdf")