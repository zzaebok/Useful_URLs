import os.path
import tensorflow as tf
from konlpy.tag import Okt
import pickle
import numpy as np
from hyperparams import params
from data_helper import *

word_dict = []
with open(params['default_word_dict_pkl_path'], 'rb') as f:
    word_dict = pickle.load(f)
word_emb = np.zeros([len(word_dict), 200])
with open(params['default_word_emb_pkl_path'], 'rb') as f:
    word_emb = pickle.load(f)
tokenizer = Okt()
SAVER_DIR = params['SAVER_DIR']

#load pre trained model
saver = tf.train.import_meta_graph(os.path.join(SAVER_DIR, 'ckpt.meta'))
ckpt = tf.train.get_checkpoint_state(SAVER_DIR)
config = tf.ConfigProto(allow_soft_placement=True)
sess = tf.Session(config=config)
saver.restore(sess, ckpt.model_checkpoint_path)
graph = sess.graph
#print([node.name for node in graph.as_graph_def().node]) - for checking all the variables in model
model_context = graph.get_tensor_by_name('context:0')
model_seq_len = graph.get_tensor_by_name('sequence_length:0')
model_labels = graph.get_tensor_by_name('labels:0')
model_pred = graph.get_tensor_by_name('accuracy/prediction:0')
while(1):
    sentence = input('문장을 입력해주세요. (그만하려면 z 입력)')
    if sentence == 'z':
        break
    context = []
    sequence_length = []
    tokens = tokenizer.morphs(sentence)
    sentence = [word_dict[word] if word in word_dict else word_dict['<unk>'] for word in tokens]
    sequence_length.append(len(tokens))
    sentence = zero_padding(sentence, word_dict)
    context = [sentence]
    prediction = sess.run(model_pred, feed_dict={model_context: context, model_seq_len: sequence_length})
    if prediction == 0:
        print('부정입니다.')
    else:
        print('긍정입니다.')
