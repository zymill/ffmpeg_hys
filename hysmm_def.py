#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/****************************************************************************
#* hysmm_def.py: hysmm common defines on python 3.x
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
import logging
from logging import handlers

#*****************************************************************************
# version / author / blog address
version    = "ver 0.0.1 last updated on 2020-12-31 19:30:25"
author     = "Author: hybase@qq.com  QQ:23207689 WebChat: hybase"
url_csdn   = "https://blog.csdn.net/zymill"
url_github = "https://github.com/zymill"

#*****************************************************************************
# 通用字符串常量
# 统一的输入参数，本文以常见的mkv（H264+AAC）格式为测试素材
# (其中部分需要用到的mpegts文件，采用它派生的tt.ts)
# 测试前的准备工作
# 1）PC 上有 D、E 分区
# 2）E分区上准备下面 mkv/mp4/ts 源文件: 推荐格式为 H264+AAC
# 3）准备测试素材
#
log_param       = ' -loglevel info '
src_dir         = 'E:/material/_utfiles_unittest_hysmm'
dst_dir         = 'd:/otest'

input_mp4_file  = " -y -i " + src_dir + "/mp4_h264_1080p_2020_琅琊榜.mp4 "
input_flv_file  = " -i " + src_dir + "/france.flv "
tsmux_vbr_str   = ' -pat_period 0.1 -sdt_period 1.2 -pcr_period 40 -muxrate 0 -f mpegts '
#****************************** logger ***************************************
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - [%(levelname)s] %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

#*****************************************************************************
# Methods check dir/file
def traverseDir(root_path, file_list, dir_list):
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        dir_file_path = os.path.join(root_path, dir_file)
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            traverseDir(dir_file_path, file_list, dir_list)
        else:
            file_list.append(dir_file_path)

#*****************************************************************************
# check dst_path, create it if not found
def createDirIfNotFound(log, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
        log.logger.info('created ' + dst_path)
        return
    log.logger.info('found ' + dst_path)
    return

#*****************************************************************************
# check dst_path, create it if not found
def checkDir(log, curr_path):
    file_list = []   # 文件路径列表
    dir_list = []    # 目录路径列表
    traverseDir(curr_path, file_list, dir_list)

    log.logger.info('>>>')
    log.logger.info('found %d dir', len(dir_list))
    for dir in dir_list:
        log.logger.info(dir)

    log.logger.info('>>>')
    log.logger.info('found %d files', len(file_list))
    for file in file_list:
        log.logger.info(file)
    return

#*****************************************************************************
# end
#