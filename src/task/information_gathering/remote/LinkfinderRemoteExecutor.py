import configparser
import luigi

from ...helper.command import *
from ...helper.instance import *

config = configparser.ConfigParser()


class LinkfinderRemoteExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('linkfinder', 'command')

    provider_token: str = ''
    template: str = ''

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _endpoints: list = []
        _new_endpoints: list = []

        instance_ip = return_new_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        if not instance_ip:
            raise Exception(f"VM creation failed or IP not assigned")

        conn = get_context(instance_ip, username='root', key_file="src/task/key/terraform_rsa")

        with self.input().open('r') as fp:
            [_endpoints.append(line.rstrip()) for line in fp]

        for _endpoint in _endpoints:
            if str(_endpoint).find(".js") != -1:
                _command = self.command_tpl.replace('**DOMAIN**', _endpoint)
                proc_out = rc(conn, _command.rstrip())
                if proc_out:
                    items = proc_out.decode('utf8').split('\n')
                    [_new_endpoints.append(endpoint) for endpoint in items]

        destroy_instance(
            self.provider_token.__str__(),
            self.template.__str__()
        )

        with self.output().open('w') as fp:
            [fp.write(_endpoint.rstrip() + '\n') for _endpoint in _endpoints]

    def output(self):
        raise NotImplemented
