import configparser
import luigi
import re

from ...helper.command import *
from ...helper.instance import *

config = configparser.ConfigParser()


class SubfinderRemoteExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('subfinder', 'command')
    config_file = config.get('subfinder', 'config_file')

    provider_token: str = ''
    template: str = ''

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _domains: list = []
        _subdomains: list = []

        instance_ip = return_new_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        if not instance_ip:
            raise Exception(f"VM creation failed or IP not assigned")

        conn = get_context(instance_ip, username='root', key_file="src/task/key/terraform_rsa")

        with self.input().open('r') as fp:
            [_domains.append(line.rstrip()) for line in fp]

        for _domain in _domains:
            _command = self.command_tpl.replace('**DOMAIN**', _domain)
            _command = _command.replace('**CONFIG**', self.config_file)
            proc_out = rc(conn, _command.rstrip())
            if proc_out:
                items = proc_out.decode('utf8').split('\n')
                [_subdomains.append(_subdomain) for _subdomain in items
                 if re.findall(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', _subdomain)]

        destroy_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        with self.output().open('w') as fp:
            [fp.write(_sub.rstrip() + '\n') for _sub in _subdomains]

    def output(self):
        raise NotImplemented
