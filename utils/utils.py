import re
from bin.parser import Parser


def write_sorted_grouped_transactions_to_file():
    df = Parser('../data/test_task_2_logs.log').group_by_transactions()
    f = open('groups.txt', 'w')
    print('rows after grouping = ' + str(df.size().size))
    for i in sorted(df.groups.items(), key=lambda x: x[0]):
        f.write(re.sub(r'(\w+)\s\/(.*)', r'\2', i[0] + '\n'))


if __name__ == '__main__':
    write_sorted_grouped_transactions_to_file()
