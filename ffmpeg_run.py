#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/****************************************************************************
#* ffmpeg_run.py: ffmpeg/ffplay api based on python 3.x, ffmpeg-4.3.1
#*****************************************************************************
#* Copyright (c) 2020-2021 Hybase@qq.com
#*
#* This program is free software: you can redistribute it and/or modify
#* it under the terms of the GNU General Public License as published by
#* the Free Software Foundation, either version 3 of the License, or
#* (at your option) any later version.
#*
#* This program is distributed in the hope that it will be useful,
#* but WITHOUT ANY WARRANTY; without even the implied warranty of
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#* GNU General Public License for more details.
#****************************************************************************/
import os
import re
import sys
import hysmm_def

#*****************************************************************************
# ffmpeg run by os.system()
def ffmpeg_run(case_name, run_flag, log, cmd):
    if (run_flag):
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

#*****************************************************************************
# ffplay run by os.system()
# format: ffplay -i e:/material/tt.mkv -vf "vf_str"
def ffplay_run(case_name, run_flag, log, cmd):
    if (run_flag):
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

#*****************************************************************************
# ffmpeg run by os.system()
# format: ffmpeg -y -i e:/material/tt.mkv -filter_complex "vf_str" -vcodec libx264 -acodec aac -f mp4 "output_filename"
def ffmpeg_vf_run(case_name, run_flag, log, input_file, vf_str, output_filename):
    if (run_flag):
        cmd = 'ffmpeg ' + hysmm_def.log_param + input_file + ' -filter_complex ' + vf_str + ' -max_muxing_queue_size 256 -vcodec libx264 -acodec aac -f mp4 ' + output_filename
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

#*****************************************************************************
# ffmpeg run by os.system()
# format: ffmpeg -y -i e:/material/tt.mkv -filter_complex "af_str" -vcodec copy -acodec aac -f mp4 "output_filename"
def ffmpeg_af_run(case_name, run_flag, log, input_file, af_str, output_filename):
    if (run_flag):
        cmd = 'ffmpeg ' + hysmm_def.log_param + input_file + ' -filter_complex ' + af_str + ' -max_muxing_queue_size 256 -vcodec copy -acodec aac -f mp4 ' + output_filename
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

#*****************************************************************************
# end
#