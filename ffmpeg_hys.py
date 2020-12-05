#/**************************************************************************
#* ffmpeg_hys.py: ffmpeg cases options on windows
#                 Python 3.x, ffmpeg-4.3.1 
#***************************************************************************
#* Copyright (c) 2020-2020 Hybase@qq.com
#*
#* Author: hybase@qq.com  QQ:23207689  WebChat: hybase
#*         http://blog.csdn.net/zymill
#*         http://github.com/zymill
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
#*****************************************************************************
#* Last update Date: 2020-12-03 21:30:25           version: 0.0.1
#*****************************************************************************
#*/

import os
import re
import sys
import logging
from logging import handlers

################################ logger ######################################
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

################################################################################
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

############################################################
# ffmpeg run by os.system()
def ffmpeg_run(log, cmd, run_flag, case_name):
    if (run_flag):
        log.logger.info('=== start === : ' + case_name)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

################################################################################
# 通用参数字符串
# 统一的输入参数，本文以常见的mkv（H264+AAC）格式为测试素材
# (其中部分需要用到的mpegts文件，采用它派生的tt.ts)
# 测试前的准备工作
# 1）PC 上有 D、E 分区
# 2）E分区上准备下面 mkv/mp4/ts 源文件: 推荐格式为 H264+AAC
# 3）准备拼接需要的hls分片至少 5片，名称及目录：
#    E:\material\ffmpeg_hys_python\hls_part\h264_part0.ts
#    E:\material\ffmpeg_hys_python\hls_part\h264_part1.ts
#    E:\material\ffmpeg_hys_python\hls_part\h264_part2.ts
#    E:\material\ffmpeg_hys_python\hls_part\h264_part3.ts
#    E:\material\ffmpeg_hys_python\hls_part\h264_part4.ts
#    e:/material/ffmpeg_hys_python/hls_part/hls_concat.txt
#   hls_concat.txt文件每行内容格式描述一个分片绝对路径，如下所示共5片：
#   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part0.ts'
#   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part1.ts'
#   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part2.ts'
#   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part3.ts'
#   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part4.ts'
# 4）准备图片转视频所需的序列化png图片(1000左右)，背景MP3音频
# 5) d分区，创建输出目录 d:/otest/   d:/otest/png  d:/otest/jpg

tt_src_dir     = 'e:/material/ffmpeg_hys_python'
log_param      = ' -loglevel info '
input_mkv_file = ' -y -i ' + tt_src_dir + '/tt.mkv '
input_mp4_file = ' -y -i ' + tt_src_dir + '/tt.mp4 '
input_ts_file  = ' -y -i ' + tt_src_dir + '/tt.ts '
input_mp3_file = ' -i    ' + tt_src_dir + '/es_mp3.mp3 '
input_png_file = ' -f image2 -i ' + tt_src_dir + '/image/image-%03.png '
hls_cancat_file= tt_src_dir + '/hls_part/hls_concat.txt '

################################################################################
# case flags: (default: the first be set, please set others by yourself)
flag_mkv2mp4          = True
flag_mkv2mpegts       = False
flag_mkv2flv          = False
flag_mpegts2mp4       = False

flag_trc_libx264_aac_mkv2mp4 = False
flag_trc_libx265_aac_mkv2mp4 = False
flag_trc_h264_nvenc_mkv2mp4  = False
flag_trc_hevc_nvenc_mkv2mp4  = False
flag_trc_libx264_mpegts_cbr  = False

flag_cut_by_time      = False
flag_extract_video_es = False
flag_extract_audio_es = False

flag_extract_png_from_video = False
flag_extract_jpg_from_video = False

flag_image2_png2video_no_audio   = False
flag_image2_png2video_with_audio = False

flag_segment_hls_spts = False
flag_segment_mp4      = False
flag_concat_mpegts    = False
flag_live_flv_stream  = False

#################################################################################
# check dst_path, create it if not found
def createDirIfNotFound(log, dst_path):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
        log.logger.info('created ' + dst_path)
        return
    log.logger.info('found ' + dst_path)
    return

#################################################################################
# main process 
if __name__ == "__main__":
    log = Logger('sys_all.log',level='debug')
    Logger('sys_err.log', level='error')
    log.logger.info("========= program start ============")

    #检查源路径相关内容
    root_path = tt_src_dir
    #文件路径列表
    file_list = []
    #目录路径列表
    dir_list = []

    traverseDir(root_path, file_list, dir_list)

    log.logger.info('>>>')
    log.logger.info('found %d dir', len(dir_list))
    for dir in dir_list:
        log.logger.info(dir)

    log.logger.info('>>>')
    log.logger.info('found %d files', len(file_list))
    for file in file_list:
        log.logger.info(file)

    # create output dir if necessary
    createDirIfNotFound(log, 'd:/otest/')
    createDirIfNotFound(log, 'd:/otest/png')
    createDirIfNotFound(log, 'd:/otest/jpg')

    #####################################################
    # 常用几类ffmpeg命令及样例（供参考）
    #
    # (查询指南：官方 www.ffmpeg.org，或 通过命令 ffmpeg -h full 可以查询全部参数选项详情)
    #
    # 1 封装转换：
    # 常见mkv->mp4/mpegts/flv, mpegts->mp4, mp4->flv
    # ffmpeg -y -i e:/material/tt.mkv -vcodec copy -acodec copy -f mp4 d:/tt.mp4
    # ffmpeg -y -i e:/material/tt.mkv -bsf:v h264_mp4toannexb -vcodec copy -acodec copy -f mpegts d:/tt.ts
    # ffmpeg -y -i e:/material/tt.mkv -vcodec copy -acodec copy -f flv d:/tt.flv
    # ffmpeg -y -i d:/tt.ts -vcodec copy -acodec copy -f mp4 d:/ts2mp4.mp4    
    #
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f mp4 d:/case001_tt.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -acodec copy -f mpegts d:/case002_tt.ts '
    cmd3 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f flv d:/case003_tt.flv '
    cmd4 = 'ffmpeg ' + log_param + input_ts_file  + ' -vcodec copy -acodec copy -f mp4 d:/case004_ts2mp4.mp4 '
    ffmpeg_run(log, cmd1, flag_mkv2mp4,    'case_mkv2mp4')
    ffmpeg_run(log, cmd2, flag_mkv2mpegts, 'case_mkv2mpegts')
    ffmpeg_run(log, cmd3, flag_mkv2flv,    'case_mkv2flv')
    ffmpeg_run(log, cmd4, flag_mpegts2mp4, 'case_mpegts2mp4')

    #
    # 2 转码
    #   1）转成 H264+AAC (指定视频分辨率, B帧，关键帧间隔，不指定视频码率默认是 VBR 模式)
    #   ffmpeg -y -i e:/material/tt.mkv -vcodec libx264 -s 640x360 -bf 2 -g 25 -acodec aac -f mp4 d:/tt_h264_aac.mp4
    #
    #   2）转成 HEVC+AAC（增加指定音频采样率，码率，声道，可选）
    #   ffmpeg -y -i e:/material/tt.mkv -vcodec libx265 -preset medium -s 640x360 -bf 2 -g 25 -acodec aac -ar 48000 -ab 128k -ac 2 -f mp4 d:/tt_hevc_aac.mp4
    #
    #   3）带NVIDIA显卡（支持H264/HEVC硬件加速）
    #   ffmpeg -y -c:v h264_cuvid -gpu 0 -i e:/material/tt.mkv -c:v:0 h264_nvenc -gpu any -s 640x360 -g 25 -acodec copy -f mp4 d:/nv_h264_aac.mp4
    #   ffmpeg -y -c:v h264_cuvid -gpu 0 -i e:/material/tt.mkv -c:v:0 hevc_nvenc -gpu any -s 640x360 -g 25 -acodec copy -f mp4 d:/nv_hevc_aac.mp4
    #
    #   4) 输出 MPEGTS CBR（指定视频码率 1Mbps，音频64Kbps，整体码率输出1.25Mbps，恒定码率模式，通常需转码带上恒定码率控制参数）
    #   ffmpeg -y -i e:/material/tt.mkv -c:v:0 libx264 -s 640x360 -bf 2 -g 25 -b:v:0 1000k -minrate 1000k -maxrate 1000k -bufsize 1000k -c:a:0 aac -b:a:0 64k\
    #   -muxrate 1250k -muxdelay 0.85 -pcr_period 33 -pat_period 0.1 -sdt_period 1.2 -f mpegts d:/tt_h264_aac_cbr.ts
    #
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx264 -s 640x360 -bf 2 -g 25 -acodec aac  -max_muxing_queue_size 256 -f mp4 d:/case005_h264_aac.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx265 -preset medium -s 640x360 -bf 2 -g 25 -acodec aac -max_muxing_queue_size 256 -f mp4 d:/case006_hevc_aac.mp4 '
    cmd3 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 h264_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/case007_nv_h264_aac.mp4 '
    cmd4 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 hevc_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/case008_nv_hevc_aac.mp4 '
    cmd5 = 'ffmpeg ' + log_param + input_mkv_file + ' -c:v:0 libx264 -s 640x360 -bf 2 -g 25 -b:v:0 1000k -minrate 1000k -maxrate 1000k -bufsize 1000k -c:a:0 aac -b:a:0 64k -max_muxing_queue_size 256 -muxrate 1250k -muxdelay 0.85 -pcr_period 33 -pat_period 0.1 -sdt_period 1.2 -f mpegts d:/case009_h264_aac_cbr.ts '
    ffmpeg_run(log, cmd1, flag_trc_libx264_aac_mkv2mp4, 'case_trc_libx264_aac_mkv2mp4')
    ffmpeg_run(log, cmd2, flag_trc_libx265_aac_mkv2mp4, 'case_trc_libx265_aac_mkv2mp4')
    ffmpeg_run(log, cmd3, flag_trc_h264_nvenc_mkv2mp4 , 'case_trc_h264_nvenc_mkv2mp4')
    ffmpeg_run(log, cmd4, flag_trc_hevc_nvenc_mkv2mp4 , 'case_trc_hevc_nvenc_mkv2mp4')
    ffmpeg_run(log, cmd5, flag_trc_libx264_mpegts_cbr , 'case_trc_libx264_mpegts_cbr')

    # 3 按时间截取视频 (ss: 起始时间 精度秒, t: 持续时间 精度秒，二种格式等同)
    #   ffmpeg -y -ss 00:01:30 -t 00:01:00 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #   ffmpeg -y -ss 90 -t 60 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #
    cmd = 'ffmpeg ' + log_param + ' -ss 00:01:30 -t 00:01:00 '+ input_mkv_file + ' -vcodec copy -acodec copy d:/case010_part.mkv '
    ffmpeg_run(log, cmd, flag_cut_by_time, 'case_cut_by_time')

    # 4 分离视频，音频：提取成 ES 文件
    #   ffmpeg -y -i e:/material/tt.mkv -bsf:v h264_mp4toannexb -vcodec copy -an es_h264.h264
    #   ffmpeg -y -i e:/material/tt.mkv -acodec copy -vn es_aac.aac
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -an d:/case011_es_h264.h264 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -acodec copy -vn d:/case012_es_aac.aac '
    ffmpeg_run(log, cmd1, flag_extract_video_es, 'case_extract_video_es')
    ffmpeg_run(log, cmd2, flag_extract_audio_es, 'case_extract_audio_es')

    #
    # 5 从视频周期提取PNG/JPG图片(指定频率，图片分辨率)
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.png
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.jpg
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -r 1 -s 640x360 -f image2 d:/otest/png/image-%04d.png '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -r 1 -s 640x360 -f image2 d:/otest/jpg/image-%04d.jpg '
    ffmpeg_run(log, cmd1, flag_extract_png_from_video, 'case_extract_png_from_video')
    ffmpeg_run(log, cmd2, flag_extract_jpg_from_video, 'case_extract_jpg_from_video')

    #
    # 6 序列化图片转视频
    #   纯视频
    #   ffmpeg -y -f image2 -i e:/material/image_png/image%3d.png -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/image2video_no_audio.mp4
    #   配音频
    #   ffmpeg -y -i e:/material/background.mp3 -i e:/material/image_png/image%3d.png -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/image2video_audio.mp4
    cmd1 = 'ffmpeg -y ' +                  input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/case012_image2video_no_audio.mp4'
    cmd2 = 'ffmpeg -y ' + input_mp3_file + input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/case013_image2video_with_audio.mp4'
    ffmpeg_run(log, cmd1, flag_image2_png2video_no_audio,   'case_image2_png2video_no_audio')
    ffmpeg_run(log, cmd2, flag_image2_png2video_with_audio, 'case_image2_png2video_with_audio')

    # 7 视频切片(源为single program ts 或 mp4, 分片单位时间 60 秒)
    #
    #   ffmpeg -y -fflags +genpts -i d:/tt_h264_aac.ts -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 h264_part.m3u8
    #   ffmpeg -y -i test.mp4 -c copy -map 0 -f segment -segment_time 60 d:/part-%03d.mp4
    cmd1 = 'ffmpeg -fflags +genpts ' + input_ts_file + ' -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 d:/case014_h264_part.m3u8'
    cmd2 = 'ffmpeg -fflags +genpts ' + input_mp4_file + ' -c copy -map 0 -f segment -segment_time 60 d:/case015_part-%03d.mp4'
    ffmpeg_run(log, cmd1, flag_segment_hls_spts, 'case_segment_hls_spts')
    ffmpeg_run(log, cmd2, flag_segment_mp4,      'case_segment_mp4')

    #
    # 8 文件合并(mpegts: VBR)
    #   Windows下通常采用文件方式
    #   ffmpeg -f concat -safe 0 -i "m.txt" -c copy new.mp4
    #   文件每行内容格式描述一个分片绝对路径，如下所示共5片：
    #   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part0.ts'
    #   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part1.ts'
    #   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part2.ts'
    #   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part3.ts'
    #   file 'file:E:/material/ffmpeg_hys_python/hls_part/h264_part4.ts'
    #
    #   Linux下 则可以采用相对路径直接拼接
    #   ffmpeg -i "concat:/data/part0_convert.ts|
    #                     /data/part1_convert.ts|
    #                     /data/part2_convert.ts|
    #                     /data/part3_convert.ts|
    #                     /data/part4_convert.ts|
    #                     /data/part5_convert.ts|
    #                     /data/part6_convert.ts|
    #                     /data/part7_convert.ts"
    #      -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -pat_period 0.1 -sdt_period 1.2 -pcr_period 40 -muxrate 0 -f mpegts d:/otest/whole.ts
    #
    map_str = ' -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy '
    mux_str = ' -pat_period 0.1 -sdt_period 1.2 -pcr_period 40 -muxrate 0 '
    cmd = 'ffmpeg -y -f concat -safe 0 -i ' + hls_cancat_file + map_str + mux_str + ' -f mpegts d:/case016_concat_h264.ts '
    ffmpeg_run(log, cmd, flag_concat_mpegts, 'case_concat_mpegts')

    # 9 输出实时流(结合rtmp-flv流媒体服务, flv通常需为H264+AAC格式)
    #   ffmpeg -re -stream_loop -1 -i e:/material/tt.mkv -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1"
    #
    cmd = 'ffmpeg -re -stream_loop -1 ' + log_param + input_ts_file + ' -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1" '
    ffmpeg_run(log, cmd, flag_live_flv_stream, 'case_live_flv_stream')

    log.logger.info("=== all cases run ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

################################################################################
# end
#
