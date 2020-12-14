#/**************************************************************************
#* ffmpeg_hys.py: ffmpeg cases options on windows
#                 python 3.x, ffmpeg-4.3.1 
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
#* Last update Date: 2020-12-14 19:30:25           version: 0.0.4
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

############################################################
# ffmpeg run by os.system()
# format: ffmpeg -y -i e:/material/tt.mkv -filter_complex "vf_str" -vcodec libx264 -acodec aac -f mp4 "output_filename"
def ffmpeg_vf_run(log, vf_str, output_filename, run_flag, case_name):
    if (run_flag):
        cmd = 'ffmpeg ' + log_param + input_mkv_file + ' -filter_complex ' + vf_str + ' -max_muxing_queue_size 256 -vcodec libx264 -acodec aac -f mp4 ' + output_filename
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
        os.system(cmd)
        log.logger.info('=== end === : ' + case_name)
        return
    log.logger.info('=== by pass === case not setting : ' + case_name)
    return

############################################################
# ffmpeg run by os.system()
# format: ffmpeg -y -i e:/material/tt.mkv -filter_complex "af_str" -vcodec copy -acodec aac -f mp4 "output_filename"
def ffmpeg_af_run(log, af_str, output_filename, run_flag, case_name):
    if (run_flag):
        cmd = 'ffmpeg ' + log_param + input_mkv_file + ' -filter_complex ' + af_str + ' -max_muxing_queue_size 256 -vcodec copy -acodec aac -f mp4 ' + output_filename
        log.logger.info('=== start === : ' + case_name)
        log.logger.info('exec: ' + cmd)
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

flag_segment_hls_spts   = False
flag_segment_mp4        = False
flag_concat_mpegts      = False
flag_live_flv_stream    = False

## video filter flags ##
flag_vf_overlay_logos    = False
flag_vf_drawtext         = False
flag_vf_overlay_drawtext_delogo = False
flag_vf_crop             = False
flag_vf_pad              = False
flag_vf_rotate_dynamic   = False
flag_vf_rotate_45        = False
flag_vf_transpose_cw90   = False
flag_vf_transpose_ccw90  = False
flag_vf_transpose_cw180  = False
flag_vf_hflip            = False
flag_vf_vflip            = False
flag_vf_drawtext_marquee = False

## other video filter cases ##
flag_vf_drawgrid         = False
flag_vf_drawbox          = False
flag_vf_boxblur          = False 
flag_vf_edgedetect       = False    
flag_vf_eq               = False
flag_vf_histeq           = False 
flag_vf_fadein           = False 
flag_vf_fadeout          = False
flag_vf_geq              = False 
flag_vf_histogram        = False
flag_vf_hqdn3d           = False 
flag_vf_hue              = False    
flag_vf_il               = False
flag_vf_lutyuv           = False 
flag_vf_negate           = False    
flag_vf_oscilloscope     = False
flag_vf_showpalette      = False 
flag_vf_shuffleplanes    = False    
flag_vf_sobel            = False    
flag_vf_stereo3d         = False
flag_vf_swapuv           = False 
flag_vf_tile             = False   
flag_vf_unsharp          = False 
flag_vf_vignette         = False  

## audio filter cases ##
flag_af_aformat          = False
flag_af_volume           = False
flag_af_amix             = False
flag_af_adelay           = False
flag_af_aecho            = False
flag_af_afade            = False
flag_af_aloop            = False
flag_af_asubboost        = False
flag_af_atempo           = False
flag_af_chorus           = False
flag_af_aresample        = False
flag_af_tremolo          = False

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
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f mp4 d:/otest/case001_mkv2mp4.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -acodec copy -f mpegts d:/otest/case002_mkv2ts.ts '
    cmd3 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f flv d:/otest/case003_mkv2flv.flv '
    cmd4 = 'ffmpeg ' + log_param + input_ts_file  + ' -vcodec copy -acodec copy -f mp4 d:/otest/case004_ts2mp4.mp4 '
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
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx264 -s 640x360 -bf 2 -g 25 -acodec aac  -max_muxing_queue_size 256 -f mp4 d:/otest/case005_trc_h264_aac.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx265 -preset medium -s 640x360 -bf 2 -g 25 -acodec aac -max_muxing_queue_size 256 -f mp4 d:/otest/case006_trc_hevc_aac.mp4 '
    cmd3 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 h264_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/otest/case007_trc_nv_h264_aac.mp4 '
    cmd4 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 hevc_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/otest/case008_trc_nv_hevc_aac.mp4 '
    cmd5 = 'ffmpeg ' + log_param + input_mkv_file + ' -c:v:0 libx264 -s 640x360 -bf 2 -g 25 -b:v:0 1000k -minrate 1000k -maxrate 1000k -bufsize 1000k -c:a:0 aac -b:a:0 64k -max_muxing_queue_size 256 -muxrate 1250k -muxdelay 0.85 -pcr_period 33 -pat_period 0.1 -sdt_period 1.2 -f mpegts d:/otest/case009_trc_h264_aac_cbr.ts '
    ffmpeg_run(log, cmd1, flag_trc_libx264_aac_mkv2mp4, 'case_trc_libx264_aac_mkv2mp4')
    ffmpeg_run(log, cmd2, flag_trc_libx265_aac_mkv2mp4, 'case_trc_libx265_aac_mkv2mp4')
    ffmpeg_run(log, cmd3, flag_trc_h264_nvenc_mkv2mp4 , 'case_trc_h264_nvenc_mkv2mp4')
    ffmpeg_run(log, cmd4, flag_trc_hevc_nvenc_mkv2mp4 , 'case_trc_hevc_nvenc_mkv2mp4')
    ffmpeg_run(log, cmd5, flag_trc_libx264_mpegts_cbr , 'case_trc_libx264_mpegts_cbr')

    # 3 按时间截取视频 (ss: 起始时间 精度秒, t: 持续时间 精度秒，二种格式等同)
    #   ffmpeg -y -ss 00:01:30 -t 00:01:00 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #   ffmpeg -y -ss 90 -t 60 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #
    cmd = 'ffmpeg ' + log_param + ' -ss 00:01:30 -t 00:01:00 '+ input_mkv_file + ' -vcodec copy -acodec copy d:/otest/case010_cut_part.mkv '
    ffmpeg_run(log, cmd, flag_cut_by_time, 'case_cut_by_time')

    # 4 分离视频，音频：提取成 ES 文件
    #   ffmpeg -y -i e:/material/tt.mkv -bsf:v h264_mp4toannexb -vcodec copy -an es_h264.h264
    #   ffmpeg -y -i e:/material/tt.mkv -acodec copy -vn es_aac.aac
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -an d:/otest/case011_es_h264.h264 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -acodec copy -vn d:/otest/case012_es_aac.aac '
    ffmpeg_run(log, cmd1, flag_extract_video_es, 'case_extract_video_es')
    ffmpeg_run(log, cmd2, flag_extract_audio_es, 'case_extract_audio_es')

    #
    # 5 从视频周期提取PNG/JPG图片(指定频率，图片分辨率)
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.png
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.jpg
    #   -r 1: 一秒一张图片
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
    cmd1 = 'ffmpeg -y ' +                  input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/otest/case012_image2video_no_audio.mp4'
    cmd2 = 'ffmpeg -y ' + input_mp3_file + input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/otest/case013_image2video_with_audio.mp4'
    ffmpeg_run(log, cmd1, flag_image2_png2video_no_audio,   'case_image2_png2video_no_audio')
    ffmpeg_run(log, cmd2, flag_image2_png2video_with_audio, 'case_image2_png2video_with_audio')

    # 7 视频切片(源为single program ts 或 mp4, 分片单位时间 60 秒)
    #
    #   ffmpeg -y -fflags +genpts -i d:/tt_h264_aac.ts -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 h264_part.m3u8
    #   ffmpeg -y -i test.mp4 -c copy -map 0 -f segment -segment_time 60 d:/part-%03d.mp4
    cmd1 = 'ffmpeg -fflags +genpts ' + input_ts_file + ' -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 d:/otest/case014_h264_part.m3u8'
    cmd2 = 'ffmpeg -fflags +genpts ' + input_mp4_file + ' -c copy -map 0 -f segment -segment_time 60 d:/otest/case015_part-%03d.mp4'
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
    #      -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -pat_period 0.1 -sdt_period 1.2 -pcr_period 40 -muxrate 0 -f mpegts /output/whole.ts
    #
    map_str = ' -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy '
    mux_str = ' -pat_period 0.1 -sdt_period 1.2 -pcr_period 40 -muxrate 0 '
    cmd = 'ffmpeg -y -f concat -safe 0 -i ' + hls_cancat_file + map_str + mux_str + ' -f mpegts d:/otest/case016_concat_h264.ts '
    ffmpeg_run(log, cmd, flag_concat_mpegts, 'case_concat_mpegts')

    # 9 输出实时流(结合rtmp-flv流媒体服务, flv通常需为H264+AAC格式)
    #   ffmpeg -re -stream_loop -1 -i e:/material/tt.mkv -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1"
    #
    cmd = 'ffmpeg -re -stream_loop -1 ' + log_param + input_ts_file + ' -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1" '
    ffmpeg_run(log, cmd, flag_live_flv_stream, 'case_live_flv_stream')

    # 10 overlay image logos(png/bmp/webp/gif/jpeg) , draw text and delogo
    #   ffmpeg "
    #   ffmpeg -fflags +genpts -i main_video.mkv -i logo1.png -i logo2.jpg -max_muxing_queue_size 256
    #          -filter_complex "[0:v][1:v]overlay=40:40[bkg1];[bkg1][2:v]overlay=200:40,"\
    #          "drawtext=fontfile=/fonts/mingliu.ttc:text='hybase@qq.com 视频水印1':x=50:y=450:fontsize=32:fontcolor=0xFFEE00@0.7:shadowy=-1,"\
    #          "drawtext=fontfile=/fonts/mingliu.ttc:text='hybase@qq.com 视频水印2':x=350:y=450:fontsize=32:fontcolor=0xFFEE00@0.7:shadowy=-1,"\
    #          "delogo=w=200:h=80:x=1000:y=50" \
    #          -map 0:0 -c:v:0 libx264 -s 1280x720 -b:v:0 1500000 -minrate 1500000 -maxrate 3000000 -bufsize 1500000 -g 25 -bf 1 -pix_fmt yuv420p -r:v:0 25.000000 \
    #          -map 0:1 -c:a:0 aac -ab:a:0 64k -ar:a:0 48000 -ac:a:0 2 -vol:a:0 256 \
    #          -map 0:1 -c:a:1 ac3 -ab:a:1 128k -ar:a:1 48000 -ac:a:1 2 -vol:a:1 256 \
    #          -muxrate 0 -f mpegts d:/output.ts
    
    png_logo  = ' -i e:/material/image/logo/jxtv_96x96.png '
    jpg_logo  = ' -i e:/material/image/logo/jxtv_96x96.jpg '
    drawtext1 = '''drawtext=fontfile=c:/Windows/Fonts/msyh.ttf:text='hybase@qq.com视频水印1':x=50:y=550:fontsize=36:fontcolor=0xFFFF00@0.7:shadowy=-1,'''
    drawtext2 = '''drawtext=fontfile=c:/Windows/Fonts/msyh.ttf:text='hybase@qq.com视频水印2':x=50:y=650:fontsize=36:fontcolor=0xFFFF00@0.7:shadowy=-1'''
    delogo_str= 'delogo=w=200:h=80:x=1000:y=50'
    video_param_str = ' -map 0:0 -c:v:0 libx264 -s 1280x720 -b:v:0 1500000 -minrate 1500000 -maxrate 3000000 -bufsize 1500000 -g 25 -bf 1 -pix_fmt yuv420p -r:v:0 25.000000 '
    aac_str = ' -map 0:1 -c:a:0 aac -ab:a:0 64k -ar:a:0 48000 -ac:a:0 2 -vol:a:0 256 '
    ac3_str = ' -map 0:1 -c:a:1 ac3 -ab:a:1 128k -ar:a:1 48000 -ac:a:1 2 -vol:a:1 256 '
    mux_str = ' -muxrate 0 -pat_period 0.1 -sdt_period 1.2 '
    
    cmd1 = 'ffmpeg -y -fflags +genpts ' + log_param + input_ts_file + png_logo + jpg_logo + ' -max_muxing_queue_size 256 -filter_complex ' + \
           '[0:v][1:v]overlay=60:40[bkg1];[bkg1][2:v]overlay=200:40,' + video_param_str + aac_str + ac3_str +\
            mux_str + ' -f mpegts d:/otest/case017_vf_overlay_logos.ts '
    cmd2 = 'ffmpeg -y -fflags +genpts ' + log_param + input_ts_file + ' -max_muxing_queue_size 256 -filter_complex ' + \
            drawtext1 + drawtext2 + video_param_str + aac_str + ac3_str + mux_str + ' -f mpegts d:/otest/case018_vf_drawtexts.ts '
    cmd3 = 'ffmpeg -y -fflags +genpts ' + log_param + input_ts_file + png_logo + jpg_logo + ' -max_muxing_queue_size 256 -filter_complex ' + \
           '[0:v][1:v]overlay=60:40[bkg1];[bkg1][2:v]overlay=200:40,' + drawtext1 + drawtext2 + video_param_str + aac_str + ac3_str +\
            mux_str + ' -f mpegts d:/otest/case018_vf_overlay_drawtext_delogo.ts '
    ffmpeg_run(log, cmd1, flag_vf_overlay_logos, 'case_vf_overlay_logos')
    ffmpeg_run(log, cmd2, flag_vf_drawtext, 'case_vf_drawtext')
    ffmpeg_run(log, cmd3, flag_vf_overlay_drawtext_delogo, 'case_vf_overlay_drawtext_delogo')

    # 11 视频裁剪
    #   crop=w=%d:h=%d:x=%d:y=%d
    #   注释：宽度:高度:x:y(x,y如果不写则从中心裁剪)
    #   注意事项：width, height, x, y 不要超出原始视频边界
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex crop=w=960:h=540:x=80:y=40 -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    #
    vf_str=' crop=w=960:h=540:x=80:y=40 '
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case019_vf_crop.mp4', flag_vf_crop, 'case_vf_crop')

    # 12 视频填充，视频尺寸增大
    #   "pad='iw*1.1:ih*1.1:(ow-iw)/2:(oh-ih)/2:color=violet'"
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex pad='iw*1.1:ih*1.1:(ow-iw)/2:(oh-ih)/2:color=violet' -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    #
    vf_str=" pad='iw*1.1:ih*1.1:(ow-iw)/2:(oh-ih)/2:color=violet' "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case020_vf_pad.mp4', flag_vf_pad, 'case_vf_pad')

    # 13 视频动态旋转 (rotate)
    #   rotate=PI*2/T*t (T为旋转360度的时间常量, 单位:秒)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex rotate=PI*2/T*t -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" rotate='PI*2/10*t' "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case021_vf_rotate.mp4', flag_vf_rotate_dynamic, 'case_vf_rotate_dynamic')

    # 14 视频旋转45度 (rotate)
    #   rotate=PI/4
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex rotate=PI/4 -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex rotate='PI/4:ow=floor(hypot(iw,ih)/4)*4:oh=ow:c=none' -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str1=" rotate='PI/4' "
    vf_str2=''' rotate='PI/4:ow=floor(hypot(iw,ih)/4)*4:oh=ow:c=none' '''
    ffmpeg_vf_run(log, vf_str1, 'd:/otest/case022_vf_rotate45_01.mp4', flag_vf_rotate_45, 'case_vf_rotate_45')
    ffmpeg_vf_run(log, vf_str2, 'd:/otest/case022_vf_rotate45_02.mp4', flag_vf_rotate_45, 'case_vf_rotate_45')

    # 15 视频顺时针旋转90 (transpose=1)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex transpose=1 -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" transpose=1 "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case023_vf_transpose_1_cw90.mp4', flag_vf_transpose_cw90, 'case_vf_transpose_cw90')

    # 16 视频顺时针旋转180度 (hflip,vflip)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex hflip,vflip -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" hflip,vflip "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case024_vf_rotate_cw180.mp4', flag_vf_transpose_cw180, 'case_vf_transpose_cw180')

    # 17 视频逆时针旋转90度 (transpose=3)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex transpose=3 -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" transpose=3 "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case025_vf_transpose_3_ccw90.mp4', flag_vf_transpose_ccw90, 'case_vf_transpose_ccw90')

    # 18 视频水平镜像 (hflip)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex hflip -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" hflip "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case026_vf_hflip.mp4', flag_vf_hflip, 'case_vf_hflip')

    # 19 视频竖直镜像 (vflip)
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex vflip -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str=" vflip "
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case027_vf_vflip.mp4', flag_vf_vflip, 'case_vf_vflip')


    # 20 视频文字跑马灯效果 (drawtext)
    #   水平从左往右： x+t*n   n越大滚动越快，单位：像素
    #   水平从右往做： x-t*n   n越大滚动越快，单位：像素
    #   竖直从上往下： y+t*n   n越大滚动越快，单位：像素
    #   竖直从下往上： y-t*n   n越大滚动越快，单位：像素
    #   ffmpeg -y -i e:/material/tt.mkv -filter_complex drawtext=”fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome':x=90+t*40:y=55:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1“ -vcodec libx264 -acodec aac -f mp4 d:/tt.mp4
    vf_str1= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-hr-left2right':x=90+t*40:y=60:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
    vf_str2= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-hr-right2left':x=1200-t*40:y=360:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
    vf_str3= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-ve-up2down':x=100:y=10+t*20:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
    vf_str4= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-ve-down2up':x=400:y=700-t*20:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
    vf_str= vf_str1 + ',' + vf_str2 + ',' + vf_str3 + ',' + vf_str4
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case028_vf_drawtext_marquee.mp4', flag_vf_drawtext_marquee, 'case_vf_drawtext_marquee')

    ############################
    # other video filter cases

    # 21 drawgrid 网格
    vf_str = "drawgrid=width=80:height=80:thickness=2:color=yellow@0.9" 
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case029_vf_drawgrid.mp4', flag_vf_drawgrid, 'case_vf_drawgrid')
    # 22 drawbox 框
    vf_str = "drawbox=x=10:y=10:w=860:h=480:color=pink@0.5:t=fill"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case030_vf_drawbox.mp4', flag_vf_drawbox, 'case_vf_drawbox')
    # 23 boxblur 平滑
    vf_str = "boxblur=2:1:cr=0:ar=0"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case031_vf_boxblur.mp4', flag_vf_boxblur, 'case_vf_boxblur')
    # 24 edgedetect 边缘检测
    vf_str = "edgedetect=low=0.1:high=0.4"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case032_vf_edgedetect.mp4', flag_vf_edgedetect, 'case_vf_edgedetect')
    # 25 eq
    vf_str = "eq=contrast=1.5:brightness=0.5"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case033_vf_eq.mp4', flag_vf_eq, 'case_vf_eq')
    # 26 histeq
    vf_str = "histeq=strength=0.5:intensity=0.4:antibanding=weak"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case034_vf_histeq.mp4', flag_vf_histeq, 'case_vf_histeq')
    # 27 fade in
    vf_str = "fade=in:0:250"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case035_vf_fadein.mp4', flag_vf_fadein, 'case_vf_fadein')
    # 28 fade out
    vf_str = "fade=out:0:250"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case036_vf_fadeout.mp4', flag_vf_fadeout, 'case_vf_fadeout')
    # 29 geq
    vf_str = "format=gray,geq=lum_expr='(p(X,Y)+(256-p(X-4,Y-4)))/2'"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case037_vf_geq.mp4', flag_vf_geq, 'case_vf_geq')
    # 30 histogram
    vf_str = "histogram"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case038_vf_histogram.mp4', flag_vf_histogram, 'case_vf_histogram')
    # 31 hqdn3d
    vf_str = "hqdn3d"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case039_vf_hqdn3d.mp4', flag_vf_hqdn3d, 'case_vf_hqdn3d')
    # 32 hue
    vf_str = "hue=h=90:s=1:b=5"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case040_vf_hue.mp4', flag_vf_hue, 'case_vf_hue')
    # 33 il
    vf_str = "il=l=d:c=d"   
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case041_vf_il.mp4', flag_vf_il, 'case_vf_il')    
    # 34 lutyuv
    vf_str = "lutyuv='y=maxval+minval-val:u=maxval+minval-val:v=maxval+minval-val'"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case042_vf_lutyuv.mp4', flag_vf_lutyuv, 'case_vf_lutyuv')
    # 35 negate
    vf_str = "negate"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case043_vf_negate.mp4', flag_vf_negate, 'case_vf_negate')
    # 36 oscilloscope
    vf_str = "oscilloscope=x=1:y=0.5:s=1:t=1"    
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case044_vf_oscilloscope.mp4', flag_vf_oscilloscope, 'case_vf_oscilloscope')
    # 37 showpalette
    vf_str = "showpalette"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case045_vf_showpalette.mp4', flag_vf_showpalette, 'case_vf_showpalette')
    # 38 shuffleplanes
    vf_str = "shuffleplanes=0:2:1:3"  
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case046_vf_shuffleplanes.mp4', flag_vf_shuffleplanes, 'case_vf_shuffleplanes')    
    # 39 sobel
    vf_str = "sobel"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case047_vf_sobel.mp4', flag_vf_sobel, 'case_vf_sobel')
    # 40 stereo3d
    vf_str = "stereo3d=abl:sbsr"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case048_vf_stereo3d.mp4', flag_vf_stereo3d, 'case_vf_stereo3d')
    # 41 swapuv
    vf_str = "swapuv"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case049_swapuv.mp4', flag_vf_swapuv, 'case_vf_swapuv')
    # 42 tile 填充参数需注意，确保不造成奇数宽或高
    vf_str = "scale=224:180,tile=4x3:nb_frames=12:padding=2:margin=2"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case050_vf_tile.mp4', flag_vf_tile, 'case_vf_tile')    
    # 43 unsharp
    vf_str = "unsharp"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case051_vf_unsharp.mp4', flag_vf_unsharp, 'case_vf_unsharp')
    # 44 vignette
    vf_str = "vignette='PI/4+random(1)*PI/50'"
    ffmpeg_vf_run(log, vf_str, 'd:/otest/case052_vf_vignette.mp4', flag_vf_vignette, 'case_vf_vignette')    

    ############################
    # audio filter cases

    # 45 aformat 转换格式
    af_str = " aformat=f=s16:r=48000:cl=stereo "
    ffmpeg_af_run(log, af_str, 'd:/otest/case053_af_aformat.mp4', flag_af_aformat, 'case_af_aformat') 
    # 46 volume 调整音量
    af_str = " volume=0.25"
    ffmpeg_af_run(log, af_str, 'd:/otest/case054_af_volume.mp4', flag_af_volume, 'case_af_volume')

    # 47 amix 混音 （需要两路以上输入）
    af_str = " -filter_complex amix=inputs=2:duration=first:dropout_transition=3"
    cmd = 'ffmpeg ' + log_param + input_mkv_file + input_mp3_file + af_str + ' -vcodec copy -acodec aac d:/otest/case055_af_amix.mp4'
    ffmpeg_run(log, cmd, flag_af_amix, 'case_af_amix')

    # 48 adelay 延迟
    af_str = " adelay=delays=1500:all=1"
    ffmpeg_af_run(log, af_str, 'd:/otest/case056_af_adelay.mp4', flag_af_adelay, 'case_af_adelay')
    # 49 aecho 回声
    af_str = " aecho=0.8:0.88:60:0.4"
    ffmpeg_af_run(log, af_str, 'd:/otest/case057_af_aecho.mp4', flag_af_aecho, 'case_af_aecho')
    # 50 afade 淡入淡出
    af_str = " afade=t=in:ss=0:d=5"
    ffmpeg_af_run(log, af_str, 'd:/otest/case058_af_afadein.mp4', flag_af_afade, 'case_af_afade')
    # 51 aloop 循环
    af_str = " aloop=loop=-1"
    ffmpeg_af_run(log, af_str, 'd:/otest/case059_af_aloop.mp4', flag_af_aloop, 'case_af_aloop')
    # 52 asubboost 低音炮效果
    af_str = " asubboost=dry=0.5:wet=0.8:decay=0.7:feedback=0.5:cutoff=100:slope=0.5:delay=20"
    ffmpeg_af_run(log, af_str, 'd:/otest/case060_af_asubboost.mp4', flag_af_asubboost, 'case_af_asubboost')
    # 53 atempo 节拍速度
    af_str = " atempo=0.5"
    ffmpeg_af_run(log, af_str, 'd:/otest/case061_af_atempo.mp4', flag_af_atempo, 'case_af_atempo')
    # 54 chorus 和声
    # | ^ " &等字符是特殊字符
    # 转义时，^^代表^，^|代表|，^"代表"等等
    #af_str = ''' chorus=0.7:0.9:55:0.4:0.25:2'''
    #af_str = ''' chorus='0.6:0.9:50^|60:0.4^|0.32:0.25^|0.4:2^|1.3' '''
    af_str = ''' chorus=0.5:0.9:50^|60^|40:0.4^|0.32^|0.3:0.25^|0.4^|0.3:2^|2.3^|1.3'''
    ffmpeg_af_run(log, af_str, 'd:/otest/case062_af_chorus.mp4', flag_af_chorus, 'case_af_chorus')
    # 55 aresample 重采样
    af_str = " aresample=44100"
    ffmpeg_af_run(log, af_str, 'd:/otest/case063_af_aresample.mp4', flag_af_aresample, 'case_af_aresample')
    # 56 tremolo 颤音
    af_str = " tremolo"
    ffmpeg_af_run(log, af_str, 'd:/otest/case064_af_tremolo.mp4', flag_af_tremolo, 'case_af_tremolo')

    ## end of all cases
    log.logger.info("=== all cases run ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

################################################################################
# end
#
