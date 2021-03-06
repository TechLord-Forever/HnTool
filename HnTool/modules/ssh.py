# -*- coding: utf-8 -*-
#
# HnTool rules - ssh
# Copyright (C) 2009-2010 Hugo Doria <mail@hugodoria.org>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

import os
import HnTool.modules.util
from HnTool.modules.rule import Rule as MasterRule

class Rule(MasterRule):
    def __init__(self, options):
        MasterRule.__init__(self, options)
        self.short_name="ssh"
        self.long_name="Checks security problems on sshd config file"
        self.type="config"
        self.required_files = ['/etc/ssh/sshd_config']

    def requires(self):
        return self.required_files

    def analyze(self, options):
        check_results = self.check_results
        ssh_conf_file = self.required_files

        for sshd_conf in ssh_conf_file:
            if os.path.isfile(sshd_conf):
                # dict with all the lines
                lines = HnTool.modules.util.hntool_conf_parser(sshd_conf)

                # Checking if SSH is using the default port
                if 'Port' in lines:
                    if int(lines['Port']) == 22:
                        check_results['low'].append('SSH is using the default port')
                    else:
                        check_results['ok'].append('SSH is not using the default port')
                else:
                    check_results['low'].append('SSH is using the default port')

                # Checking if SSH is using protocol v2 (recommended)
                if 'Protocol' in lines:
                    if int(lines['Protocol']) == 2:
                        check_results['ok'].append('SSH is using protocol v2')
                    else:
                        check_results['high'].append('SSH is not using protocol v2')
                else:
                    check_results['high'].append('SSH is not using protocol v2')

                # Checking if the Root Login is allowed
                if 'PermitRootLogin' in lines:
                    if lines['PermitRootLogin'] == 'yes':
                        check_results['medium'].append('Root access allowed')
                    else:
                        check_results['ok'].append('Root access is not allowed')
                else:
                    check_results['medium'].append('Root access is allowed')

                # Disconnects no successfully login after 30 seconds
                if 'LoginGraceTime' in lines:
                    if int(lines['LoginGraceTime']) > 30:
                        check_results['low'].append('Keeping connection login attempt to more than 30 seconds')
                    else:
                        check_results['ok'].append('Disconnects no successfully login after 30 seconds')
                else:
                    check_results['low'].append('Keeping connection login attempt to more than 30 seconds')

                # Disconnects session after more than 120 seconds of inactivity 
                if 'ClientAliveInterval' in lines and int(lines['Protocol']) == 2:
                    if int(lines['ClientAliveInterval']) > 120:
                        check_results['low'].append('Keeping inactive session')
                    else:
                        check_results['ok'].append('Disconnects session after more than 120 seconds of inactivity')
                else:
                    check_results['low'].append('Keeping inactive session')
                    
                # Total number of checkalive message sent by the ssh server
                if 'ClientAliveCountMax' in lines and int(lines['Protocol']) == 2:
                    if int(lines['ClientAliveInterval']) >= 4:
                        check_results['low'].append('High total number of checkalive message')
                    else:
                        check_results['ok'].append('Great value checkalive message')
                else:
                    check_results['low'].append('High total number of checkalive message')

                # Number of tries to login
                if 'MaxAuthTries' in lines:
                    if int(lines['MaxAuthTries']) >= 5:
                        check_results['low'].append('High value for login attempts')
                    else:
                        check_results['ok'].append('Good value for login attempts')
                else:
                    check_results['low'].append('High value for login attempts')

                # Total number of open sessions
                if 'MaxSessions' in lines:
                    if int(lines['MaxSessions']) > 5:
                        check_results['low'].append('High number of open sessions allowed')
                    else:
                        check_results['ok'].append('Good value of open sessions allowed')
                else:
                    check_results['low'].append('High number of open sessions allowed')

                # Checking if empty password are allowed (shouldn't)
                if 'PermitEmptyPasswords' in lines:
                    if lines['PermitEmptyPasswords'] == 'yes':
                        check_results['high'].append('Empty passwords are allowed')
                    else:
                        check_results['ok'].append('Empty passwords are not allowed')
                else:
                    check_results['high'].append('Empty passwords are allowed')

                # Specifies whether rhosts or shosts files should not be used in authentication
                if 'IgnoreRhosts' in lines:
                    if lines['IgnoreRhosts'] == 'no':
                        check_results['high'].append('Using rhosts file')
                    else:
                        check_results['ok'].append('Not using rhosts file')
                else:
                    check_results['high'].append('Using rhosts file')

                # Checking if X11 Forward is allowed (shouldn't)
                if 'X11Forwarding' in lines:
                    if lines['X11Forwarding'] == 'yes':
                        check_results['low'].append('X11 forward is allowed')
                    else:
                        check_results['ok'].append('X11 forward is not allowed')
                else:
                    check_results['ok'].append('X11 forward is not allowed')

                # Checking if SSH allow TCP Forward (shouldn't)
                if 'AllowTcpForwarding' in lines:
                    if lines['AllowTcpForwarding'] == 'yes':
                        check_results['low'].append('TCP forwarding is allowed')
                    else:
                        check_results['ok'].append('TCP forwarding is not allowed')
                else:
                    check_results['low'].append('TCP forwarding is allowed')

        return check_results
