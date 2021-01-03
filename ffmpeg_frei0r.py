#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/****************************************************************************
#* ffmpeg_frei0r.py: ffmpeg frei0r cases on windows, based on ffmpeg-4.3.1
#*****************************************************************************
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
#****************************************************************************/
import os
import re
import sys
import hysmm_def
import ffmpeg_run

#*****************************************************************************
# 通用字符串常量 定义在 hysmm_def.py
# 统一的输入参数，本文以常见的mkv（H264+AAC）格式为测试素材
# (其中部分需要用到的mpegts文件，采用它派生的tt.ts)
# 测试前的准备工作
# 1）PC 上有 D、E 分区
# 2）E分区上准备下面 mkv/mp4/ts 源文件: 推荐格式为 H264+AAC
# 3）准备测试素材
log_param       = hysmm_def.log_param
src_dir         = hysmm_def.src_dir
dst_dir         = hysmm_def.dst_dir

input_mp4_file  = " -y -i " + src_dir + "/mp4_h264_1080p_2020_琅琊榜.mp4 "
input_flv_file  = hysmm_def.input_flv_file
frei0r_out      = dst_dir + "/frei0r_effect"

#*****************************************************************************
# case flags
play_flag = False   # true - ffplay,  false - ffmpeg
sfx       = '.gif'  # .gif or .ts
start_num = 1
end_num   = 74

class frei0r_case_c:
    def __init__(self):
        self.dst_concat_file = dst_dir + '/dst_frei0r_concat.ts'
        self.hls_concat_file = dst_dir + '/hls_frei0r_concat.txt'
        self.case001 = [frei0r_out + '/d001_b' + sfx,                    " frei0r='filter_name=B' "]
        self.case002 = [frei0r_out + '/d002_g' + sfx,                    " frei0r='filter_name=G' "]
        self.case003 = [frei0r_out + '/d003_r' + sfx,                    " frei0r='filter_name=R' "]
        self.case004 = [frei0r_out + '/d004_colordistance_7f7f7f' + sfx, " frei0r='filter_name=colordistance:0x7f7f7f' "]
        self.case005 = [frei0r_out + '/d005_colordistance_000000' + sfx, " frei0r='filter_name=colordistance:0x000000' "]
        self.case006 = [frei0r_out + '/d006_3dflippo' + sfx,             " frei0r='filter_name=3dflippo' "]
        self.case007 = [frei0r_out + '/d007_perspective' + sfx,          " frei0r='filter_name=perspective:0.2/0.2^|0.8/0.2' "]
        self.case008 = [frei0r_out + '/d008_IIRblur' + sfx,              " frei0r='filter_name=IIRblur:filter_params=0.1^|0.933344' "]
        self.case009 = [frei0r_out + '/d009_alpha0ps' + sfx,             " frei0r='filter_name=alpha0ps' "]
        self.case010 = [frei0r_out + '/d010_alphagrad' + sfx,            " frei0r='filter_name=alphagrad' "]
        self.case011 = [frei0r_out + '/d011_alphaspot' + sfx,            " frei0r='filter_name=alphaspot' "]
        self.case012 = [frei0r_out + '/d012_balanc0r' + sfx,             " frei0r='filter_name=balanc0r:filter_params=0x5080ee^|0.9' "]
        self.case013 = [frei0r_out + '/d013_bgsubtract0r' + sfx,         " frei0r='filter_name=bgsubtract0r' "]
        self.case014 = [frei0r_out + '/d014_brightness' + sfx,           " frei0r='filter_name=brightness:0.9' "]
        self.case015 = [frei0r_out + '/d015_bw0r' + sfx,                 " frei0r='filter_name=bw0r' "]
        self.case016 = [frei0r_out + '/d016_c0rners_1x' + sfx,           " frei0r='filter_name=c0rners:0.8' "]
        self.case017 = [frei0r_out + '/d017_c0rners_1xy' + sfx,          " frei0r='filter_name=c0rners:0.4^|0.5' "]
        self.case018 = [frei0r_out + '/d018_c0rners_12xy' + sfx,         " frei0r='filter_name=c0rners:0.4^|0.5^|0.4^|0.4' "]
        self.case019 = [frei0r_out + '/d019_c0rners_123xy' + sfx,        " frei0r='filter_name=c0rners:0.8^|0.5^|0.3^|0.3^|0.4^|0.4' "]
        self.case020 = [frei0r_out + '/d020_c0rners_1234xy' + sfx,       " frei0r='filter_name=c0rners:0.8^|0.5^|0.3^|0.3^|0.4^|0.4^|0.3^|0.6' "]
        self.case021 = [frei0r_out + '/d021_cluster' + sfx,              " frei0r='filter_name=cluster:0.5^|0.5' "]
        self.case022 = [frei0r_out + '/d022_colgate' + sfx,              " frei0r='filter_name=colgate:#1f1f1f^|0.1333' "]
        self.case023 = [frei0r_out + '/d023_coloradj_RGB' + sfx,         " frei0r='filter_name=coloradj_RGB:0.9^|0.5^|0.1^|0.333344' "]
        # 视频黑屏
        self.case024 = [frei0r_out + '/d024_colorhalftone' + sfx,        " frei0r='filter_name=colorhalftone:0.3^|0.7^|0.05^|0.25' "]
        self.case025 = [frei0r_out + '/d025_colorize' + sfx,             " frei0r='filter_name=colorize:0.8^|0.8^|0.8' "]
        self.case026 = [frei0r_out + '/d026_defish0r' + sfx,             " frei0r='filter_name=defish0r:1' "] # 鱼眼
        self.case027 = [frei0r_out + '/d027_distort0r' + sfx,            " frei0r='filter_name=distort0r:filter_params=0.15^|0.25' "]
        self.case028 = [frei0r_out + '/d028_dither' + sfx,               " frei0r='filter_name=dither:filter_params=0.1^|0.5' "]
        self.case029 = [frei0r_out + '/d029_emboss' + sfx,               " frei0r='filter_name=emboss:0.875^|0.8333^|0.825' "]
        self.case030 = [frei0r_out + '/d030_flippo' + sfx,               " frei0r='filter_name=flippo:y^|n' "]
        self.case031 = [frei0r_out + '/d031_gamma' + sfx,                " frei0r='filter_name=gamma:0.5' "]
        self.case032 = [frei0r_out + '/d032_glitch0r' + sfx,             " frei0r='filter_name=glitch0r:0^|0.5^|0.1^|0.1' "]
        self.case033 = [frei0r_out + '/d033_glow' + sfx,                 " frei0r='filter_name=glow:0.9' "]
        self.case034 = [frei0r_out + '/d034_hqdn3d' + sfx,               " frei0r='filter_name=hqdn3d:0.92^|0.92' "]
        self.case035 = [frei0r_out + '/d035_hueshift0r' + sfx,           " frei0r='filter_name=hueshift0r:0.6' "]
        self.case036 = [frei0r_out + '/d036_invert0r' + sfx,             " frei0r='filter_name=invert0r' "]
        # 没有明显效果
        self.case037 = [frei0r_out + '/d037_keyspillm0pup' + sfx,        " frei0r='filter_name=keyspillm0pup:#000000^|#ffffff^|0^|0.24^|0.4^|0.25^|0.15^|1^|0.55' "]
        self.case038 = [frei0r_out + '/d038_lenscorrection1' + sfx,      " frei0r='filter_name=lenscorrection:0.5^|0.5^|0.8^|0.8^|0.9' "]
        self.case039 = [frei0r_out + '/d039_lenscorrection2' + sfx,      " frei0r='filter_name=lenscorrection:0.5^|0.5^|0.2^|0.2^|0.8' "]
        self.case040 = [frei0r_out + '/d040_letterb0xed' + sfx,          " frei0r='filter_name=letterb0xed:0.6^|y' "] # 默认值0.4，在原视频上下部分按比例涂为黑色，做成电影效果
        self.case041 = [frei0r_out + '/d041_levels_1' + sfx,             " frei0r='filter_name=levels:0^|0^|1^|0.25^|0^|1^|y^|0.2' "]
        self.case042 = [frei0r_out + '/d042_levels_2' + sfx,             " frei0r='filter_name=levels:1^|1^|1^|0.25^|0^|1^|y^|0.3' "]#黑色
        self.case043 = [frei0r_out + '/d043_levels_3' + sfx,             " frei0r='filter_name=levels:1^|1^|1^|0.25^|1^|0^|y^|0.3' "]#白色
        self.case044 = [frei0r_out + '/d044_levels_4' + sfx,             " frei0r='filter_name=levels:0^|1^|0^|0.25^|0^|0^|y^|0.1' "]
        self.case045 = [frei0r_out + '/d045_luminance' + sfx,            " frei0r='filter_name=luminance' "] # 黑白图像， 无参数
        self.case046 = [frei0r_out + '/d046_mask0mate_0' + sfx,          " frei0r='filter_name=mask0mate:0.1^|0.2^|0.2^|0.2^|n^|0.1' "]
        self.case047 = [frei0r_out + '/d047_mask0mate_1' + sfx,          " frei0r='filter_name=mask0mate:0.1^|0.2^|0.2^|0.2^|y^|0.2' "]
        # Choose type of median: Cross5, Square3x3, Bilevel, Diamond3x3, Square5x5, Temp3, Temp5, ArceBI, ML3D, ML3dEX, VarSize
        self.case048 = [frei0r_out + '/d048_medians' + sfx,              " frei0r='filter_name=medians:Diamond3x3^|0.4' "]
        self.case049 = [frei0r_out + '/d049_normaliz0r_0' + sfx,         " frei0r='filter_name=normaliz0r:#ff0000^|#ffffff^|0.3^|1^|1' "]
        self.case050 = [frei0r_out + '/d050_normaliz0r_1' + sfx,         " frei0r='filter_name=normaliz0r:#00ff00^|#ffffff^|0.3^|1^|1' "]
        self.case051 = [frei0r_out + '/d051_normaliz0r_2' + sfx,         " frei0r='filter_name=normaliz0r:#0000ff^|#ffffff^|0.3^|1^|1' "]
        self.case052 = [frei0r_out + '/d052_normaliz0r_3' + sfx,         " frei0r='filter_name=normaliz0r:#ff0000^|#000000^|0.3^|1^|1' "]
        self.case053 = [frei0r_out + '/d053_pixeliz0r' + sfx,            " frei0r='filter_name=pixeliz0r:0.02^|0.02' "]
        self.case054 = [frei0r_out + '/d054_posterize' + sfx,            " frei0r='filter_name=posterize:0.1' "] #油画效果
        self.case055 = [frei0r_out + '/d055_pr0be_1_rgb' + sfx,          " frei0r='filter_name=pr0be:0^|0.5^|0.5^|0.25^|0.25^|n^|y^|n' "]
        self.case056 = [frei0r_out + '/d056_pr0be_2_yuv' + sfx,          " frei0r='filter_name=pr0be:0.5^|0.5^|0.5^|0.25^|0.25^|n^|n^|n' "]
        self.case057 = [frei0r_out + '/d057_pr0be_3_hsv' + sfx,          " frei0r='filter_name=pr0be:1^|0.2^|0.2^|0.55^|0.55^|y^|n^|y' "]
        self.case058 = [frei0r_out + '/d058_pr0file' + sfx,              " frei0r='filter_name=pr0file' "]
        self.case059 = [frei0r_out + '/d059_rgbnoise' + sfx,             " frei0r='filter_name=rgbnoise:0.3' "]
        self.case060 = [frei0r_out + '/d060_rgbsplit0r' + sfx,           " frei0r='filter_name=rgbsplit0r:0.2^|0.2' "]
        self.case061 = [frei0r_out + '/d061_saturat0r' + sfx,            " frei0r='filter_name=saturat0r:0.5' "]
        self.case062 = [frei0r_out + '/d062_select0r' + sfx,             " frei0r='filter_name=select0r' "] # 需要进一步调参数
        self.case063 = [frei0r_out + '/d063_sharpness' + sfx,            " frei0r='filter_name=sharpness:0.7^|0.5' "] #锐化突出轮廓
        self.case064 = [frei0r_out + '/d064_sigmoidaltransfer' + sfx,    " frei0r='filter_name=sigmoidaltransfer:0.75^|0.85' "]#黑白肖像
        self.case065 = [frei0r_out + '/d065_softglow' + sfx,             " frei0r='filter_name=softglow:0.5^|0.75^|0.85^|0' "]
        self.case066 = [frei0r_out + '/d066_spillsupress' + sfx,         " frei0r='filter_name=spillsupress:0.5' "]
        self.case067 = [frei0r_out + '/d067_squareblur' + sfx,           " frei0r='filter_name=squareblur:0.01' "]
        self.case068 = [frei0r_out + '/d068_tehRoxx0r' + sfx,            " frei0r='filter_name=tehRoxx0r:0.0001' "]
        self.case069 = [frei0r_out + '/d069_3point_balance' + sfx,       " frei0r='filter_name=three_point_balance:#ff00ff^|#7f7f7f^|#ffffff^|y^|y' "]
        self.case070 = [frei0r_out + '/d070_threshold0r' + sfx,          " frei0r='filter_name=threshold0r:0.5' "]
        self.case071 = [frei0r_out + '/d071_tint0r' + sfx,               " frei0r='filter_name=tint0r:#ff0000^|#7fff7f^|0.55' "]
        self.case072 = [frei0r_out + '/d072_transparency' + sfx,         " frei0r='filter_name=transparency:0.6' "]
        self.case073 = [frei0r_out + '/d073_vertigo' + sfx,              " frei0r='filter_name=vertigo:0.02^|0.5' "]

        # unsupported now: comment by zengyong on 2020.12.31
        #self.case099 = [frei0r_out + '/d101_aech0r' + sfx,              " frei0r='filter_name=aech0r' "]
        #self.case099 = [frei0r_out + '/d102_baltan' + sfx,              " frei0r='filter_name=baltan' "]
        #self.case099 = [frei0r_out + '/d103_bluescreen0r' + sfx,        " frei0r='filter_name=bluescreen0r' "]
        #self.case099 = [frei0r_out + '/d104_cairogradient' + sfx,       " frei0r='filter_name=cairogradient' "]
        #self.case099 = [frei0r_out + '/d105_cairoimagegrid' + sfx,      " frei0r='filter_name=cairoimagegrid' "]
        #self.case099 = [frei0r_out + '/d106_cartoon' + sfx,             " frei0r='filter_name=cartoon' "]
        #self.case099 = [frei0r_out + '/d026_colortap' + sfx,            " frei0r='filter_name=colortap' "]
        #self.case099 = [frei0r_out + '/d026_contrast0r' + sfx,          " frei0r='filter_name=constrast0r' "]
        #self.case099 = [frei0r_out + '/d026_curves' + sfx,              " frei0r='filter_name=curves' "]
        #self.case099 = [frei0r_out + '/d026_d90stairsteppingfix' + sfx, " frei0r='filter_name=d90stairsteppingfix' "]
        #self.case099 = [frei0r_out + '/d027_delay0r' + sfx,             " frei0r='filter_name=delay0r' "]
        #self.case099 = [frei0r_out + '/d027_delaygrab' + sfx,           " frei0r='filter_name=delaygrab' "]
        #self.case099 = [frei0r_out + '/d038_edgeglow' + sfx,            " frei0r='filter_name=edgeglow' "]
        #self.case099 = [frei0r_out + '/d039_elastic_scale' + sfx,       " frei0r='filter_name=elastic_scale' "]
        #self.case099 = [frei0r_out + '/d030_equaliz0r' + sfx,           " frei0r='filter_name=equaliz0r' "]
        #self.case099 = [frei0r_out + '/d042_facebl0r' + sfx,            " frei0r='filter_name=facebl0r' "]
        #self.case099 = [frei0r_out + '/d043_facedetect' + sfx,          " frei0r='filter_name=facedetect' "]
        #self.case099 = [frei0r_out + '/d055_lightgraffiti' + sfx,       " frei0r='filter_name=lightgraffiti' "]
        #self.case099 = [frei0r_out + '/d059_ndvi' + sfx,                " frei0r='filter_name=ndvi' "]
        #self.case099 = [frei0r_out + '/d060_nervous' + sfx,             " frei0r='filter_name=nervous' "]
        #self.case099 = [frei0r_out + '/d062_nosync0r' + sfx,            " frei0r='filter_name=nosync0r' "]
        #self.case099 = [frei0r_out + '/d067_premultiply' + sfx,         " frei0r='filter_name=premultiply' "]
        #self.case099 = [frei0r_out + '/d068_primaries' + sfx,           " frei0r='filter_name=primaries' "]
        #self.case099 = [frei0r_out + '/d070_rgbparade' + sfx,           " frei0r='filter_name=rgbparade' "]
        #self.case099 = [frei0r_out + '/d073_scale0tilt' + sfx,          " frei0r='filter_name=scale0tilt' "]
        #self.case099 = [frei0r_out + '/d074_scanline0r' + sfx,          " frei0r='filter_name=scanline0r' "]
        #self.case099 = [frei0r_out + '/d078_sobel' + sfx,               " frei0r='filter_name=sobel' "]
        #self.case099 = [frei0r_out + '/d080_sopsat' + sfx,              " frei0r='filter_name=sopsat' "]
        #self.case099 = [frei0r_out + '/d086_threelay0r' + sfx,          " frei0r='filter_name=threelay0r' "]
        #self.case099 = [frei0r_out + '/d088_timeout' + sfx,             " frei0r='filter_name=timeout' "]
        #self.case099 = [frei0r_out + '/d091_twolay0r' + sfx,            " frei0r='filter_name=twolay0r' "]
        #self.case099 = [frei0r_out + '/d092_vectorscope' + sfx,         " frei0r='filter_name=vectorscope' "]
        #self.case099 = [frei0r_out + '/d094_vignette' + sfx,            " frei0r='filter_name=vignette:filter_params=0.5^|0.2^|0.5' "]

#*****************************************************************************
# main process
if __name__ == "__main__":
    # init logger
    log = hysmm_def.Logger('sys_all.log', level='debug')
    hysmm_def.Logger('sys_err.log', level='error')
    log.logger.info("========= program start ============")

    # check source and output dir, create output dir if necessary
    hysmm_def.checkDir(log, src_dir)
    hysmm_def.createDirIfNotFound(log, dst_dir)
    hysmm_def.createDirIfNotFound(log, frei0r_out)

    # init frei0r case
    frei0r_case      = frei0r_case_c()
    frei0r_case_dict = frei0r_case.__dict__

    #***************************************
    # cut short slice from source file
    # ffmpeg -y -i e:/material/tt.mkv -vcodec copy -acodec copy -f mp4 d:/tt.mp4
    #
    video_param_str = ' '
    gif_str    = ' -an -s 320x240 -r 15 -pix_fmt rgb8 '
    mpegts_str = ' -an -s 640x360 -r 25 -pix_fmt yuv420p -vcodec libx264 -b 500k -minrate 500k -maxrate 900k -bufsize 500k -g 25 -bf 2 ' + hysmm_def.tsmux_vbr_str
    if (sfx == '.gif'):
        video_param_str = gif_str
    else:
        video_param_str = mpegts_str
    log.logger.info(video_param_str)

    for i in range(start_num, end_num):
        idx = '%03d' %i
        key = "case" + idx
        input_file  = input_mp4_file
        output_file = frei0r_case_dict[key][0]
        frei0r_str  = ' -vf ' + frei0r_case_dict[key][1]
        log.logger.info("key:%s, frei0r: %s,  dst: %s", key, frei0r_str, output_file)

        if (play_flag):
            cmd = 'ffplay ' + log_param  + input_flv_file + frei0r_str
            ffmpeg_run.ffplay_run(key, True, log, cmd)
        else:
            cmd = 'ffmpeg ' + log_param + input_file + ' -t 10 ' + frei0r_str  + video_param_str + output_file
            ffmpeg_run.ffmpeg_run(key, True, log, cmd)

    ## end of case
    log.logger.info("=== finished ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

#*****************************************************************************
# end
#