import configparser
import luigi

from ...helper.scp import *
from ...helper.command import *
from ...helper.instance import *

config = configparser.ConfigParser()


class MassdnsRemoteExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('massdns', 'command')

    provider_token: str = ''
    template: str = ''

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _subdomains: list = []
        _dns_records: list = []

        instance_ip = return_new_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        if not instance_ip:
            raise Exception(f"VM creation failed or IP not assigned")

        conn = get_context(instance_ip, username='root', key_file="src/task/key/terraform_rsa")

        with self.input().open('r') as infile:
            [_subdomains.append(line.rstrip()) for line in infile]

        with open('/tmp/.massdns.subdomains.txt', 'w') as fp:
            [fp.write(_subdomain.rstrip() + '\n') for _subdomain in _subdomains]

        copy_to_host(instance_ip, 'root', 'src/task/key/terraform_rsa',
                     '/tmp/.massdns.subdomains.txt', '/tmp/.massdns.subdomains.txt')

        proc_out = rc(conn, self.command_tpl.rstrip())
        if proc_out:
            items = proc_out.decode('utf8').split('\n')
            [_dns_records.append(_record) for _record in items if len(_record.strip().split(' ')) == 3]

        destroy_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        with self.output().open('w') as outfile:
            [outfile.write(_record.rstrip() + '\n') for _record in _dns_records]

    def output(self):
        raise NotImplemented
