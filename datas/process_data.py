from datas.stock_spider import code,start,end
import sqlite3
import numpy as np
from sklearn.preprocessing import StandardScaler

code_table_name = "代码"+code
db_connection = sqlite3.connect('./stocks.db')
data = db_connection.execute("SELECT * FROM %s"%code_table_name)


li = []
for i in data:
    five_dims = i[1:6]
    li.append(five_dims)
data_numpy = np.array(li) # len()=2675
scaler = StandardScaler()
scaler.fit(data_numpy)
data_scaled = scaler.transform(data_numpy)
# return data_scaled


train_data_ratio = 0.8
split_index =int(len(data_scaled)*train_data_ratio) # 2140
batch_size = 64
encoder_sequence_length = 20
decoder_sequence_length = 20
generate_times = 20000

max_random_index = split_index-encoder_sequence_length
one_sequence = 






print()