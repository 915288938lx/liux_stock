import tensorflow as tf
from tqdm import tqdm

class seq2seq_with_attention(object):

    def build_inputs(self, config):
        self.seq_inputs = tf.placeholder(shape=(config.batch_size, None), dtype=tf.float32, name='seq_inputs')
        self.seq_inputs_length = tf.placeholder(shape=(config.batch_size,), dtype=tf.int32,name='seq_inputs_length')
        self.seq_targets = tf.placeholder(shape=(config.batch_size, None), dtype=tf.float32, name='seq_targets')
        self.seq_targets_length = tf.placeholder(shape=(config.batch_size,), dtype=tf.int32, name='seq_targets_length')