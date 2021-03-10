# -*- coding: utf-8 -*-
#
# This file is part of the MoCo project
#
# Copyright (c) 2020 ALBA controls team
# Distributed under the GNU General Public License v3.
# See LICENSE for more info.

import serial


class SyncConn:
    def __init__(self, url, timeout=1.5, **kwargs):
        self._conn = serial.serial_for_url(url, timeout=timeout, **kwargs)

    def write_raw(self, data):
        self._conn.write(data)

    def write_readline(self, data):
        self._conn.write(data)
        return self._conn.readline()

    def write_readlines(self, data):
        self._conn.write(data)
        return self._conn.readlines()


class Moco:

    def __init__(self, conn):
        self.conn = conn

    @classmethod
    def for_url(cls, url, **kwargs):
        conn = SyncConn(url, **kwargs)
        return cls(conn)

    def write_cmd(self, cmd):
        data = '{}\r?ERR\r'.format(cmd)
        ans = self.conn.write_readline(data.encode())
        ans = ans.decode()
        ans = ans.strip('\r\n')
        if ans.lower() != 'ok':
            raise Exception('Error: {}'.format(ans))

    def read_cmd(self, cmd):
        MULTILINE_CMDS = ["HELP", "INFO"]
        data = '?{}\r'.format(cmd)
        if cmd in MULTILINE_CMDS:
            lines = self.conn.write_readlines(data.encode())
            ans = []
            # Remove $ character used on multilines commands
            for line in lines[1:-1]:
                line = line.decode()
                ans.append(line.strip('\r\n'))
        else:
            ans = self.conn.write_readline(data.encode())
            ans = ans.decode()
            ans = ans.strip('\r\n')

        if ans == 'ERROR':
            err = self.conn.write_readline(b'?ERR\r')
            err = err.decode()
            raise Exception('Error: {}'.format(err))
        return ans

    # ------------------------------------------------------------------------
    #                           Attributes
    # ------------------------------------------------------------------------

    def in_beam_conf(self, conf=None):
        if conf is None:
            value = self.read_cmd('INBEAM')
            return value
        cmd = 'INBEAM {0}'.format(conf)
        self.write_cmd(cmd)

    def out_beam_conf(self, conf=None):
        if conf is None:
            value = self.read_cmd('OUTBEAM')
            return value
        cmd = 'OUTBEAM {0}'.format(conf)
        self.write_cmd(cmd)

    def set_point(self, value=None):
        if value is None:
            value = float(self.read_cmd('SETPOINT'))
            return value
        cmd = 'SETPOINT {}'.format(value)
        self.write_cmd(cmd)

    def mode(self, value=None):
        if value is None:
            value = self.read_cmd('MODE')
            return value
        cmd = 'MODE {}'.format(value)
        self.write_cmd(cmd)

    def tau(self, value=None):
        if value is None:
            value = float(self.read_cmd('TAU'))
            return value
        cmd = 'TAU {}'.format(value)
        self.write_cmd(cmd)

    def soft_beam(self, value=None):
        if value is None:
            value = float(self.read_cmd('SOFTBEAM'))
            return value
        cmd = 'SOFTBEAM {0}'.format(float(value))
        self.write_cmd(cmd)

    def operation_flags(self):
        value = self.read_cmd('SET')
        return value

    def beam(self):
        beam = self.read_cmd('BEAM')
        beam_in, beam_out = beam.split()
        beam_in = float(beam_in)
        beam_out = float(beam_out)
        return beam, beam_in, beam_out

    def fbeam(self):
        fbeam = self.read_cmd('FBEAM')
        fbeam_in, fbeam_out = fbeam.split()
        fbeam_in = float(fbeam_in)
        fbeam_out = float(fbeam_out)
        return fbeam, fbeam_in, fbeam_out

    def state(self):
        value = self.read_cmd('STATE')
        return value

    def piezo(self, value=None):
        if value is None:
            value = float(self.read_cmd('PIEZO'))
            return value
        cmd = 'PIEZO {}'.format(value)
        self.write_cmd(cmd)

    def speed(self, values=None):
        if values is None:
            scan_speed, move_speed = self.read_cmd('SPEED').split()
            return float(scan_speed), float(move_speed)
        str_values = ''
        for value in values:
            str_values += '{} '.format(str(value))
        cmd = 'SPEED {}'.format(str_values)
        self.write_cmd(cmd)

    def scan_speed(self, value=None):
        if value is None:
            scan_speed, _ = self.speed()
            return scan_speed
        self.speed([value])

    def move_speed(self, value=None):
        scan_speed, move_speed = self.speed()
        if value is None:
            return move_speed
        self.speed([scan_speed, value])

    def osc_beam_signals(self):
        main_signal, quad_signal = self.read_cmd('OSCBEAM').split()
        main_signal = float(main_signal)
        quad_signal = float(quad_signal)
        return main_signal, quad_signal

    def phase(self, value=None):
        if value is None:
            value = float(self.read_cmd('PHASE'))
            return value
        cmd = 'PHASE {}'.format(value)
        self.write_cmd(cmd)

    def amplitude(self, value=None):
        if value is None:
            value = float(self.read_cmd('AMPLITUDE'))
            return value
        cmd = 'AMPLITUDE {}'.format(value)
        self.write_cmd(cmd)

    def frequency(self, value=None):
        if value is None:
            value = float(self.read_cmd('FREQUENCY'))
            return value
        cmd = 'FREQUENCY {}'.format(value)
        self.write_cmd(cmd)

    def slope(self, value=None):
        if value is None:
            value = float(self.read_cmd('SLOPE'))
            return value
        cmd = 'SLOPE {}'.format(value)
        self.write_cmd(cmd)

    def operation_flags(self):
        value = self.read_cmd('SET').split()
        return value

    def oscil(self, value=None):
        if value is None:
            value = self.read_cmd('OSCIL')
            return value
        cmd = 'OSCIL {}'.format(value)
        self.write_cmd(cmd)

    # ------------------------------------------------------------------------
    #                           Commands
    # ------------------------------------------------------------------------

    def tune(self):
        self.write_cmd('TUNE')

    def tune_peak(self):
        self.write_cmd('TUNE PEAK')

    def go(self):
        self.write_cmd('GO')

    def stop(self):
        self.write_cmd('STOP')

    def pause(self, arg):
        self.write_cmd('PAUSE {}'.format(arg))

    def set_operation_flags(self, args):
        flags = ' '.join(args)
        cmd = 'SET {}'.format(flags)
        self.write_cmd(cmd)

    def clear_operation_flags(self, args):
        flags = ' '.join(args)
        cmd = 'CLEAR {}'.format(flags)
        self.write_cmd(cmd)

    def info(self):
        value = self.read_cmd('INFO')
        return value

    def reset(self):
        # The reset command do not allow to check the error after
        self.conn.write_raw(b'RESET\r')
