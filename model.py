import tensorflow as tf
from tensorflow.python.ops.rnn_cell import LSTMCell
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn
from hyperparams import params
import pickle

class Model:
    def __init__(self, cfg):

        # fed by 'feed_dict'
        self.context = tf.placeholder(name='context', shape=[None, None], dtype=tf.int32)
        self.seq_len = tf.placeholder(name='sequence_length', shape=[None], dtype=tf.int32)
        self.labels = tf.placeholder(name='labels', shape=[None, cfg.num_classes], dtype=tf.float32)
        self.lr = tf.placeholder(name='learning_rate', dtype=tf.float32)

        with tf.device('/gpu:0'):
            with tf.variable_scope('context_lookup_table'):
                with open(params['default_word_emb_pkl_path'], 'rb') as f:
                    word_emb = pickle.load(f)

                word_embeddings = tf.constant(word_emb, dtype=tf.float32)
                # make lookup table for given review context
                context_emb = tf.nn.embedding_lookup(word_embeddings, self.context)

            with tf.variable_scope('context_representation'):
                cell_fw = LSTMCell(num_units = cfg.num_units)
                cell_bw = LSTMCell(num_units = cfg.num_units)

                h,_ = bidirectional_dynamic_rnn(cell_fw, cell_bw, context_emb, sequence_length=self.seq_len, dtype=tf.float32, time_major=False)
                #concat forward and backward hidden states
                h = tf.concat(h, axis=-1)
                h = self.self_attention(h)
                weight = tf.get_variable(name='weight', shape=[2*cfg.num_units, 2*cfg.num_units], dtype=tf.float32)  ###
                h = tf.nn.tanh(tf.matmul(h, weight))
				
				
            with tf.variable_scope('compute_logits'):
                context_logits = self.ffn_layer(h, cfg.hidden_units, cfg.num_classes, scope='ffn_layer')

            with tf.variable_scope('compute_loss'):
                self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=context_logits, labels=self.labels))
                self.train_op = tf.train.AdamOptimizer(learning_rate=self.lr).minimize(self.loss)

            with tf.variable_scope('accuracy'):
                #pred is 0 (neg) or 1 (pos)
                self.pred = tf.argmax(tf.nn.softmax(context_logits),1,name='prediction')
                num_correct_pred = tf.equal(self.pred, tf.argmax(self.labels, 1))
                self.accuracy = tf.reduce_mean(tf.cast(num_correct_pred, tf.float32))

    def self_attention(self, inputs):
        hidden_size = inputs.shape[2].value
        with tf.variable_scope('self_attn'):
            x_proj = tf.layers.Dense(hidden_size)(inputs)
            x_proj = tf.nn.tanh(x_proj)
            u_w = tf.Variable(tf.random_normal([hidden_size, 1], stddev=0.01, seed=1227))
            x = tf.tensordot(x_proj, u_w, axes=1)
            alphas = tf.nn.softmax(x, axis=1)
            # alphas is row based
            output = tf.matmul(tf.transpose(inputs, [0, 2, 1]), alphas)
            output = tf.squeeze(output, -1)
            return output

    def ffn_layer(self, inputs, hidden_units, output_units, bias_init=0, activation=tf.nn.tanh,
                  scope='ffn_layer'):
        with tf.variable_scope(scope):
            dim = inputs.get_shape().as_list()[-1]
            hidden_weight = tf.get_variable(name='hidden_weight', shape=[dim, hidden_units], dtype=tf.float32)
            hidden_output = tf.matmul(inputs, hidden_weight)
            hidden_bias = tf.get_variable(name='hidden_bias', shape=[hidden_units], dtype=tf.float32,
                                          initializer=tf.constant_initializer(bias_init))
            hidden_output = tf.nn.bias_add(hidden_output, hidden_bias)
            hidden_output = activation(hidden_output)
            hidden_output = tf.nn.dropout(hidden_output, 0.5)

            weight = tf.get_variable(name='weight', shape=[hidden_units, output_units], dtype=tf.float32)
            output = tf.matmul(hidden_output, weight)
            bias = tf.get_variable(name='bias', shape=[output_units], dtype=tf.float32,
                                   initializer=tf.constant_initializer(bias_init))
            output = tf.nn.bias_add(output, bias)
            output = activation(output)

            return output