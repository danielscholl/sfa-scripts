# Azure KeyVault Secrets Python SDK

## Overview

The Azure KeyVault Secrets client library for Python allows you to securely store and control access to tokens, passwords, certificates, API keys, and other secrets in Azure Key Vault. This library is part of the Azure SDK for Python, which provides several Key Vault client libraries:

- **Secrets management** (this library) - securely store and control access to tokens, passwords, certificates, API keys, and other secrets
- **Cryptographic key management** (azure-keyvault-keys) - create, store, and control access to the keys used to encrypt your data
- **Certificate management** (azure-keyvault-certificates) - create, manage, and deploy public and private SSL/TLS certificates
- **Vault administration** (azure-keyvault-administration) - role-based access control (RBAC), and vault-level backup and restore options

## Installation

Install the Azure Key Vault Secrets client library and Azure Identity library with pip:

```bash
pip install azure-keyvault-secrets azure-identity
```

## Prerequisites

- An Azure subscription
- Python 3.7+
- An existing Azure Key Vault

## Getting Started

To use the library, you'll need:
- The vault URL (also known as the vault's "DNS Name")
- Appropriate credentials for authentication

### Authenticating with Azure Identity

The recommended way to authenticate is to use the `DefaultAzureCredential` from the Azure Identity library, which supports multiple authentication methods and determines which method to use at runtime:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Create a secret client using default Azure credentials
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)
```

## Key Concepts

### Secret

A secret in Key Vault consists of a value and its associated metadata/management information. In this library, secret values are handled as strings, although Azure Key Vault doesn't store them as such.

## Usage Examples

### Setting a Secret

```python
# Create a new secret or update an existing secret's value
secret = secret_client.set_secret("secret-name", "secret-value")
print(secret.name)
print(secret.value)
print(secret.properties.version)
```

### Getting a Secret

```python
# Get the latest version of a secret
secret = secret_client.get_secret("secret-name")

# Get a specific version of a secret
secret = secret_client.get_secret("secret-name", version="secret-version")

print(secret.id)
print(secret.name)
print(secret.value)
print(secret.properties.version)
```

### Updating Secret Properties

```python
# Update properties of a secret (can't change its value)
content_type = "text/plain"
tags = {"environment": "production"}

updated_secret_properties = secret_client.update_secret_properties(
    "secret-name",
    content_type=content_type,
    tags=tags,
    enabled=True
)

print(updated_secret_properties.version)
print(updated_secret_properties.updated_on)
print(updated_secret_properties.content_type)
print(updated_secret_properties.tags)
```

### Listing Secrets

```python
# List all secrets in the vault (doesn't include values)
secret_properties = secret_client.list_properties_of_secrets()

for secret_property in secret_properties:
    # The list doesn't include values or versions of the secrets
    print(secret_property.name)
```

### Listing Secret Versions

```python
# List all versions of a secret (doesn't include values)
secret_versions = secret_client.list_properties_of_secret_versions("secret-name")

for secret_property in secret_versions:
    print(secret_property.id)
    print(secret_property.enabled)
    print(secret_property.updated_on)
```

### Deleting a Secret

```python
# Delete a secret (this is a long-running operation when soft-delete is enabled)
poller = secret_client.begin_delete_secret("secret-name")
deleted_secret = poller.result()

print(deleted_secret.name)
print(deleted_secret.deleted_date)
```

### Working with Deleted Secrets (Soft-Delete Enabled Vaults)

```python
# List deleted secrets
deleted_secrets = secret_client.list_deleted_secrets()

for deleted_secret in deleted_secrets:
    print(deleted_secret.name)
    print(deleted_secret.deleted_date)

# Get a specific deleted secret
deleted_secret = secret_client.get_deleted_secret("secret-name")
print(deleted_secret.name)

# Recover a deleted secret
recovered_secret = secret_client.recover_deleted_secret("secret-name")
print(recovered_secret.name)
```

### Backing Up and Restoring Secrets

```python
# Backup a secret
secret_backup = secret_client.backup_secret("secret-name")

# Restore a secret from backup
restored_secret = secret_client.restore_secret_backup(secret_backup)
print(restored_secret.id)
print(restored_secret.name)
```

## Asynchronous Client

The library also provides an asynchronous client through the `azure.keyvault.secrets.aio` namespace:

```python
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)

# Example of an async operation
async def set_secret_example():
    secret = await secret_client.set_secret("secret-name", "secret-value")
    print(secret.name)
    print(secret.value)
    print(secret.properties.version)
```

## Enabling Logging

To enable detailed logging for debugging:

```python
import sys
import logging

# Create a logger for the 'azure' SDK
logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)

# Configure a console output handler
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

# Create a client with logging enabled
secret_client = SecretClient(
    vault_url="https://my-key-vault.vault.azure.net/",
    credential=credential,
    logging_enable=True
)

# Alternatively, enable logging for a single operation
secret_client.get_secret("my-secret", logging_enable=True)
```

## Additional Resources

- [Source code on GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-secrets)
- [Package on PyPI](https://pypi.org/project/azure-keyvault-secrets/)
- [API reference documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/keyvault-secrets-readme)
- [Key Vault documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Code samples on GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-secrets/samples)