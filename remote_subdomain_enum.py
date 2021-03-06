import luigi

from luigi.util import inherits
# from luigi.contrib.s3 import S3Target
from src.task.data_collection import *
from src.task.helper.token import generate_token
from src.task.information_gathering.remote import *

_provider_token = '<digitalocean api_key>'


class _GetDataFromSource(GetDataFromSource.GetDataFromSource):

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-GetDataFromSource-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _GetDomainsFromData(GetDomainsFromData.GetDomainsFromData):

    def requires(self):
        return _GetDataFromSource(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-GetDomainsFromData-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _ChaosExecutorTask(ChaosRemoteExecutor.ChaosRemoteExecutor):

    provider_token = _provider_token
    template = f'src/task/information_gathering/remote/templates/digitalocean/chaos'

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-ChaosExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _AssetfinderExecutorTask(AssetfinderRemoteExecutor.AssetfinderRemoteExecutor):

    provider_token = _provider_token
    template = f'src/task/information_gathering/remote/templates/digitalocean/assetfinder'

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-AssetfinderExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _SubfinderExecutorTask(SubfinderRemoteExecutor.SubfinderRemoteExecutor):

    provider_token = _provider_token
    template = f'src/task/information_gathering/remote/templates/digitalocean/subfinder'

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-SubfinderExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _Sublist3rExecutorTask(Sublist3rRemoteExecutor.Sublist3rRemoteExecutor):

    provider_token = _provider_token
    template = f'src/task/information_gathering/remote/templates/digitalocean/sublist3r'

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-Sublist3rExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _AmassExecutorTask(AmassRemoteExecutor.AmassRemoteExecutor):

    provider_token = _provider_token
    template = f'src/task/information_gathering/remote/templates/digitalocean/amass'

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-AmassExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _GetSubdomainsFromData(GetSubdomainsFromData.GetSubdomainsFromData):

    def requires(self):
        return {
            'task_a': _AmassExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source),
            'task_b': _AssetfinderExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source),
            'task_c': _ChaosExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source),
            'task_d': _SubfinderExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source),
            'task_e': _Sublist3rExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source)
        }

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-GetSubdomainsFromData-{self.nonce_token}.complete')


if __name__ == '__main__':
    token: str = generate_token()
    data_source: str = '/tmp/targets.txt'
    luigi.build([_GetSubdomainsFromData(nonce_token=token, data_source=data_source)], local_scheduler=True, workers=5)
