# Azure CLI Commands Reference - az keyvault secret

This document provides a reference for Azure CLI commands related to Azure Key Vault secrets.

## Overview

Azure Key Vault is a cloud service that provides a secure store for secrets, keys, and certificates. The `az keyvault secret` commands allow you to manage secrets in your Azure Key Vault.

## Command Groups

| Command Group | Description |
|---------------|-------------|
| az keyvault secret | Manage secrets in Azure Key Vault |

## Commands

### az keyvault secret set

Create a secret in a Key Vault.

#### Syntax

```bash
az keyvault secret set --name NAME --vault-name VAULT_NAME 
                       [--description DESCRIPTION]
                       [--disabled {false, true}]
                       [--encoding ENCODING]
                       [--expires EXPIRES]
                       [--file FILE]
                       [--not-before NOT_BEFORE]
                       [--tags TAGS]
                       [--value VALUE]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --name -n | Name of the secret |
| --vault-name | Name of the Key Vault |
| --description | Description of the secret contents (e.g. password, connection string, etc.) |
| --disabled | Create secret in disabled state |
| --encoding | Source file encoding. The value is saved as a tag (file-encoding=<val>) and used during download to automatically encode the resulting file. Accepted values: ascii, base64, hex, utf-16be, utf-16le, utf-8 |
| --expires | Expiration UTC datetime (Y-m-d'T'H:M:S'Z') |
| --file | Source file for secret. Use in conjunction with '--encoding' |
| --not-before | Secret not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z') |
| --tags | Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags |
| --value | Plain text secret value. Cannot be used with '--file' or '--encoding' |

#### Examples

Create a secret with a value:
```bash
az keyvault secret set --vault-name MyKeyVault --name MySecretName --value MySecretValue
```

Create a secret from a file:
```bash
az keyvault secret set --vault-name MyKeyVault --name MySecretName --file /path/to/file --encoding utf-8
```

### az keyvault secret show

Get a specified secret from a Key Vault.

#### Syntax

```bash
az keyvault secret show [--id ID]
                        [--name NAME]
                        [--vault-name VAULT_NAME]
                        [--version VERSION]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --id | ID of the secret. If specified all other 'Id' arguments should be omitted |
| --name -n | Name of the secret. Required if --id is not specified |
| --vault-name | Name of the Key Vault. Required if --id is not specified |
| --version -v | The secret version. If omitted, uses the latest version |

#### Examples

Get a secret:
```bash
az keyvault secret show --name MySecret --vault-name MyKeyVault
```

Get a specific version of a secret:
```bash
az keyvault secret show --name MySecret --vault-name MyKeyVault --version SecretVersion
```

Get just the secret value as plain text:
```bash
az keyvault secret show --name MySecret --vault-name MyKeyVault --query value -o tsv
```

### az keyvault secret list

List secrets in a specified Key Vault.

#### Syntax

```bash
az keyvault secret list --vault-name VAULT_NAME
                        [--maxresults MAXRESULTS]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --vault-name | Name of the Key Vault |
| --maxresults | Maximum number of results to return |

#### Examples

List all secrets in a Key Vault:
```bash
az keyvault secret list --vault-name MyKeyVault
```

### az keyvault secret delete

Delete a secret from a Key Vault.

#### Syntax

```bash
az keyvault secret delete [--id ID]
                          [--name NAME]
                          [--vault-name VAULT_NAME]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --id | ID of the secret. If specified all other 'Id' arguments should be omitted |
| --name -n | Name of the secret. Required if --id is not specified |
| --vault-name | Name of the Key Vault. Required if --id is not specified |

#### Examples

Delete a secret:
```bash
az keyvault secret delete --name MySecret --vault-name MyKeyVault
```

### az keyvault secret backup

Back up a secret in a Key Vault.

#### Syntax

```bash
az keyvault secret backup --file FILE
                          [--id ID]
                          [--name NAME]
                          [--vault-name VAULT_NAME]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --file | File to receive the secret contents |
| --id | ID of the secret. If specified all other 'Id' arguments should be omitted |
| --name -n | Name of the secret. Required if --id is not specified |
| --vault-name | Name of the Key Vault. Required if --id is not specified |

#### Examples

Back up a secret to a file:
```bash
az keyvault secret backup --name MySecret --vault-name MyKeyVault --file secret-backup.bak
```

### az keyvault secret restore

Restore a backed-up secret to a Key Vault.

#### Syntax

```bash
az keyvault secret restore --file FILE
                          [--vault-name VAULT_NAME]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --file | File containing the backed-up secret |
| --vault-name | Name of the Key Vault |

#### Examples

Restore a secret from a backup file:
```bash
az keyvault secret restore --vault-name MyKeyVault --file secret-backup.bak
```

### az keyvault secret download

Download a secret from a Key Vault.

#### Syntax

```bash
az keyvault secret download --file FILE
                           [--encoding ENCODING]
                           [--id ID]
                           [--name NAME]
                           [--vault-name VAULT_NAME]
                           [--version VERSION]
```

#### Parameters

| Parameter | Description |
|-----------|-------------|
| --file | File to receive the secret contents |
| --encoding | Encoding of the secret. By default, will look for the 'file-encoding' tag on the secret. Otherwise will assume 'utf-8'. Allowed values: ascii, base64, hex, utf-16be, utf-16le, utf-8 |
| --id | ID of the secret. If specified all other 'Id' arguments should be omitted |
| --name -n | Name of the secret. Required if --id is not specified |
| --vault-name | Name of the Key Vault. Required if --id is not specified |
| --version -v | The secret version. If omitted, uses the latest version |

#### Examples

Download a secret to a file:
```bash
az keyvault secret download --name MySecret --vault-name MyKeyVault --file mysecret.txt
```

## Common Scenarios

### Creating and managing secrets

1. Create a new secret:
   ```bash
   az keyvault secret set --vault-name "MyKeyVault" --name "ExamplePassword" --value "SecretValue"
   ```

2. Retrieve a secret:
   ```bash
   az keyvault secret show --name "ExamplePassword" --vault-name "MyKeyVault"
   ```

3. Get only the secret value (plain text):
   ```bash
   az keyvault secret show --name "ExamplePassword" --vault-name "MyKeyVault" --query "value" -o tsv
   ```

4. List all secrets in a vault:
   ```bash
   az keyvault secret list --vault-name "MyKeyVault"
   ```

5. Delete a secret:
   ```bash
   az keyvault secret delete --vault-name "MyKeyVault" --name "ExamplePassword"
   ```

### Working with multiline secrets

For multiline secrets, save the secret content to a file first, then use the `--file` parameter:

1. Create a multiline secret from a file:
   ```bash
   # First, create a file with the multiline content
   az keyvault secret set --vault-name "MyKeyVault" --name "MultilineSecret" --file "secretfile.txt"
   ```

## References

For more information, see:
- [Azure Key Vault documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure Key Vault CLI reference](https://learn.microsoft.com/en-us/cli/azure/keyvault?view=azure-cli-latest)
- [Key Vault secrets documentation](https://learn.microsoft.com/en-us/azure/key-vault/secrets/about-secrets)