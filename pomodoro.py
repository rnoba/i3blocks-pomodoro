#!/usr/bin/env python3

import time
import sys 
import os

progress_bar_segments = 10
extract_minutes = lambda x: (int(x / 60), int(x % 60))
min_to_sec = lambda x: x * 60
progress_bar = lambda x: (('■'))*int(x*progress_bar_segments)+(('▢'))*(progress_bar_segments-int(x*progress_bar_segments))

pomodoro_time = min_to_sec(30)
pause_time = min_to_sec(10)
cycles = 100 

args = len(sys.argv)
task = ""
if args == 2:
    task = sys.argv[1]
elif args == 3:
    cycles = int(sys.argv[2])
    
start_time = time.time()
in_freeze = False 
current = -1 
current_cycle = 0
elapsed = 0 
in_pause = False
current_time = pomodoro_time 

while True: 
    if current_cycle < cycles:
        elapsed = int(time.time()-start_time) if not in_freeze else elapsed 
        if current == elapsed: continue
        current = elapsed
        p = (elapsed/100/current_time*100)
        min, secs = extract_minutes(current_time-elapsed)
        print('{t} {m:02}:{s:02} | {cc} of {c} {i:10s} {p}'
              .format(
                      t=task,
                      m=min, 
                      s=secs, 
                      cc=current_cycle+1,
                      c=cycles,
                      p=(('{t:.1f}%'.format(t=p*100).rjust(6))) if not in_freeze else 'BREAK', 
                      i=progress_bar(p) if not in_pause else progress_bar(p)[::-1]),
              flush = True)
        if elapsed >= current_time:
            start_time = time.time() 
            if in_pause: 
                current_time = pomodoro_time
                current_cycle += 1
            else: current_time = pause_time
            in_pause = not in_pause
    else: 
       print("DONE!", flush=True) 
    time.sleep(1)
