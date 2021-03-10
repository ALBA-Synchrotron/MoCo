# -*- coding: utf-8 -*-
#
# This file is part of the MoCo project
#
# Copyright (c) 2020 ALBA controls team
# Distributed under the GNU General Public License v3.
# See LICENSE for more info.


from tango.server import Device, attribute, device_property, command
from tango import AttributeProxy, DevState
import moco.core


class Moco(Device):

    url = device_property(dtype=str)
    softwareInBeamAtt = device_property(dtype=str, default_value=None)

    def init_device(self):
        super().init_device()
        self.moco = moco.core.Moco.for_url(self.url)
        self.in_beam_attr_proxy = None
        if self.softwareInBeamAtt is not None:
            self.in_beam_attr_proxy = AttributeProxy(self.softwareInBeamAtt)
        self.set_state(DevState.ON)
    # ------------------------------------------------------------------
    # COMMANDS
    # ------------------------------------------------------------------
    @command()
    def RestoreSoftInBeam(self):
        if self.in_beam_attr_proxy is None:
            raise Exception("Error: softwareInBeamAttr is not defined")
        value = self.in_beam_attr_proxy.read().value
        self.moco.soft_beam(value)

    @command()
    def Tune(self):
        self.moco.tune()

    @command()
    def TunePeak(self):
        self.moco.tune_peak()
        self.setToMoco("TUNE PEAK")

    @command()
    def Go(self):
        self.moco.go()

    @command()
    def Stop(self):
        self.moco.stop()

    @command(dtype_in=str, doc_in='Allowed values ON/OFF')
    def Pause(self, arg):
        self.moco.pause(arg)

    @command(dtype_in=[str],
             doc_in='Sequence of strings - ARGIN. They will be merged to a '
                    'SET ARGIN[0] ARGIN[1] ... and send to MOCO)')
    def SetOperationFlags(self, args):
        self.moco.set_operation_flags(args)

    @command(dtype_in=[str],
             doc_in='Sequence of strings - ARGIN. They will be merged to a '
                    'SET ARGIN[0] ARGIN[1] ... and send to MOCO)')
    def ClearOperationFlags(self, args):
        self.moco.clear_operation_flags(args)

    @command(dtype_out=[str])
    def GetInfo(self):
        return self.moco.info()

    @command()
    def Reset(self):
        self.moco.reset()

    @command(dtype_in=str, dtype_out=[str],
             doc_in='Any MOCO understandable command e.g. MODE, ?GAIN',
             doc_out='If a query command was sent, the result gets returned')
    def OnlineCmd(self, arg):
        self.debug_stream("OnlineCmd %s" % arg)
        arg = arg.strip('\r\n')
        if arg.startswith('?'):
            cmd = arg[1:]
            ans = self.moco.read_cmd(cmd)
            if not isinstance(ans, list):
                ans = [ans]
        else:
            self.moco.write_cmd(arg)
            ans = []
        return ans

    @command()
    def OscilOn(self):
        self.moco.oscil('ON')

    @command()
    def OscilOff(self):
        self.moco.oscil('OFF')

    # ------------------------------------------------------------------
    # ATTRIBUTES
    # ------------------------------------------------------------------
    @attribute(dtype=str,
               description='Set/query INBEAM configuration equivalent to '
                           '(?INBEAM/INBEAM)')
    def InBeamConf(self):
        return self.moco.in_beam_conf()

    @InBeamConf.write
    def InBeamConf(self, value):
        self.moco.in_beam_conf(value)

    @attribute(dtype=str,
               description='Set/query OUTBEAM configuration (equivalent to '
                           '?OUTBEAM/OUTBEAM)')
    def OutBeamConf(self):
        return self.moco.out_beam_conf()

    @OutBeamConf.write
    def OutBeamConf(self, value):
        self.moco.out_beam_conf(value)

    @attribute(dtype=float,
               description='Set/query setpoint value (equivalent to '
                           '?SETPOINT/SETPOINT)')
    def SetPoint(self):
        return self.moco.set_point()

    @SetPoint.write
    def SetPoint(self, value):
        self.moco.set_point(value)

    @attribute(dtype=str,
               description='Set/query operation mode (equivalent to '
                           '?MODE/MODE)')
    def Mode(self):
        return self.moco.mode()

    @Mode.write
    def Mode(self, value):
        self.moco.mode(value)

    @attribute(dtype=float,
               description='Set/query regulation time constant (equivalent '
                           'to ?TAU/TAU)')
    def Tau(self):
        return self.moco.tau()

    @Tau.write
    def Tau(self, value):
        self.moco.tau(value)

    @attribute(dtype=float,
               description='Set/query software INBEAM values (equivalent to '
                           '?SOFTBEAM/SOFTBEAM)')
    def SoftBeam(self):
        return self.moco.soft_beam()

    @SoftBeam.write
    def SoftBeam(self, value):
        self.moco.soft_beam(value)

    @attribute(dtype=[str],
               description='Set/query operation flags  equivalent to '
                           '?SET/SET)')
    def OperationFlags(self):
        return self.moco.operation_flags()

    @attribute(dtype=str)
    def Beam(self):
        beam, _, _ = self.moco.beam()
        return beam

    @attribute(dtype=float)
    def Beam_In(self):
        _, beam_in, _ = self.moco.beam()
        return beam_in

    @attribute(dtype=float)
    def Beam_Out(self):
        _, _, beam_out = self.moco.beam()
        return beam_out

    @attribute(dtype=str)
    def FBeam(self):
        fbeam, _, _ = self.moco.fbeam()
        return fbeam

    @attribute(dtype=float)
    def FBeam_In(self):
        _, fbeam_in, _ = self.moco.fbeam()
        return fbeam_in

    @attribute(dtype=float)
    def FBeam_Out(self):
        _, _, fbeam_out = self.moco.fbeam()
        return fbeam_out

    @attribute(dtype=str,
               description='Query controller state (equivalent to ?STATE)')
    def MocoState(self):
        return self.moco.state()

    @attribute(dtype=float,
               description='Set/query output voltage (equivalent to '
                           '?PIEZO/PIEZO)')
    def Piezo(self):
        return self.moco.piezo()

    @Piezo.write
    def Piezo(self, value):
        self.moco.piezo(value)

    @attribute(dtype=[float], max_dim_x=2,
               description='Set/query scanning speed values (equivalent to '
                           '?SPEED/SPEED)')
    def Speed(self):
        return self.moco.speed()

    @Speed.write
    def Speed(self, value):
        self.moco.speed(value)

    @attribute(dtype=float,
               description='Set/query scanning speed values (equivalent to '
                           '?SPEED/SPEED)')
    def ScanSpeed(self):
        return self.moco.scan_speed()

    @ScanSpeed.write
    def ScanSpeed(self, value):
        self.moco.scan_speed(value)

    @attribute(dtype=float,
               description='Set/query scanning speed values (equivalent to '
                           '?SPEED/SPEED)')
    def MoveSpeed(self):
        return self.moco.move_speed()

    @MoveSpeed.write
    def MoveSpeed(self, value):
        self.moco.move_speed(value)

    @attribute(dtype=float,
               description='Query main signal amplitude (equivalent to '
                           '?OSCBEAM[0])')
    def OscBeamMainSignal(self):
        main_signal, _ = self.moco.osc_beam_signals()
        return main_signal

    @attribute(dtype=float,
               description='Query quadrature signal amplitude (equivalent to '
                           '?OSCBEAM[1])')
    def OscBeamQuadSignal(self):
        _, quad_signal = self.moco.osc_beam_signals()
        return quad_signal

    @attribute(dtype=float,
               description='Set/query oscillation phase (equivalent to '
                           '?PHASE/PHASE)')
    def Phase(self):
        return self.moco.phase()

    @Phase.write
    def Phase(self, value):
        self.moco.phase(value)

    @attribute(dtype=float,
               description='Set/query amplitude of oscillation (equivalent '
                           'to ?AMPLITUDE/AMPLITUDE')
    def Amplitude(self):
        return self.moco.amplitude()

    @Amplitude.write
    def Amplitude(self, value):
        self.moco.amplitude(value)

    @attribute(dtype=float)
    def Frequency(self):
        return self.moco.frequency()

    @Frequency.write
    def Frequency(self, value):
        self.moco.frequency(value)

    @attribute(dtype=float,
               description='Set/query response function slope (equivalent to '
                           '?SLOPE/SLOPE)')
    def Slope(self):
        return self.moco.slope()

    @Slope.write
    def Slope(self, value):
        self.moco.slope(value)
