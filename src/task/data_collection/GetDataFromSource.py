import luigi

from pathlib import Path
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class GetDataFromSource(luigi.Task):

    nonce_token: str = luigi.Parameter()
    data_source: str = luigi.Parameter()

    def store(self, data: dict):
        # Stub for database storage feature
        pass

    def run(self):
        _items: list = []

        if Path(self.data_source).is_file():
            with open(self.data_source, 'r') as fp:
                [_items.append(line.rstrip()) for line in fp]
        elif self.data_source.startswith('http'):
            with Session() as session:
                retry = Retry(connect=2, backoff_factor=0.25, status_forcelist=[429, 504])
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter=adapter)
                session.mount('https://', adapter=adapter)
                response_data = session.get(self.data_source).text
                for line in response_data.split('\n'):
                    _items.append(line)
        else:
            _items.append(self.data_source)

        with self.output().open('w') as outfile:
            [outfile.write(item + '\n') for item in _items]

    def output(self):
        raise NotImplemented
