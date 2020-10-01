import luigi

from luigi.util import inherits
# from luigi.contrib.s3 import S3Target
from src.task.data_collection import *
from src.task.helper.token import generate_token
from src.task.information_gathering.local import *


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
class _ChaosExecutorTask(ChaosExecutor.ChaosExecutor):

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-ChaosExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _AssetfinderExecutorTask(AssetfinderExecutor.AssetfinderExecutor):

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-AssetfinderExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _SubfinderExecutorTask(SubfinderExecutor.SubfinderExecutor):

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-SubfinderExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _Sublist3rExecutorTask(Sublist3rExecutor.Sublist3rExecutor):

    def requires(self):
        return _GetDomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-Sublist3rExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _AmassExecutorTask(AmassExecutor.AmassExecutor):

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


@luigi.util.inherits(_GetDataFromSource)
class _MassdnsExecutorTask(MassdnsExecutor.MassdnsExecutor):

    def requires(self):
        return _GetSubdomainsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-MassdnsExecutorTask-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _ParseHostsFromData(ParseHostsFromData.ParseHostsFromData):

    def requires(self):
        return _MassdnsExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return {
            'ip_addresses': luigi.LocalTarget(f'/tmp/recon-ParseHostsFromData-IPs-{self.nonce_token}.complete'),
            'subdomains': luigi.LocalTarget(f'/tmp/recon-ParseHostsFromData-Subdomains-{self.nonce_token}.complete'),
        }


@luigi.util.inherits(_GetDataFromSource)
class _MasscanExecutorTask(MasscanExecutor.MasscanExecutor):

    def requires(self):
        return _ParseHostsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-MasscanExecutor-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _NmapExecutorTask(NmapExecutor.NmapExecutor):

    def requires(self):
        return _ParseHostsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-NmapExecutor-{self.nonce_token}.complete')


'''
@luigi.util.inherits(_GetDataFromSource)
class _AlienvaultExecutorTask(AlienvaultExecutor.AlienvaultExecutor):

    def requires(self):
        return _ParseHostsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-AlienvaultExecutor-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _WaybackurlsExecutorTask(WaybackurlsExecutor.WaybackurlsExecutor):

    def requires(self):
        return _ParseHostsFromData(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-Waybackurls-executor-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _ParseIPPortsFromData(ParseIPPortsFromData.ParseIPPortsFromData):

    def requires(self):
        return _MasscanExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source)

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-ParseIPPortsFromData-{self.nonce_token}.complete')


@luigi.util.inherits(_GetDataFromSource)
class _GetEndpointsFromData(GetEndpointsFromData.GetEndpointsFromData):

    def requires(self):
        return {
            'task_a': _AlienvaultExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source),
            'task_b': _WaybackurlsExecutorTask(nonce_token=self.nonce_token, data_source=self.data_source)
        }

    def output(self):
        return luigi.LocalTarget(f'/tmp/recon-GetEndpointsFromData-{self.nonce_token}.complete')
'''

if __name__ == '__main__':
    token: str = generate_token()
    data_source: str = '/tmp/targets.txt'
    luigi.build(
        [
            _MasscanExecutorTask(nonce_token=token, data_source=data_source),
            _NmapExecutorTask(nonce_token=token, data_source=data_source),
        ],
        local_scheduler=True, workers=5)
