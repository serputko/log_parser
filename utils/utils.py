from bin.parser import *


def write_sorted_grouped_transactions_to_file(dataframe):
    df = group_by_transactions(dataframe)
    f = open('groups.txt', 'w')
    print('rows after grouping = ' + str(df.size().size))
    for i in sorted(df.groups.items(), key=lambda x: x[0]):
        f.write(re.sub(r'(\w+)\s\/(.*)', r'\2', i[0]+'\n'))


if __name__ == '__main__':
    data = read_log('../bin/test_task_2_logs.log')
    dataframe = replace_dynamic_data(data)
    write_sorted_grouped_transactions_to_file(dataframe)