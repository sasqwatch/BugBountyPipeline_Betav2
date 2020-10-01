import paramiko


def copy_to_host(host: str, username: str, key_file: str, src: str, dest: str):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=host,
        username=username,
        key_filename=key_file
    )
    sftp_client = ssh_client.open_sftp()
    sftp_client.put(src, dest)
    sftp_client.close()
