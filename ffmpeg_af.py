#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/**************************************************************************
#* ffmpeg_af.py: audio filter cases on windows: python 3.x, ffmpeg-4.3.1
#***************************************************************************
#* Copyright (c) 2020-2020 Hybase@qq.com
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
#*
#****************************************************************************/
import os
import re
import sys
import hysmm_def
import ffmpeg_run

################################################################################
# 通用参数字符串

dst_dir        = hysmm_def.dst_dir
log_param      = hysmm_def.log_param
tt_src_dir     = 'e:/material/ffmpeg_hys_python'
input_mp4_file = ' -i ' + tt_src_dir + '/tt.mp4 '
input_mp3_file = ' -i ' + tt_src_dir + '/es_mp3.mp3 '
af_out         = dst_dir + '/af_effect'

################################################################################
# case flags: (default: the first be set, please set others by yourself)
play_flag    = False   # true - ffplay, false - ffmpeg
sfx          = '.ts'
start_num    = 1
end_num      = 15

class af_case_c:
    def __init__(self):
        # aformat 转换格式
        self.case001 = [af_out + '/d001_aformat' + sfx,   " aformat=f=s16:r=48000:cl=stereo  "]
        # volume 调整音量
        self.case002 = [af_out + '/d002_volume' + sfx,    " volume=0.25 "]
        # amix 混音 （需要两路以上输入）: 不支持 ffplay
        self.case003 = [af_out + '/d003_amix' + sfx,      " amix=inputs=2:duration=first:dropout_transition=3 "]
        # adelay 延迟
        self.case004 = [af_out + '/d004_adelay' + sfx,    " adelay=delays=1500:all=1 "]
        # aecho 回声
        self.case005 = [af_out + '/d005_aecho' + sfx,     " aecho=0.8:0.88:60:0.4 "]
        # afade 淡入淡出
        self.case006 = [af_out + '/d006_afadein' + sfx,   " afade=t=in:ss=0:d=5 "]
        # aloop 循环
        self.case007 = [af_out + '/d007_aloop' + sfx,     " aloop=loop=-1 "]
        # asubboost 低音炮效果
        self.case008 = [af_out + '/d008_asubboost' + sfx, " asubboost=dry=0.5:wet=0.8:decay=0.7:feedback=0.5:cutoff=100:slope=0.5:delay=20"]
        # atempo 节拍速度
        self.case009 = [af_out + '/d009_atempo' + sfx,    " atempo=0.5"]
        # chorus 和声
        # | ^ " &等字符是特殊字符。
        # windows cmd.exe特殊字符需转义。
        # 转义时，^^代表^，^|代表|，^"代表"等等
        #af_str = ''' chorus=0.7:0.9:55:0.4:0.25:2'''
        #af_str = ''' chorus='0.6:0.9:50^|60:0.4^|0.32:0.25^|0.4:2^|1.3' '''
        self.case010 = [af_out + '/d010_chorus' + sfx,    " chorus='0.7:0.9:55:0.4:0.25:2' "]
        self.case011 = [af_out + '/d011_chorus' + sfx,    " chorus='0.6:0.9:50^|60:0.4^|0.32:0.25^|0.4:2^|1.3' "]
        self.case012 = [af_out + '/d012_chorus' + sfx,    " chorus='0.5:0.9:50^|60^|40:0.4^|0.32^|0.3:0.25^|0.4^|0.3:2^|2.3^|1.3' "]
        # aresample 重采样
        self.case013 = [af_out + '/d013_aresample' + sfx, " aresample=44100 "]
        # tremolo 颤音
        self.case014 = [af_out + '/d014_tremolo' + sfx,   " tremolo "]

#################################################################################
# main process
if __name__ == "__main__":
    # init logger
    log = hysmm_def.Logger('sys_all.log',level='debug')
    hysmm_def.Logger('sys_err.log', level='error')
    log.logger.info("========= program start ============")

    # check source and output dir, create output dir if necessary
    hysmm_def.checkDir(log, tt_src_dir)
    hysmm_def.createDirIfNotFound(log, dst_dir)
    hysmm_def.createDirIfNotFound(log, af_out)

    # init af case
    af_case      = af_case_c()
    af_case_dict = af_case.__dict__

    # ***********************************
    # transcode parameters
    trc_str = ' -vcodec copy -acodec aac -ab 128k ' + hysmm_def.tsmux_vbr_str
    log.logger.info(trc_str)

    for i in range(start_num, end_num):
        idx = '%03d' %i
        key = "case" + idx
        if (i == 3): # only for amix
            input_file = input_mp4_file + input_mp3_file
        else:
            input_file = input_mp4_file
        output_file = af_case_dict[key][0]

        if (play_flag):
            af_str = ' -af ' + af_case_dict[key][1]
            log.logger.info("key:%s, af: %s, dst: %s", key, af_str, output_file)
            cmd = 'ffplay ' + log_param + input_file + af_str
            ffmpeg_run.ffplay_run(key, True, log, cmd)
        else:
            af_str = ' -filter_complex ' + af_case_dict[key][1]
            log.logger.info("key:%s, af: %s, dst: %s", key, af_str, output_file)
            cmd = 'ffmpeg -y ' + log_param + input_file + af_str  + trc_str + output_file
            ffmpeg_run.ffmpeg_run(key, True, log, cmd)

    ## end of all cases
    log.logger.info("=== all cases run ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

################################################################################
# end
#