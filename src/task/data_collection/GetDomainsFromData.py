import tldextract
import luigi
import re


class GetDomainsFromData(luigi.Task):

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        # Stub for database storage feature
        pass

    def run(self):
        _domains: list = []
        _tld_domains: list = []

        with self.input().open('r') as infile:
            [_domains.append(line) for line in infile if re.findall(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', line)]

        if _domains:
            for _domain in _domains:
                domain_parts = tldextract.extract(_domain)
                tld_domain = f'{domain_parts.domain}.{domain_parts.suffix}'
                if tld_domain in _tld_domains:
                    continue
                _tld_domains.append(tld_domain)

        with self.output().open('w') as outfile:
            [outfile.write(domain + '\n') for domain in _tld_domains]

    def output(self):
        raise NotImplemented
