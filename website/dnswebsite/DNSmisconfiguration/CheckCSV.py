import re
import csv


class MisconfigurationResult:

    def __init__(self):
        self.misconfiguration_dict = dict()
        self.misconfiguration_count_dict = dict()


class MisconfigurationInfo:

    def __init__(self, server1, server2, foreign_to_server_1, foreign_to_server_2, mutual_to_both_servers, domain):
        self.__foreign_to_server_1 = foreign_to_server_1
        self.__foreign_to_server_2 = foreign_to_server_2
        self.__mutual_to_both_server = mutual_to_both_servers
        self.__domain = domain
        self.__server1 = server1
        self.__server2 = server2

    def __str__(self):
        s = "Misconfiguration information\n"
        s += "Domain: " + str(self.__domain) + "\n"
        s += "Host1: " + str(self.__server1) + "\n"
        s += "Host2: " + str(self.__server2) + "\n"
        f1 = "" if len(self.__foreign_to_server_1) == 0 else str(self.__foreign_to_server_1)
        f2 = "" if len(self.__foreign_to_server_2) == 0 else str(self.__foreign_to_server_2)
        m = "" if len(self.__mutual_to_both_server) == 0 else str(self.__mutual_to_both_server)
        s += "NS known to both servers: " + m + "\n"
        s += "NS known to host1 and not known to host2: " + f1 + "\n"
        s += "NS known to host2 and not known to host1: " + f2 + "\n"
        return s


def read_from_csv(file):
    """
    reads a csv file
    :returns: {generator} the raw data read from the given csv file
    """
    utf8 = (line.decode('utf-8') for line in file)
    file_reader = csv.reader(utf8)
    return file_reader


def convert_key_format(str):
    str = re.sub('[\'()]', '', str)
    hostA, domainA = str.split(',')
    domainA = re.sub(' ', '', domainA)
    return hostA, domainA


def convert_val_format(str):
    str = re.sub('[\'()}{ ]', '', str)
    known_servers = str.split(',')
    return known_servers


def check_csv(misconfiguration_result, file):
    data = read_from_csv(file)
    record_num = 0
    for record_A in data:
        if record_A[0] == "(Server Name, Domain)":
            continue
        record_num += 1
        if record_num % 100 == 0:
            print("record #" + str(record_num))
        host_A, domain_A = convert_key_format(record_A[0])
        if domain_A not in misconfiguration_result.misconfiguration_count_dict:
            misconfiguration_result.misconfiguration_count_dict[domain_A] = 0
        servers_known_to_A = set(convert_val_format(record_A[1]))
        for record_B in data:
            host_B, domain_B = convert_key_format(record_B[0])
            servers_known_to_B = set(convert_val_format(record_B[1]))
            if host_A != host_B and domain_A == domain_B:
                foreign_to_A = servers_known_to_A - servers_known_to_B
                foreign_to_B = servers_known_to_B - servers_known_to_A
                if len(foreign_to_A) > 0 or len(foreign_to_B) > 0:
                    intersection = servers_known_to_A.intersection(servers_known_to_B)
                    misconfiguration_result.misconfiguration_dict[(host_A, host_B, domain_A)] =\
                        MisconfigurationInfo(host_A, host_B, foreign_to_A, foreign_to_B, intersection, domain_A)
                    misconfiguration_result.misconfiguration_count_dict[domain_A] += 1


def storeInCSV(file_name, dict_to_store, field_names):
    """
    stores a dictionary in a CSV format file
    :param file_name: {string} the file's name (must end with .csv)
    :dict_to_store: {dict} a dictionary to store in a CSV file
    :field_names: {list} a list of the dictionary's attributes/fields names
    """
    with open(file_name, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        data = [dict(zip(field_names, [k, v])) for k, v in dict_to_store.items()]
        writer.writerows(data)


def main_known_ns(file):
    misconfiguration_result = MisconfigurationResult()

    check_csv(misconfiguration_result, file)
    # storeInCSV("misconfigurations.csv", misconfiguration_result.misconfiguration_dict, ["server1, server2, domain", "misconfiguration info" ])
    # storeInCSV("misconfigurations_count.csv", misconfiguration_result.misconfiguration_count_dict, ["domain", "num of misconfigurations" ])

    return misconfiguration_result
