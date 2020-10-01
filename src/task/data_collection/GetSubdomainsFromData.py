import luigi


class GetSubdomainsFromData(luigi.Task):

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        # Stub for database storage feature
        pass

    def run(self):
        _subdomains: list = []

        for task in self.input():
            with self.input()[task].open('r') as fp:
                [_subdomains.append(line.rstrip()) for line in fp if line not in _subdomains]

        with self.output().open('w') as outfile:
            [outfile.write(domain + '\n') for domain in _subdomains]

    def output(self):
        raise NotImplemented
