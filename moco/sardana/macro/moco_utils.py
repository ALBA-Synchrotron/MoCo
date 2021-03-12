# -*- coding: utf-8 -*-
#
# This file is part of the MoCo project
#
# Copyright (c) 2020 ALBA controls team
# Distributed under the GNU General Public License v3.
# See LICENSE for more info.

import functools
import tango
from contextlib import contextmanager
from click import style

from sardana.macroserver.macro import Type, macro, Optional

TangoDevice = functools.lru_cache(maxsize=512)(tango.DeviceProxy)


def get_device_names_by_class(class_name, server="*"):
    """
    Return list of device names for the given class name
    The list can be filtered by server. By default the
    search is performed on all servers.
    """
    db = tango.Database()
    result = []
    for server_name in db.get_server_list(server):
        dev_class = db.get_device_class_list(server_name)
        for dname, cname in zip(dev_class[::2], dev_class[1::2]):
            if cname == class_name:
                result.append(dname)
    return result


def get_device_name_by_class(class_name, server="*"):
    """
    Return device name for the given class name.
    The list can be filtered by server. By default the
    search is performed on all servers.
    """
    devices = get_device_names_by_class(class_name, server)
    if devices:
        if len(devices) == 1:
            return devices[0]
        else:
            raise ValueError(
                "More than one device of type {!} found".format(class_name)
            )
    else:
        raise ValueError("No device of type {!r} found".format(class_name))



@contextmanager
def output_context(macro, message):
    """
    Print "message" when entering context and " [DONE]/[ERROR]" in the same line
    when exiting context.

    """
    macro.outputBlock(message)
    try:
        yield
    except Exception as error:
        msg = "{} [{}]".format(message, style("ERROR. Check if it is ON",
                                              fg="red"))
        macro.outputBlock(msg)
        raise
    else:
        msg = "{} [{}]".format(message, style("DONE", fg="green"))
        macro.outputBlock(msg)


class Moco:

    def __init__(self, name=None):
        if name is None:
            name = get_device_name_by_class("Moco", "Moco/*")
        self.name = name

    @property
    def device(self):
        return TangoDevice(self.name)

    # By default, delegate methods and properties to tango directly
    def __getattr__(self, name):
        return getattr(self.device, name)

    def __repr__(self):
        try:
           return self.device.info()
        except Exception as error:
            return "Moco: {!r}".format(error)


moco = Moco()


@macro()
def moco_info(self):
    with output_context(self, 'Moco reading status info...'):
        info = '\n'.join(moco.getinfo())
        self.output(info)


@macro(result_def=[['status', Type.String, None, 'Moco state']])
def moco_status(self):
    with output_context(self, 'Moco reading state...'):
        return moco.MocoState


@macro()
def moco_go(self):
    with output_context(self, "Moco sending Go..."):
        moco.go()


@macro()
def moco_stop(self):
    with output_context(self, "Moco stopping..."):
        moco.stop()


@macro(param_def=[['config', Type.String, Optional,
                  'Configuration parameter see INBEAM/?INBEAM command']],
       result_def=[['config', Type.String, None, 'Current configuration']])
def moco_inbeam_conf(self, config):
    if config is not None:
        with output_context(self, 'Moco setting InBeamConfig "{}"...'.format(
                config)):
            moco.write_attribute('InBeamConf', config)
    else:
        with output_context(self, 'Moco reading InBeamConfig...'):
            return moco.InBeamConf


@macro(param_def=[['cmd', Type.String, None, 'Command to send']])
def moco_cmd(self, cmd):
    with output_context(self, 'Moco running OnlineCommand "{}"'.format(
            cmd)):
        ans = moco.OnlineCmd(cmd)
        self.debug(ans)
        # TODO investigate how to return a list
        return moco.OnlineCmd(cmd)




