from data_handle.stock_spider import code,start,end
import sqlite3
import numpy as np
from sklearn.preprocessing import StandardScaler




train_data_ratio = 0.8
split_index =int(len(data_scaled)*train_data_ratio) # 2140
batch_size = 64
encoder_sequence_length = 20
decoder_sequence_length = 20

def get_scaled_data():
    global data_scaled
    code_table_name = "代码" + code
    db_connection = sqlite3.connect('./stocks.db')
    data = db_connection.execute("SELECT * FROM %s" % code_table_name)
    li = []
    for i in data:
        five_dims = i[1:6]
        li.append(five_dims)
    data_numpy = np.array(li)  # len()=2675
    scaler = StandardScaler()
    scaler.fit(data_numpy)
    data_scaled = scaler.transform(data_numpy)
    return data_scaled


def get_data_set_and_min_max_index(train_data):
    if train_data == "train_data":
        data_set = data_scaled[:split_index, :]
        min_start_index = 0
        max_end_index = split_index - encoder_sequence_length - decoder_sequence_length
    else:
        data_set = data_scaled[split_index:, :]
        min_start_index = split_index
        max_end_index = len(data_scaled) - encoder_sequence_length - decoder_sequence_length
    return data_set,min_start_index,max_end_index



def get_batch_sequence(data,min_start_index,max_random_index):
    batch_source_sequence = []
    batch_target_sequence = []
    for _ in range(batch_size):
        random_index = np.random.randint(min_start_index, max_random_index)
        source_sequence = data[random_index:(random_index + encoder_sequence_length), :]
        target_sequence = data[(random_index + encoder_sequence_length):(random_index + decoder_sequence_length), :]
        batch_source_sequence.append(source_sequence)
        batch_target_sequence.append(target_sequence)
    batch_source_sequence = np.array(batch_source_sequence)
    batch_target_sequence = np.array(batch_target_sequence)
    return batch_source_sequence,batch_target_sequence
