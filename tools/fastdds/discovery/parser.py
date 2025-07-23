# Copyright 2020 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
fastdds discovery verb parser.

The parser just forward the sub-commands to the fast-discovery-server
tool application.

"""

import os
import re
import subprocess
import sys
from pathlib import Path


class Parser:
    """Discovery server tool parser."""

    __help_message = 'fastdds discovery <discovery-args>\n\n'

    def __init__(self, argv):
        """
        Parse the sub-command and dispatch to the appropriate handler.

        Shows usage if no sub-command is specified.

        """
        tool_path = str(self.__find_tool_path().resolve())

        try:
            # Test if tool exists and can run
            result = subprocess.run(
                [tool_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            if result.returncode != 0:
                # Tool exists but failed to run - show actual error
                print(f"Error running fast-discovery-server:")
                if result.stderr:
                    print(result.stderr, end='')
                if result.stdout:
                    print(result.stdout, end='')
                sys.exit(result.returncode)

            if (
                    len(argv) == 0 or
                    (len(argv) == 1 and argv[0] == '-h') or
                    (len(argv) == 1 and argv[0] == '--help')
               ):
                print(self.__edit_tool_help(result.stdout))
            else:
                # Call the tool with actual arguments
                result = subprocess.run([tool_path] + argv)
                if result.returncode != 0:
                    # Exit with same code, but don't print misleading messages
                    sys.exit(result.returncode)

        except KeyboardInterrupt:
            # it lets the subprocess to handle the exception
            pass

        except FileNotFoundError:
            print(f'fast-discovery-server tool not found at: {tool_path}')
            print('Please ensure Fast-DDS is properly built and installed.')
            sys.exit(1)

        except Exception as e:
            print(f'Unexpected error running fast-discovery-server: {str(e)}')
            sys.exit(1)

    def __find_tool_path(self):
        """
        Calculate the path to the fast-discovery-server tool.

        returns str:
            Full path to the executable

        """
        tool_path = Path(os.path.dirname(os.path.realpath(__file__)))
        # We asume the installion path is relative to our installation path
        tool_path = tool_path / '../../../bin'
        if os.name == 'posix':
            ret = tool_path / 'fast-discovery-server'
            if not os.path.exists(ret):
                print(f'fast-discovery-server tool not found at: {ret}')
                print('Please ensure Fast-DDS is properly built and installed.')
                print('You may need to run: colcon build --packages-select fastrtps')
                sys.exit(1)
        elif os.name == 'nt':
            ret = tool_path / 'fast-discovery-server.exe'
            if not os.path.exists(ret):
                ret = tool_path / 'fast-discovery-server.bat'
                if not os.path.exists(ret):
                    print('fast-discovery-server tool not installed')
                    sys.exit(1)
        else:
            print(f'{os.name} not supported')
            sys.exit(1)

        return ret

    def __edit_tool_help(self, usage_text):
        """Find and replace the tool-name by fastdds discovery."""
        m = re.search('Usage: ([a-zA-Z0-9-\\.]*)\\s', usage_text)
        if m:
            tool_name = m.group(1)
            return re.sub(tool_name, 'fastdds discovery', usage_text)

        return usage_text
