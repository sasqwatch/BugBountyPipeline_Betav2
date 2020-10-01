terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "1.22.2"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

variable "do_token" {}

resource "random_string" "random" {
  length = 16
  special = false
}

resource "tls_private_key" "temp_pvt_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "digitalocean_ssh_key" "ssh_key" {
  name = random_string.random.result
  public_key = tls_private_key.temp_pvt_key.public_key_openssh
}

resource "digitalocean_droplet" "task-masscan" {
  depends_on = [tls_private_key.temp_pvt_key]

  image = "ubuntu-18-04-x64"
  name = "task-masscan"
  region = "nyc3"
  size = "s-1vcpu-1gb"
  private_networking = true
  ssh_keys = [digitalocean_ssh_key.ssh_key.id]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = tls_private_key.temp_pvt_key.private_key_pem
    timeout = "2m"
  }

  provisioner "file" {
    source = "/tmp/resolvers.txt"
    destination = "/tmp/resolvers.txt"
  }

  provisioner "file" {
    source = "/home/d3d/.ssh/terraform_rsa.pub"
    destination = "/tmp/key.pub"
  }

  provisioner "remote-exec" {
    inline = [
      "export PATH=$PATH:/usr/bin",
      "apt-get update && apt-get upgrade -y",
      "apt-get install git -y",
      "apt-get install make -y",
      "apt-get install gcc -y",
      "apt-get install libpcap-dev -y",
      "git clone https://github.com/robertdavidgraham/masscan /tmp/masscan",
      "cd /tmp/masscan && make && cp /tmp/masscan/bin/masscan /usr/bin",
      "cat /tmp/key.pub >> /root/.ssh/authorized_keys",
      "touch /tmp/task.complete"
    ]
  }
}

output "web_ipv4_address" {
  description = "List of IPv4 addresses of web Droplets"
  value       = digitalocean_droplet.task-masscan.ipv4_address
}