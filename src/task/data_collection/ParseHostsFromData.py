import luigi


class ParseHostsFromData(luigi.Task):

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        # Stub for database storage feature
        pass

    def run(self):
        _subdomains: list = []
        _ip_addresses: list = []

        with self.input().open('r') as infile:
            for line in infile:
                if len(line.strip().split()) == 3 and ' A ' in line:
                    domain, record, ip = line.split()
                    domain = domain.rstrip('.')
                    _subdomains.append(domain)
                    _ip_addresses.append(ip)

        with self.output()['subdomains'].open('w') as outfile:
            [outfile.write(domain + '\n') for domain in _subdomains]

        with self.output()['ip_addresses'].open('w') as outfile:
            [outfile.write(ip_address + '\n') for ip_address in _ip_addresses]

    def output(self):
        raise NotImplemented
