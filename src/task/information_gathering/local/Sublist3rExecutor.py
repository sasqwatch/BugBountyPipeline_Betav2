import configparser
import luigi
import re

from ...helper.command import lc

config = configparser.ConfigParser()


class Sublist3rExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('sublist3r', 'command')

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _domains: list = []
        _subdomains: list = []

        with self.input().open('r') as fp:
            [_domains.append(line.rstrip()) for line in fp]

        for _domain in _domains:
            _command = self.command_tpl.replace('**DOMAIN**', _domain)
            proc_out = lc(_command.rstrip())
            if proc_out:
                [_subdomains.append(_subdomain) for _subdomain in proc_out
                 if re.findall(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', _subdomain)]

        with self.output().open('w') as fp:
            [fp.write(_sub.rstrip() + '\n') for _sub in _subdomains]

    def output(self):
        raise NotImplemented
