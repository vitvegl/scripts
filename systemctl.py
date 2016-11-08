import os
import subprocess

def __daemon__reload__(mode = 'user'):
    ''' systemctl [mode] daemon-reload '''
    if mode == 'user':
        subprocess.call('systemctl --user daemon-reload', shell = True)
    elif mode == 'system':
        if os.getuid() == 0:
            subprocess.call('systemctl daemon-reload', shell = True)
        else:
            raise RuntimeError('must be root')
    else:
        raise RuntimeError('unknown mode')

def __systemctl__(action, service, mode = 'user'):
    ''' This function is simple wrapper to systemctl '''
    for __argument__ in __systemctl__.__code__.co_varnames:
        if type(__argument__) == str:
            if mode == 'user':
                if action == 'start':
                    subprocess.call('systemctl --user start {}'.format(service), shell = True)
                elif action == 'stop':
                    subprocess.call('systemctl --user stop {}'.format(service), shell = True)
                elif action == 'restart':
                    subprocess.call('systemctl --user restart {}'.format(service), shell = True)
                else:
                    raise RuntimeError('unknown action')
            elif mode == 'system':
                if os.getuid() == 0:
                    if action == 'start':
                        subprocess.call('systemctl start {}'.format(service), shell = True)
                    elif action == 'stop':
                        subprocess.call('systemctl stop {}'.format(service), shell = True)
                    elif action == 'restart':
                        subprocess.call('systemctl restart {}'.format(service), shell = True)
                    else:
                        raise RuntimeError('unknown action')
                else:
                    raise RuntimeError('must be root')
            else:
              raise RuntimeError('unknown mode')
        else:
            raise RuntimeError('this function requires 3 string arguments')
