import configparser
import luigi

from ...helper.command import lc

config = configparser.ConfigParser()


class NmapExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('nmap', 'command')

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _results: list = []
        _ip_addresses: list = []

        for task in self.input():
            if task == 'ip_addresses':
                with self.input()['ip_addresses'].open('r') as infile:
                    [_ip_addresses.append(line.rstrip()) for line in infile]

        with open('/tmp/.nmap.in', 'w') as fp:
            [fp.write(_ip_address.rstrip() + '\n') for _ip_address in _ip_addresses]

        proc_out = lc(self.command_tpl.rstrip())
        if proc_out:
            [_results.append(line.rstrip('\n')) for line in proc_out if line.startswith('Host:') and '/open/' in line]

        with self.output().open('w') as outfile:
            [outfile.write(_result.rstrip() + '\n') for _result in _results]

    def output(self):
        raise NotImplemented
