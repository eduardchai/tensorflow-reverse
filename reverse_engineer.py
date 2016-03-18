from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import random
import sys
import time
import logging
import numpy as np
from six.moves import xrange

import soraya_data_utils
import config

import tensorflow as tf
from tensorflow.models.rnn.translate import seq2seq_model
from tensorflow.python.platform import gfile

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
_buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]

def create_model(session, forward_only):
	model = seq2seq_model.Seq2SeqModel(
        config.CT_VOCAB_SIZE, config.OP_VOCAB_SIZE, _buckets,
        config.SIZE, config.NUM_LAYERS, config.MAX_GRADIENT_NORM, config.BATCH_SIZE,
        config.LEARNING_RATE, config.LEARNING_RATE_DECAY_FACTOR,
        forward_only=forward_only)

	ckpt = tf.train.get_checkpoint_state(config.TRAIN_DIR)
	
	if ckpt and gfile.Exists(ckpt.model_checkpoint_path):
		model.saver.restore(session, ckpt.model_checkpoint_path)
	else:
		session.run(tf.initialize_all_variables())
	
	return model

def train():
	ct_train, op_train, ct_dev, op_dev, _, _ = soraya_data_utils.prepare_conversation_data(
      config.DATA_DIR, config.CT_VOCAB_SIZE, config.OP_VOCAB_SIZE)

	with tf.Session() as sess:
		model = create_model(sess, False)

def main(_):
	train()

if __name__ == "__main__":
    tf.app.run()