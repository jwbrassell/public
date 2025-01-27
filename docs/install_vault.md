# HashiCorp Vault Installation and Configuration Guide for Rocky Linux

## Prerequisites
- Rocky Linux (any recent version)
- Root or sudo access
- Internet connection for package installation

## 1. Install Required Packages

```bash
# Add HashiCorp repository
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

# Install Vault
sudo yum -y install vault
```

## 2. Create Vault Directory Structure

```bash
# Create necessary directories
sudo mkdir -p /opt/vault/data
sudo mkdir -p /opt/vault/config
sudo chown -R vault:vault /opt/vault
```

## 3. Configure Vault Server

Create the configuration file:
```bash
sudo nano /opt/vault/config/vault.hcl
```

Add the following configuration:
```hcl
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = 1
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "http://127.0.0.1:8201"

ui = false
disable_mlock = true
```

## 4. Create Systemd Service

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/vault.service
```

Add the following content:
```ini
[Unit]
Description=HashiCorp Vault Service
Documentation=https://www.vaultproject.io/docs/
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
User=vault
Group=vault
ExecStart=/usr/bin/vault server -config=/opt/vault/config/vault.hcl
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
KillSignal=SIGINT
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
StartLimitInterval=60
StartLimitBurst=3
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## 5. Start and Enable Vault Service

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Start Vault service
sudo systemctl start vault

# Enable Vault to start on boot
sudo systemctl enable vault

# Check status
sudo systemctl status vault
```

## 6. Initialize Vault

```bash
# Set Vault address for CLI
export VAULT_ADDR='http://127.0.0.1:8200'

# Initialize Vault with 5 keys and 3 required for unseal
vault operator init -key-shares=5 -key-threshold=3
```

IMPORTANT: Save the output from the initialization! It will show:
- 5 unseal keys
- Initial root token

Store these securely - they cannot be retrieved if lost!

## 7. Unseal Vault

You'll need to run the unseal command three times, using three different keys from the five generated:

```bash
# Run this three times with different keys
vault operator unseal
```

## 8. Verify Vault Status

```bash
# Check vault status
vault status

# Login with root token
vault login
```

## Basic Usage

```bash
# Enable a secrets engine
vault secrets enable -path=secret kv-v2

# Write a secret
vault kv put secret/my-secret foo=bar

# Read a secret
vault kv get secret/my-secret
```

## Security Notes

1. Store the unseal keys and root token securely
2. Distribute the 5 unseal keys to different trusted individuals
3. Consider changing the root token periodically
4. Ensure proper file permissions on Vault configuration files
5. Monitor Vault logs: `journalctl -u vault.service`

## Troubleshooting

If Vault fails to start:
1. Check logs: `journalctl -u vault.service -f`
2. Verify permissions on /opt/vault directories
3. Ensure ports 8200 and 8201 are not in use
4. Check SELinux status and adjust if needed
