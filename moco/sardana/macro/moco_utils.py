from sardana.macroserver.macro import Type, Macro, UnknownEnv
import tango


class Moco(object):
    def __init__(self, macro_obj):
        self.macro = macro_obj
        try:
            moco_device_name = self.macro.getEnv('MocoDeviceName')
        except UnknownEnv:
            msg = 'The macro uses the environment variable MocoDeviceName ' \
                  'which has the instance name for the Moco Tango Device ' \
                  'Server.'
            raise RuntimeError(msg)
        self.dev = tango.DeviceProxy(moco_device_name)

    def cmd(self, cmd):
        try:
            ans = self.dev.OnlineCmd(cmd)
            return ans
        except Exception as e:
            self.macro.debug('Error %s', str(e))
            self.macro.error('Can not send the command %s. Check if it is on',
                             cmd)

    def set_piezo(self, pos):
        try:
            self.dev.write_attribute('piezo', pos)
        except Exception as e:
            self.macro.debug('Error %s', str(e))
            self.macro.error('Can not set the piezo pos to %f. '
                           'Check if it is on', pos)

    def go(self):
        try:
            self.dev.go()
        except Exception as e:
            self.macro.debug('Error %s', str(e))
            self.macro.error('Can not start moco. Check if it is on')

    def stop(self):
        try:
            self.dev.stop()
        except Exception as e:
            self.macro.debug('Error %s', str(e))
            self.macro.error('Can not stop moco. Check if it is on')

    def status(self):
        try:
            return self.dev.read_attribute('MocoState').value
        except Exception as e:
            self.macro.debug('Error %s', str(e))
            self.macro.error('Can not read status. Check if it is on')
            return 'FAULT'


class moco_cmd(Macro):
    param_def = [['cmd', Type.String, None, 'Command to send']]

    def run(self, cmd):
        moco = Moco(self)
        ans = moco.cmd(cmd)
        self.output(ans)


class set_moco_piezo(Macro):
    param_def = [['pos', Type.Float, None, 'position']]

    def run(self, pos):
        moco = Moco(self)
        moco.set_piezo(pos)


class moco_go(Macro):

    def run(self):
        moco = Moco(self)
        moco.go()


class moco_stop(Macro):

    def run(self):
        moco = Moco(self)
        moco.stop()


class moco_status(Macro):
    result_def = [['status', Type.String, None, 'Moco state']]

    def run(self):
        moco = Moco(self)
        return moco.status()
