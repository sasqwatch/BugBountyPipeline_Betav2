import configparser
import luigi

from ...helper.command import lc

config = configparser.ConfigParser()


class LinkfinderExecutor(luigi.Task):

    config.read('src/task/config/command.ini')
    command_tpl = config.get('linkfinder', 'command')

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        pass

    def run(self):
        _endpoints: list = []
        _new_endpoints: list = []

        with self.input().open('r') as fp:
            [_endpoints.append(line.rstrip()) for line in fp]

        for _endpoint in _endpoints:
            if str(_endpoint).find(".js") != -1:
                _command = self.command_tpl.replace('**DOMAIN**', _endpoint)
                proc_out = lc(_command.rstrip())
                if proc_out:
                    [_new_endpoints.append(endpoint) for endpoint in proc_out]

        with self.output().open('w') as fp:
            [fp.write(_endpoint.rstrip() + '\n') for _endpoint in _endpoints]

    def output(self):
        raise NotImplemented
