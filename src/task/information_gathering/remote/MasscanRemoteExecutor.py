import configparser
import luigi

from ...helper.scp import *
from ...helper.command import *
from ...helper.instance import *

config = configparser.ConfigParser()


class MasscanRemoteExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('masscan', 'command')

    provider_token: str = ''
    template: str = ''

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _results: list = []
        _ip_addresses: list = []

        instance_ip = return_new_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        if not instance_ip:
            raise Exception(f"VM creation failed or IP not assigned")

        conn = get_context(instance_ip, username='root', key_file="src/task/key/terraform_rsa")

        for task in self.input():
            if task == 'ip_addresses':
                with self.input()['ip_addresses'].open('r') as infile:
                    [_ip_addresses.append(line.rstrip()) for line in infile]

        with open('/tmp/.masscan.in', 'w') as fp:
            [fp.write(_ip_address.rstrip() + '\n') for _ip_address in _ip_addresses]

        copy_to_host(instance_ip, 'root', 'src/task/key/terraform_rsa', '/tmp/.masscan.in', '/tmp/.masscan.in')

        proc_out = rc(conn, self.command_tpl.rstrip())
        if proc_out:
            items = proc_out.decode('utf8').split('\n')
            [_results.append(line.rstrip('\n')) for line in items if '/open/' in line]

        destroy_instance(
           self.provider_token.__str__(),
           self.template.__str__()
        )

        with self.output().open('w') as outfile:
            [outfile.write(_result.rstrip() + '\n') for _result in _results]

    def output(self):
        raise NotImplemented
