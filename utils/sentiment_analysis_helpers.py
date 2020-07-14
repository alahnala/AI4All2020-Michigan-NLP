import pandas as pd
import wget, os
import glob


NRC_Emotion_Lexicon_Path = 'NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Senselevel-v0.92.txt'
Negators_path = 'NRC-Sentiment-Emotion-Lexicons/SemEval2015-English-Twitter-Lexicon/SemEval2015-English-negators.txt'
Terms_path = 'NRC-Sentiment-Emotion-Lexicons/Sentiment-Composition-Lexicons/NRC-SemEval2015-English-Twitter-Lexicon/SemEval2015-English-Twitter-Lexicon.txt'
Intensity_path = 'NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Intensity-Lexicon-v1/NRC-Emotion-Intensity-Lexicon-v1.txt'
Colors_path = 'NRC-Sentiment-Emotion-Lexicons/NRC-Colour-Lexicon-v0.92/NRC-color-lexicon-senselevel-v0.92.txt'
Valence_path = 'NRC-Sentiment-Emotion-Lexicons/NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt'
Affects = ['fear', 'anger','anticip', 'trust', 'surprise', 'sadness','disgust', 'joy']
Polarities = ['positive', 'negative']

def get_term_rows(term, df):
    term_rows = df.loc[df['term'] == term]
    return term_rows

def load_senselevel_emotion_lexicon():
    WORDS = load_w()
    with open(NRC_Emotion_Lexicon_Path) as f:
        lines = f.read().split('\n')
    data = {'term':[], 'Synonym 1':[], 'Synonym 2':[], 'Synonym 3':[], 'fear':[], 'anger':[], 'anticip':[], 'trust':[], 'surprise':[], 'positive':[], 'negative':[], 'sadness':[], 'disgust':[], 'joy':[]}


    for i in range(0, 242060, 10):
        line = lines[i]
        line = line.strip()
        parts = line.split('--')

        term = parts[0]
        if term in WORDS:
            continue

        try:
            info = parts[1]
        except:
            print(parts, i)

        info_parts = info.split('\t')

        synonyms = info_parts[0]
        synonyms = synonyms.split(',')

        syn_1 = synonyms[0].strip()
        syn_2 = synonyms[1].strip() if len(synonyms) > 1 else ''
        syn_3 = synonyms[2].strip() if len(synonyms) > 2 else ''

        data['term'].append(term)
        data['Synonym 1'].append(syn_1)
        data['Synonym 2'].append(syn_2)
        data['Synonym 3'].append(syn_3)


        for j in range(10):
            line = lines[i+j]
            parts = line.split('\t')
            association = bool(int(parts[-1].strip()))
            emotion = parts[-2]

            data[emotion].append(association)
    del WORDS
    rm_w()
    df = pd.DataFrame(data, columns=list(data.keys()))
    return df

def load_w():
    PATH_ = 'https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en'
    try:
        filename = wget.download(PATH_)
    except:
        filename = 'en'
    with open(filename) as f:
        WORDS = f.read().split('\n')
    return WORDS

def rm_w():
    rm = glob.glob('en*.tmp') + ['en']
    for r in rm:
        try:
            os.remove(r)
        except:
            return
    

def load_colors():
    WORDS = load_w()
    data = {'term':[], 'Synonym 1':[], 'Synonym 2':[], 'Synonym 3':[], 'Color':[], '% Votes':[]}
    with open(Colors_path) as f:
        lines = f.read().split('\n')
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) == 4:
            term = parts[0].split('--')[0]
            if term in WORDS:
                continue
            senses = parts[0].split('--')[1]
            
            synonyms = senses
            synonyms = synonyms.split(',')

            syn_1 = synonyms[0].strip()
            syn_2 = synonyms[1].strip() if len(synonyms) > 1 else ''
            syn_3 = synonyms[2].strip() if len(synonyms) > 2 else ''
            
            color = parts[1].replace('Colour=', '')
            
            if color != 'None':
            
                votes = parts[2].replace('VotesForThisColour=', '')

                total_votes = parts[3].replace('TotalVotesCast=', '')

                vote_percentage = float(votes) / float(total_votes)

                data['term'].append(term)
                data['Synonym 1'].append(syn_1)
                data['Synonym 2'].append(syn_2)
                data['Synonym 3'].append(syn_3)
                data['Color'].append(color)
                data['% Votes'].append(vote_percentage)
    del WORDS
    rm_w()
    data = pd.DataFrame(data, columns=list(data.keys()))
    return data
            

Colors = load_colors()