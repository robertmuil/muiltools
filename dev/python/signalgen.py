#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ***************************************************************************
# *   Copyright (C) 2011, Paul Lutus                                        *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program; if not, write to the                         *
# *   Free Software Foundation, Inc.,                                       *
# *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
# ***************************************************************************

# version date 01-12-2011

VERSION = '1.1'

import re, sys, os

import gobject
gobject.threads_init()
import gst
import gtk
gtk.gdk.threads_init()
import time
import struct
import math
import random
import signal
import webbrowser

class Icon:
  icon = [
    "32 32 17 1",
    "   c None",
    ".  c #2A2E30",
    "+  c #333739",
    "@  c #464A4C",
    "#  c #855023",
    "$  c #575A59",
    "%  c #676A69",
    "&  c #CCFF00",
    "*  c #777A78",
    "=  c #DB731A",
    "-  c #8A8C8A",
    ";  c #969895",
    ">  c #F68C22",
    ",  c #A5A7A4",
    "'  c #F49D4A",
    ")  c #B3B5B2",
    "!  c #DEE0DD",
    "                        &&&&&&& ",
    "                  &&&===='''''& ",
    "                  &'''''====&'& ",
    "             +++++&'&&&&&   &'& ",
    "          +@$%****&'&+      &'& ",
    "        +@**%$@++@&'&*@+    &'& ",
    "      +@**@+++++++&'&@**@+  &'& ",
    "     +$*$+++++++++&'&++$*$+ &'& ",
    "     @*@++++++++++&'&+++@#&&&'& ",
    "    +*@++++++++#&&&'&+++#=''''& ",
    "   +*$++++++++#=''''&+++&'>>>'& ",
    "   @*+++++++++&'>>>'&+++#='''=  ",
    "  +%$++++++++@#='''=#@@++#&&&#  ",
    "  +*@+++++++@@@#&&&#@@@@@++@*+  ",
    "  +*+++++++@@@@++@$%$$@@@@++*+  ",
    "  +*++++++@@+@;,,*@@*$$$@@@+*+  ",
    "  +*@++++@@@%!!!!,;@$*$$$@@@*+  ",
    "  +%$++++@@+)!!!),-*+-%$$$@$%+  ",
    "  +@*+++@@@+-!!!,;-%@;%%$$+*@+  ",
    "   +*@++@@@@+$*-*%@+*-%%$@@*+   ",
    "   ++*@+@@@$$%@++@%;;*%%$@-$+   ",
    "    +@%+@@@$$%*;;;;-*%%%@**+    ",
    "    .+$%@@@$$$*******%$$*-+.    ",
    "     .+@%%@@$$*@*@%%%$%-%+.     ",
    "      .++@%$$$$$$%%%%--@+.      ",
    "        +++@@$%*****%+++        ",
    "         +++++++++++++@.        ",
    "          @--%@++@$*-%+         ",
    "           +%,))),;%+.          ",
    "             ++++++.            ",
    "                                ",
    "                                "
  ]

# this should be a temporary hack

class WidgetFinder:
  def localize_widgets(self,parent,xmlfile):
    # an unbelievable hack made necessary by
    # someone unwilling to fix a year-old bug
    with open(xmlfile) as f:
      for name in re.findall('(?s) id="(.*?)"',f.read()):
        if re.search('^k_',name):
          obj = parent.builder.get_object(name)
          setattr(parent,name,obj)

class ConfigManager:
  def __init__(self,path,dic):
    self.path = path
    self.dic = dic

  def read_config(self):
    if os.path.exists(self.path):
      with open(self.path) as f:
        for record in f.readlines():
          se = re.search('(.*?)\s*=\s*(.*)',record.strip())
          if(se):
            key,value = se.groups()
            if (key in self.dic):
              widget = self.dic[key]
              typ = type(widget)
              if(typ == list):
                widget[0] = value
              elif(typ == gtk.Entry):
                widget.set_text(value)
              elif(typ == gtk.HScale):
                widget.set_value(float(value))
              elif(typ == gtk.Window):
                w,h = value.split(',')
                widget.resize(int(w),int(h))
              elif(typ == gtk.CheckButton or typ == gtk.RadioButton or typ == gtk.ToggleButton):
                widget.set_active(value == 'True')
              elif(typ == gtk.ComboBox):
                if(value in widget.datalist):
                  i = widget.datalist.index(value)
                  widget.set_active(i)
              else:
                print("ERROR: reading, cannot identify key %s with type %s" % (key,type(widget)))

  def write_config(self):
    with open(self.path,'w') as f:
      for key,widget in sorted(self.dic.items()):
        typ = type(widget)
        if(typ == list):
          value = widget[0]
        elif(typ == gtk.Entry):
          value = widget.get_text()
        elif(typ == gtk.HScale):
          value = str(widget.get_value())
        elif(typ == gtk.Window):
          _,_,w,h = widget.get_allocation()
          value = "%d,%d" % (w,h)
        elif(typ == gtk.CheckButton or typ == gtk.RadioButton or typ == gtk.ToggleButton):
          value = ('False','True')[widget.get_active()]
        elif(typ == gtk.ComboBox):
          value = widget.get_active_text()
        else:
          print("ERROR: writing, cannot identify key %s with type %s" % (key,type(widget)))
          value = "Error"
        f.write("%s = %s\n" % (key,value))

  def preset_combobox(self,box,v):
    if(v in box.datalist):
      i = box.datalist.index(v)
      box.set_active(i)
    else:
      box.set_active(0)

  def load_combobox(self,obj,data):
    if(len(obj.get_cells()) == 0):
      # Create a text cell renderer
      cell = gtk.CellRendererText ()
      obj.pack_start(cell)
      obj.add_attribute (cell, "text", 0)
    obj.get_model().clear()
    for s in data:
      obj.append_text(s.strip())
    setattr(obj,'datalist',data)

class TextEntryController:
  def __init__(self,parent,widget):
    self.par = parent
    self.widget = widget
    widget.connect('scroll-event',self.scroll_event)
    widget.set_tooltip_text('Enter number or:\n\
    Mouse wheel: increase,decrease\n\
    Shift/Ctrl/Alt: faster change')

  def scroll_event(self,w,evt):
    q = (-1,1)[evt.direction == gtk.gdk.SCROLL_UP]
    # magnify change if shift,ctrl,alt pressed
    for m in (1,2,4):
      if(self.par.mod_key_val & m): q *= 10
    s = self.widget.get_text()
    v = float(s)
    v += q
    v = max(0,v)
    s = self.par.format_num(v)
    self.widget.set_text(s)

class SignalGen:
  M_AM,M_FM = list(range(2))
  W_SINE,W_TRIANGLE,W_SQUARE,W_SAWTOOTH = list(range(4))
  waveform_strings = ('Sine','Triangle','Square','Sawtooth')
  R_48000,R_44100,R_22050,R_16000,R_11025,R_8000,R_4000 = list(range(7))
  sample_rates = ('48000','44100','22050','16000', '11025', '8000', '4000')
  def __init__(self):
    self.restart = False
    # exit correctly on system signals
    signal.signal(signal.SIGTERM, self.close)
    signal.signal(signal.SIGINT, self.close)
    # precompile struct operator
    self.struct_int = struct.Struct('i')
    self.max_level = (2.0**31)-1
    self.gen_functions = (
      self.sine_function,
      self.triangle_function,
      self.square_function,
      self.sawtooth_function
    )
    self.main_color = gtk.gdk.color_parse('#c04040')
    self.sig_color = gtk.gdk.color_parse('#40c040')
    self.mod_color = gtk.gdk.color_parse('#4040c0')
    self.noise_color = gtk.gdk.color_parse('#c040c0')
    self.pipeline = False
    self.count = 0
    self.imod = 0
    self.rate = 1
    self.mod_key_val = 0
    self.sig_freq = 440
    self.mod_freq = 3
    self.sig_level = 100
    self.mod_level = 100
    self.noise_level = 100
    self.enable = False
    self.sig_waveform = SignalGen.W_SINE
    self.sig_enable = True
    self.sig_function = False
    self.mod_waveform = SignalGen.W_SINE
    self.mod_function = False
    self.mod_mode = SignalGen.M_AM
    self.mod_enable = False
    self.noise_enable = False
    self.sample_rate = SignalGen.R_22050
    self.left_audio  = True
    self.right_audio = True
    self.program_name = self.__class__.__name__
    self.config_file = os.path.expanduser("~/." + self.program_name)
    self.builder = gtk.Builder()
    self.xmlfile = 'signalgen_gui.glade'
    self.builder.add_from_file(self.xmlfile)
    WidgetFinder().localize_widgets(self,self.xmlfile)
    self.k_quit_button.connect('clicked',self.close)
    self.k_help_button.connect('clicked',self.launch_help)
    self.k_mainwindow.connect('destroy',self.close)
    self.k_mainwindow.set_icon(gtk.gdk.pixbuf_new_from_xpm_data(Icon.icon))
    self.title = self.program_name + ' ' + VERSION
    self.k_mainwindow.set_title(self.title)
    self.tooltips = {
      self.k_sample_rate_combobox : 'Change data sampling rate',
      self.k_left_checkbutton : 'Enable left channel audio',
      self.k_right_checkbutton : 'Enable right channel audio',
      self.k_sig_waveform_combobox : 'Select signal waveform',
      self.k_mod_waveform_combobox : 'Select modulation waveform',
      self.k_mod_enable_checkbutton  : 'Enable modulation',
      self.k_sig_enable_checkbutton  : 'Enable signal',
      self.k_noise_enable_checkbutton  : 'Enable white noise',
      self.k_mod_am_radiobutton : 'Enable amplitude modulation',
      self.k_mod_fm_radiobutton : 'Enable frequency modulation',
      self.k_quit_button : 'Quit %s' % self.title,
      self.k_enable_checkbutton : 'Enable output',
      self.k_help_button : 'Visit the %s Web page' % self.title,
    }
    for k,v in self.tooltips.items():
      k.set_tooltip_text(v)
    self.config_data = {
      'SampleRate' : self.k_sample_rate_combobox,
      'LeftChannelEnabled' : self.k_left_checkbutton,
      'RightChannelEnabled' : self.k_right_checkbutton,
      'SignalWaveform' : self.k_sig_waveform_combobox,
      'SignalFrequency' : self.k_sig_freq_entry,
      'SignalLevel' : self.k_sig_level_entry,
      'SignalEnabled' : self.k_sig_enable_checkbutton,
      'ModulationWaveform' : self.k_mod_waveform_combobox,
      'ModulationFrequency' : self.k_mod_freq_entry,
      'ModulationLevel' : self.k_mod_level_entry,
      'ModulationEnabled' : self.k_mod_enable_checkbutton,
      'AmplitudeModulation' : self.k_mod_am_radiobutton,
      'FrequencyModulation' : self.k_mod_fm_radiobutton,
      'NoiseEnabled' : self.k_noise_enable_checkbutton,
      'NoiseLevel' : self.k_noise_level_entry,
      'OutputEnabled' : self.k_enable_checkbutton,
    }
    self.cm = ConfigManager(self.config_file,self.config_data)
    self.cm.load_combobox(self.k_sig_waveform_combobox,self.waveform_strings)
    self.k_sig_waveform_combobox.set_active(self.sig_waveform)
    self.cm.load_combobox(self.k_mod_waveform_combobox,self.waveform_strings)
    self.k_mod_waveform_combobox.set_active(self.mod_waveform)
    self.cm.load_combobox(self.k_sample_rate_combobox,self.sample_rates)
    self.k_sample_rate_combobox.set_active(self.sample_rate)
    self.k_sig_freq_entry.set_text(self.format_num(self.sig_freq))
    self.k_sig_level_entry.set_text(self.format_num(self.sig_level))
    self.k_mod_freq_entry.set_text(self.format_num(self.mod_freq))
    self.k_mod_level_entry.set_text(self.format_num(self.mod_level))
    self.k_noise_level_entry.set_text(self.format_num(self.noise_level))
    self.k_main_viewport_border.modify_bg(gtk.STATE_NORMAL,self.main_color)
    self.k_sig_viewport_border.modify_bg(gtk.STATE_NORMAL,self.sig_color)
    self.k_mod_viewport_border.modify_bg(gtk.STATE_NORMAL,self.mod_color)
    self.k_noise_viewport_border.modify_bg(gtk.STATE_NORMAL,self.noise_color)
    self.sig_freq_cont = TextEntryController(self,self.k_sig_freq_entry)
    self.sig_level_cont = TextEntryController(self,self.k_sig_level_entry)
    self.mod_freq_cont = TextEntryController(self,self.k_mod_freq_entry)
    self.mod_level_cont = TextEntryController(self,self.k_mod_level_entry)
    self.noise_level_cont = TextEntryController(self,self.k_noise_level_entry)
    self.k_mainwindow.connect('key-press-event',self.key_event)
    self.k_mainwindow.connect('key-release-event',self.key_event)
    self.k_enable_checkbutton.connect('toggled',self.update_values)
    self.k_sig_freq_entry.connect('changed',self.update_entry_values)
    self.k_sig_level_entry.connect('changed',self.update_entry_values)
    self.k_sig_enable_checkbutton.connect('toggled',self.update_checkbutton_values)
    self.k_mod_freq_entry.connect('changed',self.update_entry_values)
    self.k_mod_level_entry.connect('changed',self.update_entry_values)
    self.k_noise_level_entry.connect('changed',self.update_entry_values)
    self.k_sample_rate_combobox.connect('changed',self.update_values)
    self.k_sig_waveform_combobox.connect('changed',self.update_values)
    self.k_mod_waveform_combobox.connect('changed',self.update_values)
    self.k_left_checkbutton.connect('toggled',self.update_checkbutton_values)
    self.k_right_checkbutton.connect('toggled',self.update_checkbutton_values)
    self.k_mod_enable_checkbutton.connect('toggled',self.update_checkbutton_values)
    self.k_noise_enable_checkbutton.connect('toggled',self.update_checkbutton_values)
    self.k_mod_am_radiobutton.connect('toggled',self.update_checkbutton_values)
    self.cm.read_config()
    self.update_entry_values()
    self.update_checkbutton_values()
    self.update_values()

  def format_num(self,v):
    return "%.2f" % v

  def get_widget_text(self,w):
    typ = type(w)
    if(typ == gtk.ComboBox):
      return w.get_active_text()
    elif(typ == gtk.Entry):
      return w.get_text()

  def get_widget_num(self,w):
    try:
      return float(self.get_widget_text(w))
    except:
      return 0.0

  def restart_test(self,w,pv):
    nv = w.get_active()
    self.restart |= (nv != pv)
    return nv
    
  def update_entry_values(self,*args):
    self.sig_freq = self.get_widget_num(self.k_sig_freq_entry)
    self.sig_level = self.get_widget_num(self.k_sig_level_entry) / 100.0
    self.mod_freq = self.get_widget_num(self.k_mod_freq_entry)
    self.mod_level = self.get_widget_num(self.k_mod_level_entry) / 100.0
    self.noise_level = self.get_widget_num(self.k_noise_level_entry) / 100.0
    
  def update_checkbutton_values(self,*args):
    self.left_audio = self.k_left_checkbutton.get_active()
    self.right_audio = self.k_right_checkbutton.get_active()
    self.mod_enable = self.k_mod_enable_checkbutton.get_active()
    self.sig_enable = self.k_sig_enable_checkbutton.get_active()
    self.mod_mode = (SignalGen.M_FM,SignalGen.M_AM)[self.k_mod_am_radiobutton.get_active()]
    self.noise_enable = self.k_noise_enable_checkbutton.get_active()
    
  def update_values(self,*args):
    self.restart = (not self.sig_function)
    self.sample_rate = self.restart_test(self.k_sample_rate_combobox, self.sample_rate)
    self.enable = self.restart_test(self.k_enable_checkbutton,self.enable)
    self.mod_waveform = self.k_mod_waveform_combobox.get_active()
    self.mod_function = self.gen_functions[self.mod_waveform]
    self.sig_waveform = self.k_sig_waveform_combobox.get_active()
    self.sig_function = self.gen_functions[self.sig_waveform]
    self.k_sample_rate_combobox.set_sensitive(not self.enable)
    if(self.restart):
      self.init_audio()
      
  def make_and_chain(self,name):
    target = gst.element_factory_make(name)
    self.chain.append(target)
    return target

  def unlink_gst(self):
    if(self.pipeline):
      self.pipeline.set_state(gst.STATE_NULL)
      self.pipeline.remove_many(*self.chain)
      gst.element_unlink_many(*self.chain)
      for item in self.chain:
        item = False
      self.pipeline = False
      time.sleep(0.01)

  def init_audio(self):
    self.unlink_gst()
    if(self.enable):
      self.chain = []
      self.pipeline = gst.Pipeline("mypipeline")
      self.source = self.make_and_chain("appsrc")
      rs = SignalGen.sample_rates[self.sample_rate]
      self.rate = float(rs)
      self.interval = 1.0 / self.rate
      caps = gst.Caps(
      'audio/x-raw-int,'
      'endianness=(int)1234,'
      'channels=(int)2,'
      'width=(int)32,'
      'depth=(int)32,'
      'signed=(boolean)true,'
      'rate=(int)%s' % rs)
      self.source.set_property('caps', caps)
      self.sink = self.make_and_chain("autoaudiosink")
      self.pipeline.add(*self.chain)
      gst.element_link_many(*self.chain)
      self.source.connect('need-data', self.need_data)
      self.pipeline.set_state(gst.STATE_PLAYING)
      
  def key_event(self,w,evt):
    cn = gtk.gdk.keyval_name(evt.keyval)
    if(re.search('Shift',cn) != None):
      mod = 1
    elif(re.search('Control',cn) != None):
      mod = 2
    elif(re.search('Alt|Meta',cn) != None):
      mod = 4
    else:
      return
    if(evt.type == gtk.gdk.KEY_PRESS):
      self.mod_key_val |= mod
    else:
      self.mod_key_val &= ~mod

  def sine_function(self,t,f):
    return math.sin(2.0*math.pi*f*t)

  def triangle_function(self,t,f):
    q = 4*math.fmod(t*f,1)
    q = (q,2-q)[q > 1]
    return (q,-2-q)[q < -1]

  def square_function(self,t,f):
    if(f == 0): return 0
    q = 0.5 - math.fmod(t*f,1)
    return (-1,1)[q > 0]

  def sawtooth_function(self,t,f):
    return 2.0*math.fmod((t*f)+0.5,1.0)-1.0

  def need_data(self,src,length):
    bytes = ""
    # sending two channels, so divide requested length by 2
    ld2 = length / 2
    for tt in range(ld2):
      t = (self.count + tt) * self.interval
      if(not self.mod_enable):
        datum = self.sig_function(t,self.sig_freq)
      else:
        mod = self.mod_function(t,self.mod_freq)
        # AM mode
        if(self.mod_mode == SignalGen.M_AM):
          datum = 0.5 * self.sig_function(t,self.sig_freq) * (1.0 + (mod * self.mod_level))
        # FM mode
        else:
          self.imod += (mod * self.mod_level * self.interval)
          datum = self.sig_function(t+self.imod,self.sig_freq)
      v = 0
      if(self.sig_enable):
        v += (datum * self.sig_level)
      if(self.noise_enable):
        noise = ((2.0 * random.random()) - 1.0)
        v += noise * self.noise_level
      v *= self.max_level
      v = max(-self.max_level,v)
      v = min(self.max_level,v)
      left  = (0,v)[self.left_audio]
      right = (0,v)[self.right_audio]
      bytes += self.struct_int.pack(left)
      bytes += self.struct_int.pack(right)
    self.count += ld2
    src.emit('push-buffer', gst.Buffer(bytes))
    
  def launch_help(self,*args):
    webbrowser.open("http://arachnoid.com/python/signalgen_program.html")

  def close(self,*args):
    self.unlink_gst()
    self.cm.write_config()
    gtk.main_quit()

app=SignalGen()
gtk.main()
