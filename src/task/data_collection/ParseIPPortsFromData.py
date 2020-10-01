import luigi


class ParseIPPortsFromData(luigi.Task):

    def requires(self):
        raise NotImplemented

    def store(self, data: dict):
        # Stub for database storage feature
        pass

    def run(self):
        _ip_pairs: dict = {}
        _ip_addresses: list = []
        _port_addresses: list = []

        with self.input().open('r') as infile:
            for line in infile:
                if line.rstrip().startswith('Timestamp'):
                    parts = line.rstrip().split()
                    ip = parts[3]
                    port = parts[-1].split('/')[0]
                    _ip_addresses.append(ip)
                    _port_addresses.append(port)

        if _ip_addresses:
            _ip_addresses = list(set(_ip_addresses))

        if _port_addresses:
            _port_addresses = list(set(_port_addresses))

        with self.output()['port_addresses'].open('w') as outfile:
            [outfile.write(domain + '\n') for domain in _port_addresses]

        with self.output()['ip_addresses'].open('w') as outfile:
            [outfile.write(ip_address + '\n') for ip_address in _ip_addresses]

    def output(self):
        raise NotImplemented
