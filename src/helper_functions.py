import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
mpl.rc('text', usetex=True)
mpl.rc('font', family='Times New Roman')


def filter_abstracts(df):
    print('We have {} rows of raw data'.format(len(df)))
    df = df[df['Abstract'].notnull()]
    print('After filtering, we have {} rows'.format(len(df)))
    return df

def get_grey_colour(word, font_size, position,
        orientation, random_state=None,
        **kwargs):
    """wordcloud colouring"""
    return "hsl(216, 100%, 15.1%)"


def load_data(filename, sheetname):
    return pd.read_excel(os.path.join(os.getcwd(),
                                      '..',
                                      'data',
                                      filename),
                       sheet_name=sheetname)


def make_word_array(df, top_val='all'):
    freq_dist = df['Abstract'].str.split(expand=True)
    freq_dist = freq_dist.apply(lambda x: x.str.replace('[^a-zA-Z]',
                                                        '',
                                                        regex=True))
    freq_dist = freq_dist.apply(lambda x: x.str.strip())
    freq_dist = freq_dist.stack().value_counts()
    print('We have got {} words in our freq dist'.format(len(freq_dist)))
    words_array = []
    if top_val == 'all':
        top_val = len(freq_dist)
    print('Filtering top {} words for length, numbers, stopwords'.format(top_val))
    for i, v in freq_dist[0:top_val].items():
        if i.lower() not in STOPWORDS:
            if (len(i) > 3) and (i.isdigit() is False):
                words_array.append(
                    (i.upper(), float(v))
                )
    return words_array


def make_wc_object(words_array):
    print('Result: {} words going into our cloud'.format(len(words_array)))
    mask = Image.new('RGBA', (7480, 3937))
    icon = Image.open(os.path.join(os.getcwd(),
                                   '..',
                                   'assets',
                                   'high_quality_map.png')).convert('RGBA')
    mask.paste(icon, icon)
    mask = np.array(mask)
    wc = WordCloud(background_color='white',
                   max_words=3500, mask=mask,
                   max_font_size=150)
    wc.generate_from_frequencies(dict(words_array))
    return wc.recolor(color_func=get_grey_colour)


def make_cloud(wc, capt, filename):
    fig, ax = plt.subplots(figsize=(16.18, 10))
    sns.despine(left=True, bottom=True)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_xlabel(capt,
                  loc='center',
                  fontsize=18,
                  color='k')
    plt.imshow(wc, interpolation='bilinear')
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    fig.savefig(os.path.join(os.getcwd(),
                             '..',
                             'figures',
                             filename),
                bbox_inches='tight')