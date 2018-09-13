@ECHO OFF&PUSHD %~DP0 &TITLE FFMPEG编码选项
mode con cols=150 lines=40
color 2F
>NUL 2>&1 REG.exe query "HKU\S-1-5-19" || (
    ECHO SET UAC = CreateObject^("Shell.Application"^) > "%TEMP%\Getadmin.vbs"
    ECHO UAC.ShellExecute "%~f0", "%1", "", "runas", 1 >> "%TEMP%\Getadmin.vbs"
    "%TEMP%\Getadmin.vbs"
    DEL /f /q "%TEMP%\Getadmin.vbs" 2>NUL
    Exit /b
)
:Menu
Cls
@ echo.
@ echo.　　　　HysProject 编 码 菜 单 选 项
@ echo.
@ echo.     H264编码(es): 1080p    →     请输入1
@ echo.                   720p     →     请输入2
@ echo.
@ echo.     H265编码(ts): 2160p    →     请输入3
@ echo.                   1080p    →     请输入4
@ echo.                   720p     →     请输入5
@ echo.
@ echo.     H265编码(es): 2160p    →     请输入6
@ echo.                   1080p    →     请输入7
@ echo.                   720p     →     请输入8
@ echo.
@ echo.     退出                   →     请输入9
@ echo.
set /p xj= 输入数字按回车：
if /i "%xj%"=="1" Goto H264enc1080p
if /i "%xj%"=="2" Goto H264enc720p
if /i "%xj%"=="3" Goto H265enc2160p
if /i "%xj%"=="4" Goto H265enc1080p
if /i "%xj%"=="5" Goto H265enc720p
if /i "%xj%"=="6" Goto H265enc2160p2es
if /i "%xj%"=="7" Goto H265enc1080p2es
if /i "%xj%"=="8" Goto H265enc720p2es
if /i "%xj%"=="9" Goto myExit
@ echo.
echo      选择无效，请重新输入
ping -n 2 127.1>nul 
goto menu
:H264enc1080p
@ echo.
ECHO 　　　H264编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1920x1080 -i bg1080p.yuv -r 25 -bf 0 -vcodec libx264 bg1080p.h264
goto h264finished
:H264enc720p
@ echo.
ECHO 　　　H264编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1280x720 -i bg720p.yuv -r 25 -bf 0 -vcodec libx264 bg720p.h264
goto h264finished
:H265enc2160p
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 3840x2160 -i bg2160p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" -f mpegts h265_2160p.ts
goto h265finished
:H265enc1080p
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1920x1080 -i bg1080p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" -f mpegts h265_1080p.ts
goto h265finished
:H265enc720p
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1280x720 -i bg720p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" -f mpegts h265_720p.ts
goto h265finished
:H265enc2160p2es
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 3840x2160 -i bg2160p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" h265_2160p.h265
goto h265finished
:H265enc1080p2es
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1920x1080 -i bg1080p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" h265_1080p.h265
goto h265finished
:H265enc720p2es
@echo.
ECHO 　　　H265编码中..请稍等..
taskkill /f /im ffmpeg*>NUL 2>NUL
ffmpeg.exe -pix_fmt yuv420p -s 1280x720 -i bg720p.yuv -r 25 -bf 0 -vcodec libx265 -x265-params "keyint=25:bframes=0" h265_720p.h265
goto h265finished
:myExit
@ echo.
echo 　　　正在退出..请稍等..
taskkill /f /im et*>NUL 2>NUL
goto Exit2
:h264finished
@ ECHO.
ECHO 　　　h264编码完成！
ping -n 3 127.8>nul
goto menu
:h265finished
@ ECHO.
ECHO 　　　h265编码完成！
ping -n 3 127.8>nul
goto menu
:Exit2
@ ECHO.
ECHO 　　　退出完成！
ping -n 2 127.8>nul
goto menu
