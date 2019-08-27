import tushare as ts
import sqlite3
import logging
code="000002"
start = "2008-01-01"
end = "2019-08-22"

def iter_dataFrame():
    stock_frame = ts.get_k_data(code, start, end)
    for index in stock_frame.index:
        stock_row = stock_frame.loc[index]
        yield stock_row

iters = iter_dataFrame()
def create_table():
    global creat_table_sql

    db_connection = sqlite3.connect('./stocks.db')
    with db_connection:
        creat_table_sql = """CREATE TABLE IF NOT EXISTS %s (dates DATE , open FLOAT , close FLOAT , high FLOAT , low FLOAT , volume FLOAT , code TEXT )""" % code_table_name
        db_connection.execute(creat_table_sql)

        db_connection.executemany("INSERT INTO %s VALUES (?,?,?,?,?,?,?)"%code_table_name,iters)
    db_connection.commit()

if __name__ == '__main__':
    logging.warning('start to crawling code: {}'.format(code))
    db_connection = sqlite3.connect('./stocks.db')
    code_table_name = "代码" + code
    table_names = db_connection.execute(
        """SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name""").fetchall()

    try:
        table_names_list = [x[0] for x in table_names]  # 如果列表不报超出下标的错误
    except:  # 如果报错，那么说明从未创建过表，则开始创建数据库表
        print('创建数据库表...')
        create_table()
    else:  # 否则说明不报超出下标的错误，既数据库里有数据表，还需要判断今天的表是否存在过
        if code_table_name not in table_names_list:
            create_table()
        else:
            print('数据库中表名为“%s”的表已存在！' % code_table_name)
            re_run_programs = input('如需覆盖今天所生成表，请输入yes并按回车:')
            if re_run_programs == 'yes':
                db_connection.execute('drop TABLE %s' % code_table_name)
                db_connection.commit()
                create_table()
    create_table()