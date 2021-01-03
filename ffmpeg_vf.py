#!/usr/bin/python
# -*- coding: UTF-8 -*-

#/**************************************************************************
#* ffmpeg_vf.py: video filter cases on windows: python 3.x, ffmpeg-4.3.1
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
input_mkv_file = ' -i ' + tt_src_dir + '/tt.mkv '
input_mp4_file = ' -i ' + tt_src_dir + '/tt.mp4 '
input_ts_file  = ' -i ' + tt_src_dir + '/tt.ts '
input_mp3_file = ' -i ' + tt_src_dir + '/es_mp3.mp3 '
input_png_file = ' -f image2 -i ' + tt_src_dir + '/image/image-%03.png '
hls_cancat_file= tt_src_dir + '/hls_part/hls_concat.txt '
vf_out = dst_dir + '/vf_effect'

#log, vf_str, 'd:/otest/case019_vf_crop.mp4', flag_vf_crop, 'case_vf_crop'
def ffmpeg_vf_exec(log, vf_str, output_file_name, flag, case_name):
    ffmpeg_run.ffmpeg_vf_run(case_name, flag, log, input_mkv_file, vf_str, output_file_name)
    return
################################################################################
# case flags: (default: the first be set, please set others by yourself)
overlay_flag = False
play_flag    = False    # true - ffplay, false - ffmpeg
sfx          = '.ts'   # .gif or .ts
start_num    = 3
end_num      = 39

class vf_case_c:
    def __init__(self):

        # crop=w=%d:h=%d:x=%d:y=%d
        # 注释：宽度:高度:x:y(x,y如果不写则从中心裁剪)
        # 注意事项：width, height, x, y 不要超出原始视频边界
        self.case002 = [vf_out + '/d002_crop' + sfx,               " crop=w=960:h=540:x=80:y=40 "]
        self.case003 = [vf_out + '/d003_rotate_1_dynamic' + sfx,   " rotate='PI*2/10*t' "]            # 视频动态旋转 (T为旋转360度的时间常量, 单位:秒)
        self.case004 = [vf_out + '/d004_rotate_2_45degress' + sfx, " rotate='PI/4' "]                 # 视频旋转45度 (保留原始尺寸)
        self.case005 = [vf_out + '/d005_rotate_3_45degress' + sfx, " rotate='PI/4:ow=floor(hypot(iw,ih)/4)*4:oh=ow:c=none' "] # 视频旋转45度，以对角线长度为宽高
        self.case006 = [vf_out + '/d006_transpose_1_cw90' + sfx,   " transpose=1:portrait "]          # 视频顺时针旋转90 (transpose=1)
        self.case007 = [vf_out + '/d007_transpose_2_ccw90' + sfx,  " transpose=2 "]                   # 视频逆时针旋转90 (transpose=2)
        self.case008 = [vf_out + '/d008_transpose_3' + sfx,        " transpose=3 "]                   # 视频逆时针旋转90度后垂直镜像 (transpose=3)
        self.case009 = [vf_out + '/d009_hflip_vflip' + sfx,        " hflip,vflip "]                   # 视频顺时针旋转180度 (hflip,vflip)
        self.case010 = [vf_out + '/d010_hflip' + sfx,              " hflip "]                         # 视频水平镜像 (hflip)
        self.case011 = [vf_out + '/d011_vflip' + sfx,              " vflip "]                         # 视频竖直镜像 (vflip)
        # 视频文字跑马灯效果 (drawtext)
        vf_str1= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-hr-left2right':x=90+t*40:y=60:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
        vf_str2= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-hr-right2left':x=1200-t*40:y=360:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
        vf_str3= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-ve-up2down':x=100:y=10+t*20:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
        vf_str4= '''drawtext=fontfile=c:/Windows/Fonts/Medium.ttf:text='welcome-ve-down2up':x=400:y=700-t*20:fontsize=36:fontcolor=#ffffff@0.7:shadowy=-1'''
        vf_marquee_str= vf_str1 + ',' + vf_str2 + ',' + vf_str3 + ',' + vf_str4
        self.case012 = [vf_out + '/d012_drawtext' + sfx, vf_marquee_str]

        self.case013 = [vf_out + '/d013_drawgrid' + sfx,           " drawgrid=width=80:height=80:thickness=2:color=yellow@0.9 "] # 网格
        self.case014 = [vf_out + '/d014_drawbox' + sfx,            " drawbox=x=10:y=10:w=860:h=480:color=pink@0.5:t=fill "] # box框
        self.case015 = [vf_out + '/d015_boxblur' + sfx,            " boxblur=2:1:cr=0:ar=0 "]
        self.case016 = [vf_out + '/d016_edgedetect' + sfx,         " edgedetect=low=0.1:high=0.4 "]
        self.case017 = [vf_out + '/d017_eq' + sfx,                 " eq=contrast=1.5:brightness=0.5 "]
        self.case018 = [vf_out + '/d018_fadein' + sfx,             " fade=in:0:250 "]
        self.case019 = [vf_out + '/d019_fadeout' + sfx,            " fade=out:0:250 "]
        self.case020 = [vf_out + '/d020_geq' + sfx,                " format=gray,geq=lum_expr='(p(X,Y)+(256-p(X-4,Y-4)))/2' "]
        self.case021 = [vf_out + '/d021_histogram' + sfx,          " histogram "]
        self.case022 = [vf_out + '/d022_histeq' + sfx,             " histeq=strength=0.5:intensity=0.4:antibanding=weak "]
        self.case023 = [vf_out + '/d023_hqdn3d' + sfx,             " hqdn3d "]
        self.case024 = [vf_out + '/d024_hue' + sfx,                " hue=h=90:s=1:b=5 "]
        self.case025 = [vf_out + '/d025_il' + sfx,                 " il=l=d:c=d "]
        self.case026 = [vf_out + '/d026_lutyuv' + sfx,             " lutyuv='y=maxval+minval-val:u=maxval+minval-val:v=maxval+minval-val' "]
        self.case027 = [vf_out + '/d027_negate' + sfx,             " negate "]
        self.case028 = [vf_out + '/d028_oscilloscope' + sfx,       " oscilloscope=x=1:y=0.5:s=1:t=1 "]
        self.case029 = [vf_out + '/d029_pad' + sfx,                " pad='iw*1.1:ih*1.1:(ow-iw)/2:(oh-ih)/2:color=violet' "]
        self.case030 = [vf_out + '/d030_showpalette' + sfx,        " showpalette "]
        self.case031 = [vf_out + '/d031_shuffleplanes' + sfx,      " shuffleplanes=0:2:1:3 "]
        self.case032 = [vf_out + '/d032_sobel' + sfx,              " sobel "]
        self.case033 = [vf_out + '/d033_stereo3d' + sfx,           " stereo3d=abl:sbsr "]
        self.case034 = [vf_out + '/d034_swapuv' + sfx,             " swapuv "]
        self.case035 = [vf_out + '/d035_tile' + sfx,               " scale=224:180,tile=4x3:nb_frames=12:padding=2:margin=2 "]# 42 tile 填充参数需注意，确保不造成奇数宽或高
        self.case036 = [vf_out + '/d036_unsharp' + sfx,            " unsharp "]
        self.case037 = [vf_out + '/d037_vignette' + sfx,           " vignette='PI/4+random(1)*PI/50' "] # 闪烁渐晕
        self.case038 = [vf_out + '/d038_delogo' + sfx,             " delogo=w=200:h=80:x=1000:y=50 "]

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
    hysmm_def.createDirIfNotFound(log, vf_out)

    # init vf case
    vf_case      = vf_case_c()
    vf_case_dict = vf_case.__dict__

    #####################################################
    # overlay image logos(png/bmp/webp/gif/jpeg) , draw text
    #   ffmpeg -fflags +genpts -i main_video.mkv -i logo1.png -i logo2.jpg -max_muxing_queue_size 256
    #          -filter_complex "[0:v][1:v]overlay=40:40[bkg1];[bkg1][2:v]overlay=200:40,"\
    #          "drawtext=fontfile=/fonts/mingliu.ttc:text='hybase@qq.com 视频水印1':x=50:y=450:fontsize=32:fontcolor=0xFFEE00@0.7:shadowy=-1,"\
    #          "drawtext=fontfile=/fonts/mingliu.ttc:text='hybase@qq.com 视频水印2':x=350:y=450:fontsize=32:fontcolor=0xFFEE00@0.7:shadowy=-1"\
    #          -map 0:0 -c:v:0 libx264 -s 1280x720 -b:v:0 1500000 -minrate 1500000 -maxrate 3000000 -bufsize 1500000 -g 25 -bf 1 -pix_fmt yuv420p -r:v:0 25.000000 \
    #          -map 0:1 -c:a:0 aac -ab:a:0 64k -ar:a:0 48000 -ac:a:0 2 -vol:a:0 256 \
    #          -map 0:1 -c:a:1 ac3 -ab:a:1 128k -ar:a:1 48000 -ac:a:1 2 -vol:a:1 256 \
    #          -muxrate 0 -f mpegts d:/output.ts
    tsmux_str   = hysmm_def.tsmux_vbr_str
    png_logo    = ' -i e:/material/image/logo/jxtv_96x96.png '
    jpg_logo    = ' -i e:/material/image/logo/jxtv_96x96.jpg '
    overlay_str = '[0:v][1:v]overlay=60:40[bkg1];[bkg1][2:v]overlay=200:40'
    drawtext1   = '''drawtext=fontfile=c:/Windows/Fonts/msyh.ttf:text='hybase@qq.com视频水印1':x=50:y=550:fontsize=36:fontcolor=0xFFFF00@0.7:shadowy=-1,'''
    drawtext2   = '''drawtext=fontfile=c:/Windows/Fonts/msyh.ttf:text='hybase@qq.com视频水印2':x=50:y=650:fontsize=36:fontcolor=0xFFFF00@0.7:shadowy=-1'''
    video_param = ' -map 0:0 -c:v:0 libx264 -s 1280x720 -b:v:0 1500000 -minrate 1500000 -maxrate 3000000 -bufsize 1500000 -g 25 -bf 1 -pix_fmt yuv420p -r:v:0 25.000000 '
    aac_str     = ' -map 0:1 -c:a:0 aac -ab:a:0 64k -ar:a:0 48000 -ac:a:0 2 -vol:a:0 256 '
    ac3_str     = ' -map 0:1 -c:a:1 ac3 -ab:a:1 128k -ar:a:1 48000 -ac:a:1 2 -vol:a:1 256 '

    common_str = 'ffmpeg -y -fflags +genpts ' + log_param + input_ts_file + png_logo + jpg_logo + ' -max_muxing_queue_size 256 -filter_complex ' + overlay_str
    cmd1 = common_str + video_param + aac_str + ac3_str + tsmux_str + vf_out + '/case000_overlay_logos.ts'
    cmd2 = common_str + ',' + drawtext1 + drawtext2 + video_param + aac_str + ac3_str + tsmux_str + vf_out + '/case001_overlay_logo_drawtext.ts '
    ffmpeg_run.ffmpeg_run('case_vf_overlay_logos'   , overlay_flag, log, cmd1)
    ffmpeg_run.ffmpeg_run('case_vf_overlay_drawtext', overlay_flag, log, cmd2)

    # ***********************************
    # gif or video format string
    video_param_str = ' '
    gif_str    = ' -an -s 1280x720 -r 15 -pix_fmt rgb8 '
    mpegts_str = ' -an -s 1280x720 -r 25 -pix_fmt yuv420p -vcodec libx264 -b 1500k -minrate 1500k -maxrate 2000k -bufsize 1500k -g 25 -bf 2 ' + hysmm_def.tsmux_vbr_str
    if (sfx == '.gif'):
        video_param_str = gif_str
    else:
        video_param_str = mpegts_str
    log.logger.info(video_param_str)

    for i in range(start_num, end_num):
        idx = '%03d' %i
        key = "case" + idx
        input_file  = input_mp4_file
        output_file = vf_case_dict[key][0]

        if (play_flag):
            vf_str = ' -vf ' + vf_case_dict[key][1]
            log.logger.info("key:%s, vf: %s, dst: %s", key, vf_str, output_file)
            cmd = 'ffplay ' + log_param + input_file + vf_str
            ffmpeg_run.ffplay_run(key, True, log, cmd)
        else:
            vf_str = ' -filter_complex ' + vf_case_dict[key][1]
            log.logger.info("key:%s, vf: %s, dst: %s", key, vf_str, output_file)
            cmd = 'ffmpeg -y ' + log_param + input_file + ' -t 10 ' + vf_str  + video_param_str + output_file
            ffmpeg_run.ffmpeg_run(key, True, log, cmd)

    #  frei0r cases please reference to "ffmpeg_frei0r.py"
    ## end of all cases
    log.logger.info("=== all cases run ===")
    log.logger.info("============ program exit ============")
    sys.exit(0)

################################################################################
# end
#