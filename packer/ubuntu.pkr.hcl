################################################################################
# ubuntu.pkr.hcl
# VirtualBox OVA builder – Ubuntu 22.04 LTS
# Packer >= 1.10 (HCL2)
#
# Usage:
#   packer init   packer/
#   packer build  packer/
#
# The resulting OVA is written to  packer/output-ansible-openstack-lab/
################################################################################

packer {
  required_version = ">= 1.10.0"
  required_plugins {
    virtualbox = {
      version = ">= 1.1.1"
      source  = "github.com/hashicorp/virtualbox"
    }
  }
}

##############################################################################
# Variables – override via  -var 'key=value'  or  packer.auto.pkrvars.hcl
##############################################################################
variable "vm_name" {
  default = "ansible-openstack-lab"
}

variable "vm_memory_mb" {
  default = "4096"
}

variable "vm_cpus" {
  default = "2"
}

variable "disk_size_mb" {
  default = "40960"
}

variable "iso_url" {
  # Ubuntu 22.04.4 LTS (Jammy) server ISO
  default = "https://releases.ubuntu.com/22.04/ubuntu-22.04.4-live-server-amd64.iso"
}

variable "iso_checksum" {
  default = "sha256:45f873de9f8cb637345d6e66a583762730bbea30277ef7b32c9c3bd6700a32b2"
}

variable "ssh_username" {
  default = "ansible"
}

variable "ssh_password" {
  default = "ansible"
}

##############################################################################
# Source – VirtualBox ISO boot
##############################################################################
source "virtualbox-iso" "ubuntu" {
  vm_name       = var.vm_name
  guest_os_type = "Ubuntu_64"
  memory        = var.vm_memory_mb
  cpus          = var.vm_cpus
  disk_size     = var.disk_size_mb

  iso_url      = var.iso_url
  iso_checksum = var.iso_checksum

  # Ubuntu 22.04 live-server uses subiquity / cloud-init autoinstall
  http_directory = "${path.root}/http"
  boot_wait      = "5s"
  boot_command = [
    "c<wait>",
    "linux /casper/vmlinuz --- autoinstall ds=nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/<wait>",
    "<enter><wait>",
    "initrd /casper/initrd<wait>",
    "<enter><wait>",
    "boot<enter>"
  ]

  shutdown_command = "echo '${var.ssh_password}' | sudo -S shutdown -P now"

  communicator           = "ssh"
  ssh_username           = var.ssh_username
  ssh_password           = var.ssh_password
  ssh_timeout            = "30m"
  ssh_handshake_attempts = 100

  # Export settings
  format           = "ova"
  output_directory = "${path.root}/output-${var.vm_name}"
  export_opts = [
    "--manifest",
    "--vsys", "0",
    "--description", "Ansible + OpenStack Private Cloud Lab VM",
    "--version", "1.0"
  ]

  # VirtualBox Guest Additions
  guest_additions_mode = "disable"

  vboxmanage = [
    ["modifyvm", "{{.Name}}", "--nat-localhostreachable1", "on"],
    ["modifyvm", "{{.Name}}", "--audio", "none"],
    ["modifyvm", "{{.Name}}", "--usb", "off"]
  ]
}

##############################################################################
# Build
##############################################################################
build {
  sources = ["source.virtualbox-iso.ubuntu"]

  # 1. Wait until cloud-init finishes
  provisioner "shell" {
    inline = [
      "sudo cloud-init status --wait || true"
    ]
    pause_before = "10s"
  }

  # 2. Core provisioning: Python, Ansible, repo content
  provisioner "shell" {
    script          = "${path.root}/scripts/provision.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
    environment_vars = [
      "ANSIBLE_USER=${var.ssh_username}"
    ]
  }

  # 3. Copy repository content into the VM
  provisioner "file" {
    source      = "${path.root}/../"
    destination = "/opt/ansible-openstack"
    generated   = false
  }

  # 4. Post-copy setup (fix ownership, offline pip wheel cache)
  provisioner "shell" {
    script          = "${path.root}/scripts/post_copy.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
    environment_vars = [
      "ANSIBLE_USER=${var.ssh_username}"
    ]
  }

  # 5. Cleanup to reduce OVA size
  provisioner "shell" {
    script          = "${path.root}/scripts/cleanup.sh"
    execute_command = "echo '${var.ssh_password}' | sudo -S bash '{{.Path}}'"
  }
}
