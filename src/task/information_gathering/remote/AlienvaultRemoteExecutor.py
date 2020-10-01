import configparser
import luigi

from ...helper.command import *
from ...helper.instance import *

config = configparser.ConfigParser()


class AlienvaultRemoteExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('alienvault', 'command')
    api_key = config.get('alienvault', 'api_key')

    provider_token: str = ''
    template: str = ''

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _endpoints: list = []
        _domains: list = []

        instance_ip = return_new_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        if not instance_ip:
            raise Exception(f"VM creation failed or IP not assigned")

        conn = get_context(instance_ip, username='root', key_file="src/task/key/terraform_rsa")

        for task in self.input():
            if task == 'subdomains':
                with self.input()['subdomains'].open('r') as fp:
                    [_domains.append(line.rstrip()) for line in fp]

        for _domain in _domains:
            _command = self.command_tpl.replace('**DOMAIN**', _domain)
            _command = _command.replace('**APIKEY**', self.api_key)
            proc_out = rc(conn, _command.rstrip())
            if proc_out:
                items = proc_out.decode('utf8').split('\n')
                [_endpoints.append(url) for url in items if url.startswith('http')]

        if _endpoints:
            _endpoints = list(set(_endpoints))

        destroy_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        with self.output().open('w') as fp:
            [fp.write(_sub.rstrip() + '\n') for _sub in _endpoints]

    def output(self):
        raise NotImplemented
