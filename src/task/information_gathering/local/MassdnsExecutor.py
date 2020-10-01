import configparser
import luigi

from ...helper.command import lc

config = configparser.ConfigParser()


class MassdnsExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('massdns', 'command')

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _subdomains: list = []
        _dns_records: list = []

        with self.input().open('r') as infile:
            [_subdomains.append(line.rstrip()) for line in infile]

        with open('/tmp/.massdns.subdomains.txt', 'w') as fp:
            [fp.write(_subdomain.rstrip() + '\n') for _subdomain in _subdomains]

        proc_out = lc(self.command_tpl.rstrip())
        if proc_out:
            [_dns_records.append(_record) for _record in proc_out if len(_record.strip().split(' ')) == 3]

        with self.output().open('w') as outfile:
            [outfile.write(_record.rstrip() + '\n') for _record in _dns_records]

    def output(self):
        raise NotImplemented
