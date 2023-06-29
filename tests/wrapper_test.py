from pathlib import Path
import re
import tempfile
import os
import logging
import json

import pkg_resources
from pyrclone.rclone_wrapper import RCloneWrapper
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")

config = {
    "local": {
        "type": "local",
        "nounc": True
    }
}

rclone = RCloneWrapper(config)


def test_execute_with_wrong_command():
    result = rclone._execute(
        ["command_not_valid", "some", "args"])
    assert result.get('code') == -20
    assert isinstance(result.get('error'), FileNotFoundError)


def test_listremoted():
    result = rclone.listremotes()
    assert result.get('code') == 0
    assert result.get('out') == b'local:\n'


def test_copy_and_ls():
    source = "local:" + os.getcwd() + "/README.md"
    with tempfile.TemporaryDirectory() as dest:
        result = rclone.copy(
            source, "local:" + dest)
        assert result.get('code') == 0
        assert result.get('out') == b''

        result = rclone.ls("local:"+dest)
        assert result.get('code') == 0
        assert re.search(
            r'.*\sREADME.md.*', result.get('out').decode("utf-8")), "README.md was not listed."


def test_copy_lsjson_and_delete():
    source = "local:" + os.getcwd() + "/README.md"
    with tempfile.TemporaryDirectory() as dest:
        # copy
        result = rclone.copy(
            source, "local:" + dest)
        assert result.get('code') == 0
        assert result.get('out') == b''
        # lsjson
        result = rclone.lsjson("local:"+dest)
        assert result.get('code') == 0
        result_json = json.loads(result.get('out').decode("utf-8"))
        assert len(result_json) > 0
        assert result_json[0].get('Path') == 'README.md'
        assert not result_json[0].get('IsDir')
        # delete
        result = rclone.delete(
            "local:" + dest + "/README.md")
        assert result.get('code') == 0
        # lsjson to check that the file is gone
        result = rclone.lsjson("local:"+dest)
        assert result.get('code') == 0
        result_json = json.loads(result.get('out').decode("utf-8"))
        assert len(result_json) == 0


def test_rclone_sync(tmp_path: Path):
    """
    Test rclone sync command on local

    Parameters:
        tmp_path (Path): Temporary path to use for the test
    """

    local_path = tmp_path.joinpath("local_path")
    local_path.mkdir()
    dest_path = tmp_path.joinpath("destination")
    dest_path.mkdir()
    logging.info(f'local_path: {local_path}')
    logging.info(f'dest_path: {dest_path}')
    test_file_name = f'{local_path}/test_rclone_file.txt'
    test_file_content = 'This is a test file to test rclone sync command'
    with open(test_file_name, 'w') as f:
        f.write(test_file_content)

    rclone.sync(f'{local_path}/', f'{dest_path}/')

    # Check that the file was synced correctly
    synced_file = f'{dest_path}/test_rclone_file.txt'
    assert os.path.isfile(synced_file)
    # Check the content of the synced file
    with open(synced_file, 'r') as f:
        synced_file_content = f.read()
    assert synced_file_content == test_file_content

    shutil.rmtree(tmp_path, ignore_errors=True)


if __name__ == "__main__":
    data_path = pkg_resources.resource_filename('pyrclone', '*/rlcone.exe')
    print(data_path)
    print(data_path)
    tmp_path = Path("C:\\tmp\\rclone_test")
    # test rclone sync on local
    shutil.rmtree(tmp_path, ignore_errors=True)
    tmp_path.mkdir(exist_ok=True)
    test_rclone_sync(tmp_path)
