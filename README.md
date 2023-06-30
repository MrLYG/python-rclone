# PyRCLONE
A Python wrapper for rclone.

This package, available on PyPI, conveniently includes the rclone binary (version v1.62.2) **eliminating the need for pre-installation of rclone**. It caters to various operating systems like Windows, Mac, and Linux, and supports both amd64 and x86_64 architectures. When a user downloads the package, the appropriate rclone binary file is installed based on their system type.

## Install
```python
pip install pyrclone-wrapper
```

## Usage
```python
from pyrclone import RCloneWrapper


config = {
    "remote_name": {
        'type': 'google cloud storage',
        'project_number': "project_number",
        'service_account_file': "path/to/service_account_file.json",
        'object_acl': 'private',
        'bucket_acl': 'private',
        'location': 'us',
        'storage_class': 'STANDARD'
    }
}
rclone = RCloneWrapper(config)
result = rclone.listremotes()
print(result.get('out'))
# b'remote_name:\n'
print(result.get('code'))
# 0
print(result.get('error'))
# b''
```

###  Implemented commands:

* `copy`            Copy files from source to dest, skipping already copied
* `sync`            Make source and dest identical, modifying destination only.
* `listremotes`     List all the remotes in the config file.
* `ls`              List the objects in the path with size and path.
* `lsjson`          List directories and objects in the path in JSON format.
* `delete`          Remove the contents of path.

Even if not all `rclone` commands have been exposed, it's possible to invoke any command using `run_cmd` method directly, as shown in the example bellow:

```python
from pyrclone import RCloneWrapper

config = {
    "local": {
        'type': 'local',
        'nounc': True,
    }
}
result = RCloneWrapper(config).run_cmd(command="lsd", extra_args=["local:/tmp", "-v", "--dry-run"])
```
### Logging and Debugging

To see more info about which commands are executed, or what other messages they print, you can enable logging as the example bellow shows:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")

from pyrclone import RCloneWrapper

config = {
    "local": {
        'type': 'local',
        'nounc': True,
    }
}
rclone = RCloneWrapper(config)
result = rclone.listremotes()
```

## Limitation
Only support windows, mac and, linux operating system and arch with amd64 and x86_64.

windwos: amd64

linux: amd64, x86_64

darwin(mac): amd64, x86_64

## Developer guide

```bash
$ pip install wheel twine pytest
$ make test
```

## Reference
[python-rclone](https://github.com/ddragosd/python-rclone) ( base on this project and improve it )

[rclone](https://rclone.org/)





