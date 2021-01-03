#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/**************************************************************************
#* ffmpeg_trc.py: transcode cases on windows: python 3.x, ffmpeg-4.3.1
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

#****************************************************************************
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

log_param       = hysmm_def.log_param
dst_dir         = hysmm_def.dst_dir
tt_src_dir      = 'e:/material/ffmpeg_hys_python'
input_mkv_file  = ' -y -i ' + tt_src_dir + '/tt.mkv '
input_mp4_file  = ' -y -i ' + tt_src_dir + '/tt.mp4 '
input_ts_file   = ' -y -i ' + tt_src_dir + '/tt.ts '
input_mp3_file  = ' -i    ' + tt_src_dir + '/es_mp3.mp3 '
input_png_file  = ' -f image2 -i ' + tt_src_dir + '/image/image-%03.png '
hls_cancat_file = tt_src_dir + '/hls_part/hls_concat.txt '
trc_out         = dst_dir + '/trc_out'


def ffmpeg_exec(log, cmd, flag, case_name):
    ffmpeg_run.ffmpeg_run(case_name, flag, log, cmd)
    return

#****************************************************************************
# case flags: (default: the first be set, please set others by yourself)
flag_mkv2mp4                     = True
flag_mkv2mpegts                  = True
flag_mkv2flv                     = True
flag_mpegts2mp4                  = True

flag_trc_libx264_aac_mkv2mp4     = True
flag_trc_libx265_aac_mkv2mp4     = True
flag_trc_h264_nvenc_mkv2mp4      = True
flag_trc_hevc_nvenc_mkv2mp4      = True
flag_trc_libx264_mpegts_cbr      = True

flag_cut_by_time                 = True
flag_extract_video_es            = True
flag_extract_audio_es            = True
flag_extract_png_from_video      = True
flag_extract_jpg_from_video      = True
flag_image2_png2video_no_audio   = True
flag_image2_png2video_with_audio = True

flag_segment_hls_spts            = True
flag_segment_mp4                 = True
flag_concat_mpegts               = True
flag_live_flv_stream             = True

#****************************************************************************
# main process
if __name__ == "__main__":
    # init logger
    log = hysmm_def.Logger('sys_all.log',level='debug')
    hysmm_def.Logger('sys_err.log', level='error')
    log.logger.info("========= program start ============")

    # check source and output dir, create output dir if necessary
    hysmm_def.checkDir(log, tt_src_dir)
    hysmm_def.createDirIfNotFound(log, dst_dir)
    hysmm_def.createDirIfNotFound(log, trc_out)
    hysmm_def.createDirIfNotFound(log, trc_out + '/png')
    hysmm_def.createDirIfNotFound(log, trc_out + '/jpg')

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
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f mp4 d:/otest/trc_out/case001_mkv2mp4.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -acodec copy -f mpegts d:/otest/trc_out/case002_mkv2ts.ts '
    cmd3 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec copy -acodec copy -f flv d:/otest/trc_out/case003_mkv2flv.flv '
    cmd4 = 'ffmpeg ' + log_param + input_ts_file  + ' -vcodec copy -acodec copy -f mp4 d:/otest/trc_out/case004_ts2mp4.mp4 '
    ffmpeg_exec(log, cmd1, flag_mkv2mp4,    'case_mkv2mp4')
    ffmpeg_exec(log, cmd2, flag_mkv2mpegts, 'case_mkv2mpegts')
    ffmpeg_exec(log, cmd3, flag_mkv2flv,    'case_mkv2flv')
    ffmpeg_exec(log, cmd4, flag_mpegts2mp4, 'case_mpegts2mp4')

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
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx264 -s 640x360 -bf 2 -g 25 -acodec aac  -max_muxing_queue_size 256 -f mp4 d:/otest/trc_out/case005_trc_h264_aac.mp4 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -vcodec libx265 -preset medium -s 640x360 -bf 2 -g 25 -acodec aac -max_muxing_queue_size 256 -f mp4 d:/otest/trc_out/case006_trc_hevc_aac.mp4 '
    cmd3 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 h264_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/otest/trc_out/case007_trc_nv_h264_aac.mp4 '
    cmd4 = 'ffmpeg ' + log_param + ' -c:v h264_cuvid -gpu 0 ' + input_mkv_file + ' -c:v:0 hevc_nvenc -gpu any -s 640x360 -g 25 -acodec copy  -max_muxing_queue_size 256 -f mp4 d:/otest/trc_out/case008_trc_nv_hevc_aac.mp4 '
    cmd5 = 'ffmpeg ' + log_param + input_mkv_file + ' -c:v:0 libx264 -s 640x360 -bf 2 -g 25 -b:v:0 1000k -minrate 1000k -maxrate 1000k -bufsize 1000k -c:a:0 aac -b:a:0 64k -max_muxing_queue_size 256 -muxrate 1250k -muxdelay 0.85 -pcr_period 33 -pat_period 0.1 -sdt_period 1.2 -f mpegts d:/otest/trc_out/case009_trc_h264_aac_cbr.ts '
    ffmpeg_exec(log, cmd1, flag_trc_libx264_aac_mkv2mp4, 'case_trc_libx264_aac_mkv2mp4')
    ffmpeg_exec(log, cmd2, flag_trc_libx265_aac_mkv2mp4, 'case_trc_libx265_aac_mkv2mp4')
    ffmpeg_exec(log, cmd3, flag_trc_h264_nvenc_mkv2mp4 , 'case_trc_h264_nvenc_mkv2mp4')
    ffmpeg_exec(log, cmd4, flag_trc_hevc_nvenc_mkv2mp4 , 'case_trc_hevc_nvenc_mkv2mp4')
    ffmpeg_exec(log, cmd5, flag_trc_libx264_mpegts_cbr , 'case_trc_libx264_mpegts_cbr')

    # 3 按时间截取视频 (ss: 起始时间 精度秒, t: 持续时间 精度秒，二种格式等同)
    #   ffmpeg -y -ss 00:01:30 -t 00:01:00 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #   ffmpeg -y -ss 90 -t 60 -i e:/material/tt.mkv -vcodec copy -acodec copy d:/part.mkv
    #
    cmd = 'ffmpeg ' + log_param + ' -ss 00:01:30 -t 00:01:00 '+ input_mkv_file + ' -vcodec copy -acodec copy d:/otest/trc_out/case010_cut_part.mkv '
    ffmpeg_exec(log, cmd, flag_cut_by_time, 'case_cut_by_time')

    # 4 分离视频，音频：提取成 ES 文件
    #   ffmpeg -y -i e:/material/tt.mkv -bsf:v h264_mp4toannexb -vcodec copy -an es_h264.h264
    #   ffmpeg -y -i e:/material/tt.mkv -acodec copy -vn es_aac.aac
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -bsf:v h264_mp4toannexb -vcodec copy -an d:/otest/trc_out/case011_es_h264.h264 '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -acodec copy -vn d:/otest/trc_out/case012_es_aac.aac '
    ffmpeg_exec(log, cmd1, flag_extract_video_es, 'case_extract_video_es')
    ffmpeg_exec(log, cmd2, flag_extract_audio_es, 'case_extract_audio_es')

    #
    # 5 从视频周期提取PNG/JPG图片(指定频率，图片分辨率)
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.png
    #   ffmpeg -y -i e:/material/tt.mkv -r 1 -s 640x360 -f image2 d:/otest/image-%04d.jpg
    #   -r 1: 一秒一张图片
    cmd1 = 'ffmpeg ' + log_param + input_mkv_file + ' -r 1 -s 640x360 -f image2 d:/otest/trc_out/png/image-%04d.png '
    cmd2 = 'ffmpeg ' + log_param + input_mkv_file + ' -r 1 -s 640x360 -f image2 d:/otest/trc_out/jpg/image-%04d.jpg '
    ffmpeg_exec(log, cmd1, flag_extract_png_from_video, 'case_extract_png_from_video')
    ffmpeg_exec(log, cmd2, flag_extract_jpg_from_video, 'case_extract_jpg_from_video')

    #
    # 6 序列化图片转视频
    #   纯视频
    #   ffmpeg -y -f image2 -i e:/material/image_png/image%3d.png -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/image2video_no_audio.mp4
    #   配音频
    #   ffmpeg -y -i e:/material/background.mp3 -i e:/material/image_png/image%3d.png -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/image2video_audio.mp4
    cmd1 = 'ffmpeg -y ' +                  input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/otest/trc_out/case012_image2video_no_audio.mp4'
    cmd2 = 'ffmpeg -y ' + input_mp3_file + input_png_file + ' -r 25 -vcodec libx264 -bf 2 -g 25 -f mp4 d:/otest/trc_out/case013_image2video_with_audio.mp4'
    ffmpeg_exec(log, cmd1, flag_image2_png2video_no_audio,   'case_image2_png2video_no_audio')
    ffmpeg_exec(log, cmd2, flag_image2_png2video_with_audio, 'case_image2_png2video_with_audio')

    # 7 视频切片(源为single program ts 或 mp4, 分片单位时间 60 秒)
    #
    #   ffmpeg -y -fflags +genpts -i d:/tt_h264_aac.ts -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 h264_part.m3u8
    #   ffmpeg -y -i test.mp4 -c copy -map 0 -f segment -segment_time 60 d:/part-%03d.mp4
    cmd1 = 'ffmpeg -fflags +genpts ' + input_ts_file + ' -map 0:0 -c:v:0 copy -map 0:1 -c:a:0 copy -hls_list_size 0 -hls_time 60 d:/otest/trc_out/case014_h264_part.m3u8'
    cmd2 = 'ffmpeg -fflags +genpts ' + input_mp4_file + ' -c copy -map 0 -f segment -segment_time 60 d:/otest/trc_out/case015_part-%03d.mp4'
    ffmpeg_exec(log, cmd1, flag_segment_hls_spts, 'case_segment_hls_spts')
    ffmpeg_exec(log, cmd2, flag_segment_mp4,      'case_segment_mp4')

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
    cmd = 'ffmpeg -y -f concat -safe 0 -i ' + hls_cancat_file + map_str + mux_str + ' -f mpegts d:/otest/trc_out/case016_concat_h264.ts '
    ffmpeg_exec(log, cmd, flag_concat_mpegts, 'case_concat_mpegts')

    # 9 输出实时流(结合rtmp-flv流媒体服务, flv通常需为H264+AAC格式)
    #   ffmpeg -re -stream_loop -1 -i e:/material/tt.mkv -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1"
    #
    cmd = 'ffmpeg -re -stream_loop -1 ' + log_param + input_ts_file + ' -vcodec copy -acodec aac -ar 48000 -ac 2 -b:a 64k -f flv "rtmp://192.168.128.111:1935/myapp/stream1" '
    ffmpeg_exec(log, cmd, flag_live_flv_stream, 'case_live_flv_stream')

    ## end of all cases
    log.logger.info("=== all cases run ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

#****************************************************************************
# end
#