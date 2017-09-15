import re
import os
import pandas as pd
import argparse


class Parser:
    def __init__(self, filename):
        data = self.read_log(filename)
        self.dataframe = self.replace_dynamic_data(data)

    @staticmethod
    def get_total_hits(dataframe):
        return dataframe.shape[0]

    @staticmethod
    def get_total_hits_for_each_transaction(dataframe):
        total_hits = {}
        for i in dataframe.groups:
            total_hits[i] = dataframe.groups[i].size
        return total_hits

    @staticmethod
    def read_log(logname):
        regexp = re.compile(
            r"x{1,3}\.x{1,3}\.x{1,3}\.x{1,3}\s\-\s\-\s\[((\d{2}\/(?i)\w{3}\/\d{4})\:(\d{2}\:\d{2}\:\d{2}))"
            r"\s(\+\d{4})\]\s\"(\w+\s\/.*)\s(HTTP\/1.\d)\"\s(\d{3})\s(\d+)\s\"(.+)\"\s\"(.+)\"")
        with open(logname) as log:
            data = regexp.findall(log.read())
        return data

    @staticmethod
    def get_transaction_name_for_regex(filename):
        with open(filename) as f:
            data_for_regex = f.read().splitlines()
        return data_for_regex

    def replace_dynamic_data(self, data):
        regex = {r'(\w+) /(.*/?)\?(.*)': r'\1 /\2?XXXXXX'}
        data_for_regex = self.get_transaction_name_for_regex(os.path.dirname(__file__)+'/../data/regex.txt')
        for i in data_for_regex:
            regex[r'(\w+) /{0}/(.*)'.format(i)] = r'\1 /{0}/XXXXXX'.format(i)
        df = pd.DataFrame(data, columns=['datetime', 'date', 'time', 'timezone', 'transaction', 'http_version',
                                         'status_code', 'response_time', 'url', 'user_agent'])
        for i in regex:
            df["transaction"] = df["transaction"].replace({i: regex[i]}, regex=True)
        return df

    def group_by_transactions(self):
        df = self.dataframe
        return df.groupby(["transaction"])

    def group_by_minute(self, dataframe):
        df = dataframe
        df.index = pd.to_datetime(df['datetime'], format="%d/%b/%Y:%H:%M:%S")
        grouped_df = df.groupby([df.index.map(lambda t: t.year), df.index.map(lambda t: t.month),
                                 df.index.map(lambda t: t.day), df.index.map(lambda t: t.hour),
                                 df.index.map(lambda t: t.minute)])
        return grouped_df

    def get_max_rpm_for_all_transactions(self):
        return self.group_by_minute(self.dataframe).size().values.max()

    def show_rpm_for_all_transactions(self):
        print('max_tpm_all_transactions = ' + str(self.get_max_rpm_for_all_transactions()) + '\n')

    def get_max_rpm_for_each_transaction(self, dataframe):
        max_rpm = {}
        for i in dataframe.groups:
            grouped_by_minute = self.group_by_minute(dataframe.get_group(i))
            max_rpm[i] = grouped_by_minute.size().values.max()
        return max_rpm

    def show_top_n_popular_transactions(self, n):
        dataframe = self.dataframe
        grouped = self.group_by_transactions()
        max_rpm_for_each_transaction = self.get_max_rpm_for_each_transaction(grouped)
        total_hits_each = self.get_total_hits_for_each_transaction(grouped)
        total_hits = self.get_total_hits(dataframe)
        number_to_show = n
        k = 0
        sorted_max_rpm_for_each_transaction = sorted(max_rpm_for_each_transaction.items(), key=lambda x: x[1],
                                                     reverse=True)
        for j, i in enumerate(sorted_max_rpm_for_each_transaction):
            transaction_title = i[0]
            print(transaction_title)
            print('total_hits = ' + str(total_hits_each[transaction_title]) + ', percentage = ' +
                  str(round(total_hits_each[transaction_title] / total_hits * 100, 2)) + '%, max_tpm = ' +
                  str(max_rpm_for_each_transaction[transaction_title]) + '\n')
            if j == number_to_show - 1:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', nargs='?', type=str, help="path to log file to parse",
                        default='./data/test_task_2_logs.log')
    parser.add_argument('--not', nargs='?', type=int, help="number of transactions to display",
                        default=25)
    args = parser.parse_args()
    p = Parser(args.path)
    p.show_rpm_for_all_transactions()
    p.show_top_n_popular_transactions(args.nof)
