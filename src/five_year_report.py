from helper_functions import load_data, \
    make_word_array, \
    make_wc_object, \
    make_cloud


def main():
    capt = (r'\textbf{Source:} All abstracts of papers published '
             'by LCDS researchers between November 1st, 2019 '
             'and October 31st, 2023\n'
             r' \textbf{See:} https://github.com/oxforddemsci/LCDSoutputs to '
             'reproduce this figure, consistent with our Open '
             'Access philosophy.')
    df = load_data('LCDSPublicationsYear1_4.xlsx',
                   'all_pubs')
    df = df[df['Abstract'].notnull()]
    words_array = make_word_array(df)
    wc = make_wc_object(words_array)
    make_cloud(wc, capt, 'five_year_report.svg')


if __name__ == "__main__":
    main()