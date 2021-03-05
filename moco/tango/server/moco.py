import sys
import serial
import PyTango

RESTORESOFTINBEAM_IN_DOC = ''
RESTORESOFTINBEAM_OUT_DOC = ''
TUNE_IN_DOC = ''
TUNE_OUT_DOC = ''
TUNEPEAK_IN_DOC = ''
TUNEPEAK_OUT_DOC = ''
GO_IN_DOC = ''
GO_OUT_DOC = ''
STOP_IN_DOC = ''
STOP_OUT_DOC = ''
PAUSE_IN_DOC = 'ON/OFF'
PAUSE_OUT_DOC = ''
SETOPERATIONFLAGS_IN_DOC = ('Sequence of strings - ARGIN. They will be merged ' +
                           'to a SET ARGIN[0] ARGIN[1] ... and send to MOCO')
SETOPERATIONFLAGS_OUT_DOC = ''
CLEAROPERATIONFLAGS_IN_DOC = ('Sequence of strings - ARGIN. They will be merged ' +
                           'to CLEAR ARGIN[0] ARGIN[1] ... and send to MOCO')
CLEAROPERATIONFLAGS_OUT_DOC = ''
GETINFO_IN_DOC = ''
GETINFO_OUT_DOC = ''
RESET_IN_DOC = ''
RESET_OUT_DOC = ''
ONLINECMD_IN_DOC = 'Any MOCO understandable command e.g. MODE, ?GAIN'
ONLINECMD_OUT_DOC = 'If a query command was sent, the result gets returned'
OSCILON_IN_DOC = ''
OSCILON_OUT_DOC = ''
OSCILOFF_IN_DOC = ''
OSCILOFF_OUT_DOC = ''


INBEAMCONF_DOC = ('Set/query INBEAM configuration (equivalent to ' +
                                                            '?INBEAM/INBEAM)')
OUTBEAMCONF_DOC = ('Set/query OUTBEAM configuration (equivalent to ' +
                                                            '?OUTBEAM/OUTBEAM)')
SETPOINT_DOC = 'Set/query setpoint value (equivalent to ?SETPOINT/SETPOINT)'
MODE_DOC = 'Set/query operation mode (equivalent to ?MODE/MODE)'
TAU_DOC = 'Set/query regulation time constant (equivalent to ?TAU/TAU)'
SOFTBEAM_DOC = ('Set/query software INBEAM values (equivalent to ' +
                                                          '?SOFTBEAM/SOFTBEAM)')
OPERATIONFLAGS_DOC = 'Set/query operation flags (equivalent to ?SET/SET)'
MOCOSTATE_DOC = 'Query controller state (equivalent to ?STATE)'
PIEZO_DOC = 'Set/query output voltage (equivalent to ?PIEZO/PIEZO)' 
SCANSPEED_DOC = 'Set/query scanning speed values (equivalent to ?SPEED/SPEED)'
OSCBEAMMAINSIGNAL_DOC = ('Query main signal amplitude (equivalent to ' + 
                                                                 '?OSCBEAM[0])')
OSCBEAMQUADSIGNAL_DOC = ('Query quadrature signal amplitude (equivalent to ' + 
                                                                 '?OSCBEAM[1])')
PHASE_DOC = 'Set/query oscillation phase (equivalent to ?PHASE/PHASE)'
AMPLITUDE_DOC = ('Set/query amplitude of oscillation (equivalent to ' +
                                                         '?AMPLITUDE/AMPLITUDE')
FREQUENCY_DOC = ('Set/query oscillation frequency (equivalent to ' + 
                                                        '?FREQUENCY/FREQUENCY)') 
SLOPE_DOC = 'Set/query response function slope (equivalent to ?SLOPE/SLOPE)'

class MocoClass(PyTango.DeviceClass):

    cmd_list = { 'RestoreSoftInBeam' : 
                 [ [ PyTango.ArgType.DevVoid, RESTORESOFTINBEAM_IN_DOC ],
                   [ PyTango.ArgType.DevVoid, RESTORESOFTINBEAM_OUT_DOC ] ],
                 'Tune' : [ [ PyTango.ArgType.DevVoid, TUNE_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, TUNE_OUT_DOC ] ],
                  'TunePeak' : [ [ PyTango.ArgType.DevVoid, TUNEPEAK_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, TUNEPEAK_OUT_DOC ] ],
                  'Go' : [ [ PyTango.ArgType.DevVoid, GO_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, GO_OUT_DOC ] ],
                  'Stop' : [ [ PyTango.ArgType.DevVoid, STOP_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, STOP_OUT_DOC ] ],
                  'Pause' : [ [ PyTango.ArgType.DevString, PAUSE_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, PAUSE_OUT_DOC ] ],
                  'SetOperationFlags' : [ [ PyTango.ArgType.DevVarStringArray, 
                                            SETOPERATIONFLAGS_IN_DOC ],
                                        [ PyTango.ArgType.DevVoid, 
                                            SETOPERATIONFLAGS_OUT_DOC ] ],
                  'ClearOperationFlags' : [ [ PyTango.ArgType.DevVarStringArray, 
                                              CLEAROPERATIONFLAGS_IN_DOC ],
                                        [ PyTango.ArgType.DevVoid,
                                              CLEAROPERATIONFLAGS_OUT_DOC ] ],
                  'GetInfo' : [ [ PyTango.ArgType.DevVoid, GETINFO_IN_DOC ],
                            [ PyTango.ArgType.DevVarStringArray, 
                              GETINFO_OUT_DOC ] ],
                  'Reset' : [ [ PyTango.ArgType.DevVoid, RESET_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, RESET_OUT_DOC ] ],
                  'OnlineCmd' : [ [ PyTango.ArgType.DevString, 
                                    ONLINECMD_IN_DOC ],
                            [ PyTango.ArgType.DevVarStringArray, 
                              ONLINECMD_OUT_DOC ] ],
                  'OscilOn' : [ [ PyTango.ArgType.DevVoid, OSCILON_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, OSCILON_OUT_DOC ] ],
                  'OscilOff' : [ [ PyTango.ArgType.DevVoid, OSCILOFF_IN_DOC ],
                            [ PyTango.ArgType.DevVoid, OSCILOFF_OUT_DOC ] ],
    }

    attr_list = { 'InBeamConf' : [ [ PyTango.ArgType.DevString ,
                                    PyTango.AttrDataFormat.SCALAR ,
                                    PyTango.AttrWriteType.READ_WRITE],
                                   {'description' : INBEAMCONF_DOC} ],
                  'OutBeamConf' : [ [ PyTango.ArgType.DevString ,
                                    PyTango.AttrDataFormat.SCALAR ,
                                    PyTango.AttrWriteType.READ_WRITE],
                                    {'description' : OUTBEAMCONF_DOC} ],
                  'SetPoint' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                                 {'description' : SETPOINT_DOC} ],
                  'Mode' : [ [ PyTango.ArgType.DevString ,
                                    PyTango.AttrDataFormat.SCALAR ,
                                    PyTango.AttrWriteType.READ_WRITE],
                             {'description' : MODE_DOC} ],
                  'Tau' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                            {'description' : TAU_DOC} ],
                  'SoftBeam' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                 {'description' : SOFTBEAM_DOC} ],
                  'OperationFlags' : [ [ PyTango.ArgType.DevString,
                                  PyTango.AttrDataFormat.SPECTRUM,
                                  PyTango.AttrWriteType.READ, 7 ], 
                                       {'description' : OPERATIONFLAGS_DOC} ],
                  'Beam' : [ [ PyTango.ArgType.DevString,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "Beam"} ],
                  'FBeam' : [ [ PyTango.ArgType.DevString,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "FBeam"} ],                                 
                  'Beam_In' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "Beam_In"} ],
                  'Beam_Out' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "Beam_Out"} ],
                  'FBeam_In' : [ [ PyTango.ArgType.DevDouble, 
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "FBeam_In"} ],
                  'FBeam_Out' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : "FBeam_Out"} ],                                    
                  'MocoState' : [ [ PyTango.ArgType.DevString,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ ],
                                  {'description' : MOCOSTATE_DOC} ],
                  'Piezo' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                              {'description' : PIEZO_DOC}],
                  'ScanSpeed' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                                 {'description' : SCANSPEED_DOC} ],
                  'OscBeamMainSignal' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                                    {'description' : OSCBEAMMAINSIGNAL_DOC} ],
                  'OscBeamQuadSignal' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                                    {'description' : OSCBEAMQUADSIGNAL_DOC} ],
                  'Phase' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                              {'description' : PHASE_DOC} ],
                  'Amplitude' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ], 
                                  {'description' : AMPLITUDE_DOC} ],
                  'Frequency' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                                  {'description' : FREQUENCY_DOC} ],
                  'Slope' : [ [ PyTango.ArgType.DevDouble,
                                  PyTango.AttrDataFormat.SCALAR,
                                  PyTango.AttrWriteType.READ_WRITE ],
                              {'description' : SLOPE_DOC} ]


    }
    
    #    Device Properties
    device_property_list = {'serialDevice': [PyTango.DevString,
                                            "name of the system serial device",
                                            [] ],
                            'softwareInBeamAttr': [PyTango.DevString,
                                            "name of the Tango attribute of the in beam",
                                            [] ],
                           }


class Moco(PyTango.Device_4Impl):

    def __init__(self,cl,name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        self.info_stream('In Moco.__init__')
        Moco.init_device(self)

    def init_device(self):
        self.info_stream('In Python init_device method')
        self.get_device_properties(self.get_device_class())
        self.debug_stream("serialDevice: %s; softwareInBeamAttr%s" % (self.serialDevice,self.softwareInBeamAttr))
        self.moco = serial.Serial(self.serialDevice)
        self.moco.timeout = 1.5
        self.moco.open()
        if self.moco.isOpen():
            self.set_state(PyTango.DevState.ON)
        else:
            self.set_state(PyTango.DevState.ALARM)
            self.set_status("Unbable to open serial connection.")
        self.inBeamAttr = None
        if hasattr(self, 'softwareInBeamAtt'):
            self.inBeamAttr = PyTango.AttributeProxy(self.softwareInBeamAttr)

    #------------------------------------------------------------------

    def delete_device(self):
        self.info_stream('Moco.delete_device')
        if self.moco.isOpen():
            self.moco.close()

    #------------------------------------------------------------------
    # COMMANDS
    #------------------------------------------------------------------

    def is_RestoreSoftInBeam_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def RestoreSoftInBeam(self):
        inBeam = self.inBeamAttr.read().value
        if hasattr(self, 'softwareInBeamAtt'):
            self.debug_stream("Setting softbeam to %f" % float(inBeam))
            self.setToMoco("SOFTBEAM %f" % float(inBeam))
        else:
            raise Exception("Error: softwareInBeamAttr is not defined")
           
    def is_Tune_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Tune(self):
        self.setToMoco("TUNE")

    def is_TunePeak_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def TunePeak(self):
        self.setToMoco("TUNE PEAK")

    def is_Go_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Go(self):
        self.setToMoco("GO")

    def is_Stop_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Stop(self):
        self.setToMoco("STOP")

    def is_Pause_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Pause(self, arg):
        self.setToMoco("PAUSE %s" % arg)
      
    def is_SetOperationFlags_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def SetOperationFlags(self, args):
        flags = " ".join(args)
        self.setToMoco("SET %s" % flags)
    
    def is_ClearOperationFlags_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def ClearOperationFlags(self, args):
        self.debug_stream("arg: %s" % repr(args))
        flags = " ".join(args)
        self.debug_stream("flags: %s" % repr(flags))
        self.setToMoco("CLEAR %s" % flags)

    def is_GetInfo_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def GetInfo(self):
        info = self.getFromMoco("?INFO")
        info = [line[:-2] for line in info] #getting rid of last ascii characters "\r\n"
        self.debug_stream("Info: %s" % repr(info))
        return info

    def is_Reset_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def Reset(self):
        self.setToMoco("RESET")
    
    def is_OnlineCmd_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def OnlineCmd(self, arg):
        self.debug_stream("OnlineCmd %s" % arg)
        if arg.startswith('?'):
            ans = self.getFromMoco(arg)
            self.debug_stream("ans = %s" % repr(ans))
            if isinstance(ans, str):
                ans = [ans]
            ans = [line[:-2] for line in ans] #getting rid of last ascii characters "\r\n"
        else:
            self.setToMoco(arg)
            ans = []
        return ans
        
    def is_OscilOn_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def OscilOn(self):
        self.setToMoco("OSCIL ON")
        
    def is_OscilOff_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    def OscilOff(self):
        self.setToMoco("OSCIL OFF")

    #------------------------------------------------------------------
    # ATTRIBUTES
    #------------------------------------------------------------------

    def read_attr_hardware(self, data):
        self.info_stream('In read_attr_hardware')

    def read_InBeamConf(self, the_att):
        self.info_stream("read_InBeamConf")
        ans = self.getFromMoco("?INBEAM")
        inBeamConf = ans[:-2]
        the_att.set_value(inBeamConf)

    def write_InBeamConf(self, the_att):
        self.info_stream("write_InBeamConf")
        conf = the_att.get_write_value()
        self.setToMoco("INBEAM %s" % conf)

    def is_InBeamConf_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_OutBeamConf(self, the_att):
        self.info_stream("read_OutBeamConf")
        ans = self.getFromMoco("?OUTBEAM")
        inBeamConf = ans[:-2]
        the_att.set_value(inBeamConf)

    def write_OutBeamConf(self, the_att):
        self.info_stream("write_OutBeamConf")
        conf = the_att.get_write_value()
        self.setToMoco("OUTBEAM %s" % conf)

    def is_OutBeamConf_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_SetPoint(self, the_att):
        self.info_stream("read_SetPoint")
        ans = self.getFromMoco('?SETPOINT')
        setPoint = float(ans[:-2])
        self.debug_stream("SetPoint = %f" % setPoint)
        the_att.set_value(setPoint)

    def write_SetPoint(self, the_att):
        self.info_stream("write_SetPoint")
        setPoint = the_att.get_write_value()
        self.setToMoco("SETPOINT %f" % setPoint)

    def is_SetPoint_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Mode(self, the_att):
        self.info_stream("read_Mode")
        ans = self.getFromMoco("?MODE")
        mode = ans[:-2]
        the_att.set_value(mode)

    def write_Mode(self, the_att):
        self.info_stream("write_Mode")
        conf = the_att.get_write_value()
        self.setToMoco("MODE %s" % conf)

    def is_OutBeamConf_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Tau(self, the_att):
        self.info_stream("read_Tau")
        ans = self.getFromMoco('?TAU')
        tau = float(ans[:-2])
        self.debug_stream("Tau = %f" % tau)
        the_att.set_value(tau)

    def write_Tau(self, the_att):
        self.info_stream("write_Tau")
        tau = the_att.get_write_value()
        self.setToMoco("TAU %f" % tau)

    def is_Tau_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_SoftBeam(self, the_att):
        self.info_stream("read_Tau")
        ans = self.getFromMoco('?SOFTBEAM')
        softBeam = float(ans[:-2])
        self.debug_stream("SoftBeam = %f" % softBeam)
        the_att.set_value(softBeam)

    def write_SoftBeam(self, the_att):
        self.info_stream("write_Tau")
        softBeam = the_att.get_write_value()
        self.setToMoco("SOFTBEAM %f" % softBeam)

    def is_SoftBeam_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_OperationFlags(self, the_att):
        self.info_stream("read_Set")
        ans = self.getFromMoco('?SET')
        set_ = ans[:-2]
        sets = set_.split()
        self.debug_stream("Set = %s" % set_)
        self.debug_stream("Sets = %s" % sets)
        the_att.set_value(sets)

    def is_OperationFlags_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Beam(self, the_att):
        self.info_stream("read_Beam")
        ans = self.getFromMoco('?BEAM')
        beam = ans[:-2]
        self.debug_stream("Beam = %s" % beam)
        the_att.set_value(beam)

    def is_Beam_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_FBeam(self, the_att):
        self.info_stream("read_FBeam")
        ans = self.getFromMoco('?FBEAM')
        beam = ans[:-2]
        self.debug_stream("FBeam = %s" % beam)
        the_att.set_value(beam)

    def is_FBeam_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)
    
    
    def read_Beam_In(self, the_att):
        self.info_stream("read_Beam_In")
        ans = self.getFromMoco('?BEAM')
        beam = ans[:-2]
        beam = beam.split(" ")[0]
	beam = float(beam)
        self.debug_stream("Beam_In = %f" % beam)
        the_att.set_value(beam)

    def is_Beam_In_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)
  
    def read_Beam_Out(self, the_att):
        self.info_stream("read_Beam_Out")
        ans = self.getFromMoco('?BEAM')
        beam = ans[:-2]
        beam = beam.split(" ")[1]
	beam = float(beam)
        self.debug_stream("Beam_Out = %f" % beam)
        the_att.set_value(beam)

    def is_Beam_Out_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)


    def read_FBeam_In(self, the_att): 
        self.info_stream("read_FBeam_In")
        ans = self.getFromMoco('?FBEAM')
        beam = ans[:-2]
        beam = beam.split(" ")[0]
	beam = float(beam)
        self.debug_stream("FBeam_In = %f" % beam)
        the_att.set_value(beam)

    def is_FBeam_In_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,) 
    
    
    def read_FBeam_Out(self, the_att):
        self.info_stream("read_FBeam_Out")
        ans = self.getFromMoco('?FBEAM')
        beam = ans[:-2]
        beam = beam.split(" ")[1]
	beam = float(beam)
        self.debug_stream("FBeam_Out = %f" % beam)
        the_att.set_value(beam) 

    def is_FBeam_Out_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,) 
    

    def read_MocoState(self, the_att):
        self.info_stream("read_MocoState")
        ans = self.getFromMoco('?STATE')
        state = ans[:-2]
        self.debug_stream("State = %s" % state)
        the_att.set_value(state)

    def is_MocoState_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Piezo(self, the_att):
        self.info_stream("read_Piezo")
        ans = self.getFromMoco('?PIEZO')
        piezo = float(ans[:-2])
        self.debug_stream("Piezo = %f" % piezo)
        the_att.set_value(piezo)

    def write_Piezo(self, the_att):
        self.info_stream("write_Piezo")
        piezo = the_att.get_write_value()
        self.setToMoco("PIEZO %f" % piezo)

    def is_Piezo_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_ScanSpeed(self, the_att):
        self.info_stream("read_ScanSpeed")
        ans = self.getFromMoco('?SPEED')
        speed = float(ans[:-2].split()[0])
        self.debug_stream("ScanSpeed = %f" % speed)
        the_att.set_value(speed)

    def write_ScanSpeed(self, the_att):
        self.info_stream("write_ScanSpeed")
        speed = the_att.get_write_value()
        self.setToMoco("SPEED %f" % speed)

    def is_SpeedScan_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_OscBeamMainSignal(self, the_att):
        self.info_stream("read_OscBeamMainSignal")
        ans = self.getFromMoco('?OSCBEAM')
        values = ans[:-2].split()
        mainSignal = float(values[0])
        self.debug_stream("mainSignal: %f" % mainSignal)
        the_att.set_value(mainSignal)

    def is_OscBeamMainSignal_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_OscBeamQuadSignal(self, the_att):
        self.info_stream("read_OscBeamQuadSignal")
        ans = self.getFromMoco('?OSCBEAM')
        values = ans[:-2].split()
        quadSignal = float(values[1])
        self.debug_stream("quadSignal: %f" % quadSignal)
        the_att.set_value(quadSignal)

    def is_OscBeamQuadSignal_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Phase(self, the_att):
        self.info_stream("read_Phase")
        ans = self.getFromMoco('?PHASE')
        phase = float(ans[:-2])
        self.debug_stream("phase: %f" % phase)
        the_att.set_value(phase)

    def write_Phase(self, the_att):
        self.info_stream("write_Phase")
        phase = the_att.get_write_value()
        self.setToMoco("PHASE %f" % phase)

    def is_Phase_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Amplitude(self, the_att):
        self.info_stream("read_Amplitude")
        ans = self.getFromMoco('?AMPLITUDE')
        amplitude = float(ans[:-2])
        self.debug_stream("amplitude: %f" % amplitude)
        the_att.set_value(amplitude)

    def write_Amplitude(self, the_att):
        self.info_stream("write_Amplitude")
        amplitude = the_att.get_write_value()
        self.setToMoco("Amplitude %f" % amplitude)

    def is_Amplitude_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Frequency(self, the_att):
        self.info_stream("read_Frequency")
        ans = self.getFromMoco('?FREQUENCY')
        frequency = float(ans[:-2])
        self.debug_stream("frequency: %f" % frequency)
        the_att.set_value(frequency)

    def write_Frequency(self, the_att):
        self.info_stream("write_Frequency")
        frequency = the_att.get_write_value()
        self.setToMoco("FREQUENCY %f" % frequency)

    def is_Frequency_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

    def read_Slope(self, the_att):
        self.info_stream("read_Slope")
        ans = self.getFromMoco('?SLOPE')
        slope = float(ans[:-2])
        self.debug_stream("slope: %f" % slope)
        the_att.set_value(slope)

    def write_Slope(self, the_att):
        self.info_stream("write_Slope")
        slope = the_att.get_write_value()
        self.setToMoco("SLOPE %f" % slope)

    def is_Slope_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)
    
    #-------------------------------------------------------------------
    # ADITIONAL METHODS
    #-------------------------------------------------------------------

    def setToMoco(self, cmd):
        self.info_stream("setToMoco: %s" % cmd)
        self.moco.write(cmd + "\r")
        self.moco.write("?ERR\r")
        ans = self.moco.readline()
        if ans != "OK\r\n":
            raise Exception("Error: %s" % ans)    

    def getFromMoco(self, cmd):
        MULTILINE_CMDS = ["?HELP", "?INFO"]
        self.moco.write(cmd + "\r")
        if cmd in MULTILINE_CMDS:
            ans = self.moco.readlines()
        else:
            ans = self.moco.readline()
        if ans == "ERROR\r\n":
            self.moco.write("?ERR\r")
            ans = self.moco.readline()
            raise Exception("Error: %s" % ans)
        else:
            self.info_stream("getFromMoco: %s" % ans)
            return ans

def main():
    util = PyTango.Util(sys.argv)
    util.add_class(MocoClass, Moco)

    U = PyTango.Util.instance()
    U.server_init()
    U.server_run()

if __name__ == '__main__':
    main()