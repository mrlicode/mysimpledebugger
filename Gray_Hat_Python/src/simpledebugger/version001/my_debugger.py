# coding: utf-8
'''
Created from 2016-07-15 22:51:54

@author: MrLi
@note: 定义要实现的功能
'''
from my_debugger_defines import *
from ctypes import *
kernel32 = windll.kernel32

class debugger(object):
    def __init__(self):
        
        self.h_process = None
        self.pid = None
        self.debugger_active = None #调试器是否活动
        
    def load(self, path_to_exe):
        # dwCreation flag determines how to create the Process
        # set creation_flags = CREATE_NEW_CONSOLE if you want 
        # to see the calculator GUI 
        creation_flags = DEBUG_PROCESS
        
        # instantiate the structs 
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the Debugger
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        # We then initialize the cb variavle in the STARTUPINFO struct.
        # which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)
        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print '[*] We have successfully launched the process!'
            print '[*] PID: %d ' % process_information.dwProcessId
            # Obtain a valid handle to the newly created process
            # and store it for future access
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print '[*] Error: 0x%09x.' % kernel32.GetLastError()
            
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process
            
    def attach(self, pid):
        h_process = self.open_process(pid)
        # We attempt to attach to the process
        # if this fails we exit the call
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print '[*] Unable to attach to the process.'
            print 'In attach, Error: ', kernel32.GetLastError()
            
    def run(self):
        # Now we have to poll the debuggee for
        # debugger events
        while self.debugger_active == True:
            self.get_debug_event()
            
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            # We are not going build any event handlers
            # just yet. Let's just resume the process for now
            raw_input('Press key \'Enter\' to continue...')
            self.debugger_active = False
            kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                        debug_event.dwThreadId,
                                        continue_status)
            
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print '[*] Finished debugging. Exiting...'
            return True
        else:
            print 'There was an error: ', kernel32.GetLastError()
            return False
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        