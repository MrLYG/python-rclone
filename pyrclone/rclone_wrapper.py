import logging
import subprocess
import os
import sys

import pkg_resources


class RCloneWrapper:
    """
    Wrapper class for rclone.
    """

    def __init__(self, cfg):
        self.cfg = '\n'.join(f'[{name}]\n' + '\n'.join(f'{k} = {v}' for k,
                             v in settings.items()) for name, settings in cfg.items())
        self.log = logging.getLogger("RClone")

        rp = ""
        if pkg_resources.resource_exists('pyrclone', "win/rclone.exe"):
            rp = pkg_resources.resource_filename('pyrclone', "win")
        if pkg_resources.resource_exists('pyrclone', "mac/rclone"):
            rp = pkg_resources.resource_filename('pyrclone', "mac")
        if pkg_resources.resource_exists('pyrclone', "linux/rclone"):
            rp = pkg_resources.resource_filename('pyrclone', "linux")

        self.config_path = os.path.join(rp, "rclone.conf")
        self.rclone_path = os.path.join(rp, "rclone")

    def _execute(self, command_with_args):
        # print(command_with_args)
        self.log.debug("Invoking : %s", " ".join(command_with_args))
        try:
            proc = subprocess.run(
                command_with_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=True
            )

            out = proc.stdout
            err = proc.stderr

            self.log.debug(out)
            if err:
                self.log.warning(err.decode("utf-8").replace("\\n", "\n"))

            return {
                "code": proc.returncode,
                "out": out,
                "error": err
            }
        except FileNotFoundError as not_found_e:
            self.log.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            self.log.exception("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def _deexecute(self, command_with_args):
        print(command_with_args)
        self.log.debug("Invoking : %s", " ".join(command_with_args))
        try:
            with subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) as proc:
                (out, err) = proc.communicate()

                self.log.debug(out)
                if err:
                    self.log.warning(err.decode("utf-8").replace("\\n", "\n"))

                return {
                    "code": proc.returncode,
                    "out": out,
                    "error": err
                }
        except FileNotFoundError as not_found_e:
            self.log.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            self.log.exception("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def run_cmd(self, command, extra_args=[]):
        try:
            with open(self.config_path, 'w') as cfg_file:
                self.log.debug("rclone config: ~%s~", self.cfg)
                cfg_file.write(self.cfg)
                cfg_file.flush()
                command_with_args = [self.rclone_path,
                                     command, "--config", cfg_file.name]
                command_with_args += extra_args
                command_result = self._execute(command_with_args)
        finally:
            if os.path.isfile(self.config_path):
                os.remove(self.config_path)
        return command_result

    def copy(self, source, dest, flags=[]):
        return self.run_cmd(command="copy", extra_args=[source] + [dest] + flags)

    def sync(self, source, dest, flags=[]):
        return self.run_cmd(command="sync", extra_args=[source] + [dest] + flags)

    def listremotes(self, flags=[]):
        return self.run_cmd(command="listremotes", extra_args=flags)

    def ls(self, dest, flags=[]):
        return self.run_cmd(command="ls", extra_args=[dest] + flags)

    def lsjson(self, dest, flags=[]):
        return self.run_cmd(command="lsjson", extra_args=[dest] + flags)

    def delete(self, dest, flags=[]):
        return self.run_cmd(command="delete", extra_args=[dest] + flags)
