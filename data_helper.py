import os
import os.path
import numpy as np
import pickle
import codecs
from konlpy.tag import Okt
from hyperparams import params
from gensim.models import FastText

#tokenizer
tokenizer = Okt()

def make_word_dictionary(word_dict_pkl_path=params['default_word_dict_pkl_path'], training_data_path = params['default_training_data_path']):
    #word_dict => 'Word':'index'
    word_dict = dict()
    if os.path.isfile(word_dict_pkl_path):
        #if already existed, just load it
        with open(word_dict_pkl_path, 'rb') as f:
            word_dict = pickle.load(f)
            print('Existed word_dict loaded')
    else:
        print('No word_dict pkl file, start making word_dict...')
        with codecs.open(training_data_path, 'r', encoding='utf-8') as f:
            word_vocab = dict()
            # 'word':'frequency'
            for line in f.read().split('\n')[1:]:
                review = line.split('\t')[1]
                #tokenizing
                tokens = tokenizer.morphs(review)
                for token in tokens:
                    if token in word_vocab.keys():
                        word_vocab[token] += 1
                    else:
                        word_vocab[token] = 1
            word_vocab = [word for word in word_vocab.keys() if word_vocab[word] >= params['min_vocab_count']]
            # add pad & unk token
            word_vocab = [params['PAD']] + word_vocab + [params['UNK']]
            for idx, word in enumerate(word_vocab):
                word_dict[word] = idx
        print('Making word_dict ... Done and Saved')
        with open(word_dict_pkl_path, 'wb') as f:
            pickle.dump(word_dict, f)
    return word_dict

def make_word_embedding(word_dict, word_emb_pkl_path = params['default_word_emb_pkl_path'], fasttext_path = params['default_fasttext_path']):
    word_emb = np.zeros([len(word_dict), params['word_emb_dim']])
    if os.path.isfile(word_emb_pkl_path):
        with open(word_emb_pkl_path, 'rb') as f:
            word_emb = pickle.load(f)
            print('Existed trained word embedding loaded')
    else:
        #load fasttext model
        fasttext_model = FastText.load_fasttext_format(fasttext_path, encoding='utf8')
        print('No word_emb pkl file, start making word_emb ...')
        for word, idx in word_dict.items():
            if idx==0:
                # PAD = 0
                continue
            else:
                try:
                    word_emb[idx] = np.asarray(fasttext_model.wv[word])
                except KeyError:
                    # if there is no word vector for certain word, just assign random vector
                    word_emb[idx] = np.random.uniform(-0.25, 0.25, params['word_emb_dim'])
        with open(word_emb_pkl_path, 'wb') as f:
            pickle.dump(word_emb, f)
        print('Making word_emb ... Done and Saved')
    return word_emb

def zero_padding(token_sentence, word_dict):
    #input : [1,4,3,2,1,15]
    #output : [1,4,3,2,1,15,0,0,0,0]
    padded_sentence = token_sentence + [word_dict[params['PAD']]]*(params['max_seq_length']-len(token_sentence))
    return padded_sentence


def dataset_iterator(filename, word_dict, batch_size):
    #yield batch for training
    with open(filename, 'r', encoding='utf8') as f_dataset:
        context = []
        sequence_length = []
        label = []
        text = f_dataset.read().split('\n')
        for line in text[1:]:
            class_label = [0,0]
            review = line.split('\t')[1]
            polarity = int(line.split('\t')[2])
            class_label[polarity] = 1   #mark polarity
            label.append(class_label)
            tokens = tokenizer.morphs(review)
            #if the review is too long, cut it to adequate length
            if len(tokens) > params['max_seq_length']:
                tokens = tokens[:params['max_seq_length']]
            sentence = [word_dict[word] if word in word_dict else word_dict[params['UNK']] for word in tokens]
            sequence_length.append(len(sentence))
            sentence = zero_padding(sentence, word_dict)
            context.append(sentence)

            if len(context) == batch_size:
                yield (context, sequence_length, label)
                context =[]
                sequence_length = []
                label = []
        if len(context) > 0:
            yield (context, sequence_length, label)