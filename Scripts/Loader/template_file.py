# -*- coding: utf-8 -*-
"""rdc 2.1.1(110309) 参数说明

==========登录==========
ConnectionString:       [string]        IP地址
UserName:               [string]        用户名
Domain:                 [String]        域
AddToKeychain:          [bool]          将用户信息添加到钥匙串
AutoReconnect:          [bool]          断开连接后自动重新连接

==========显示==========
DesktopSize:            [dict]          远程桌面大小
    [dict] DesktopHeight    [integer]   高度
    [dict] DesktopWidth     [integer]   宽度
DesktopSize:            [String]        远程桌面大小  DesktopFullScreen: 全屏
ColorDepth:             [integer]       颜色  0: 千  1: 百万
Display:                [integer]       打开远程桌面窗口  0: 主显示器
Wallpaper               [bool]          显示桌面背景
FontSmoothing:          [bool]          显示字体平滑
FullWindowDrag:         [bool]          拖动时显示窗口内容
MenuAnimations:         [bool]          显示菜单和窗口动画
Themes:                 [bool]          显示主题
BitmapCaching:          [bool]          允许位图缓存
HideMacDock:            [bool]          不以全屏模式显示Mac菜单栏和Dock

==========键盘==========
KeyMappingTable:        [dict]          键盘快捷键

==========声音==========
AudioRedirectionMode:   [integer]       通过Windows计算机播放声音  0: 仅在Macintosh计算机上  1:仅在Windows计算机上  2: 不播放声音

==========驱动器==========
DriveRedirectionMode:   [integer]       使以下Mac磁盘驱动器或文件夹在Windows计算机上可用  0: 无  1: 所有磁盘驱动器  2: 主文件夹  3: 文档文件夹  4: 其它文件夹
RedirectFolder:         [string]        文件夹

==========打印机==========
PrinterRedirection:     [bool]          打印机开关
RedirectPrinter:        [string]        使用连接到Mac的打印机

==========应用程序==========
RemoteApplication:      [bool]          登录到远程计算机后, 仅启动一下Windows应用程序
ApplicationPath:        [string]        应用程序路径和文件名
WorkingDirectory:       [string]        工作目录

==========安全性==========
AuthenticateLevel:      [integer]       远程计算机验证  0: 即使验证失败, 也始终连接  1: 验证失败时向我发出警告  2: 验证失败时不连接

=========OTHER=========
DontWarnOnChange:       [bool]          未知
"""

dict_desktopsize = """<dict>
    <key>DesktopHeight</key>
    <integer>{height}</integer>
    <key>DesktopWidth</key>
    <integer>{width}</integer>
</dict>
"""

fullscreen_desktopsize = """<string>DesktopFullScreen</string>
"""

rdc_cfg_tmpl = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AddToKeychain</key>
	<false/>
	<key>ApplicationPath</key>
	<string>{ApplicationPath}</string>
	<key>AudioRedirectionMode</key>
	<integer>2</integer>
	<key>AuthenticateLevel</key>
	<integer>1</integer>
	<key>AutoReconnect</key>
	<true/>
	<key>BitmapCaching</key>
	<true/>
	<key>ColorDepth</key>
	<integer>2</integer>
	<key>ConnectionString</key>
	<string>{ConnectionString}</string>
	<key>DesktopSize</key>
	{DesktopSize}
	<key>Display</key>
	<integer>0</integer>
	<key>Domain</key>
	<string>10.10.16.125</string>
	<key>DontWarnOnChange</key>
	<false/>
	<key>DontWarnOnDriveMount</key>
	<false/>
	<key>DontWarnOnQuit</key>
	<false/>
	<key>DriveRedirectionMode</key>
	<integer>{DriveRedirectionMode}</integer>
	<key>FontSmoothing</key>
	<true/>
	<key>FullWindowDrag</key>
	<true/>
	<key>HideMacDock</key>
	<false/>
	<key>KeyMappingTable</key>
	<dict>
		<key>UI_ALPHANUMERIC_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>102</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_ALT_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>4294967295</integer>
			<key>MacModifier</key>
			<integer>2048</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_CONTEXT_MENU_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>120</integer>
			<key>MacModifier</key>
			<integer>2048</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_CONVERSION_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>4294967295</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<false/>
		</dict>
		<key>UI_HALF_FULL_WIDTH_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>49</integer>
			<key>MacModifier</key>
			<integer>256</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_HIRAGANA_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>104</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_NON_CONVERSION_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>4294967295</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<false/>
		</dict>
		<key>UI_NUM_LOCK_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>71</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_PAUSE_BREAK_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>99</integer>
			<key>MacModifier</key>
			<integer>2048</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_PRINT_SCREEN_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>118</integer>
			<key>MacModifier</key>
			<integer>2048</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_SCROLL_LOCK_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>107</integer>
			<key>MacModifier</key>
			<integer>0</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_SECONDARY_MOUSE_BUTTON</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>256</integer>
			<key>MacModifier</key>
			<integer>4608</integer>
			<key>On</key>
			<true/>
		</dict>
		<key>UI_WINDOWS_START_KEY</key>
		<dict>
			<key>MacKeyCode</key>
			<integer>122</integer>
			<key>MacModifier</key>
			<integer>2048</integer>
			<key>On</key>
			<true/>
		</dict>
	</dict>
	<key>MenuAnimations</key>
	<true/>
	<key>PrinterRedirection</key>
	<false/>
	<key>RedirectFolder</key>
	<string>{RedirectFolder}</string>
	<key>RedirectPrinter</key>
	<string></string>
	<key>RemoteApplication</key>
	<true/>
	<key>Themes</key>
	<true/>
	<key>UserName</key>
	<string>administrator</string>
	<key>Wallpaper</key>
	<true/>
	<key>WorkingDirectory</key>
	<string>c:\</string>
</dict>
</plist>
"""
mstsc_cfg_tmpl = """compression:i:1
displayconnectionbar:i:1
disable wallpaper:i:1
disable full window drag:i:0
allow desktop composition:i:0
allow font smoothing:i:0
disable menu anims:i:0
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
redirectcomports:i:0
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
prompt for credentials:i:0
negotiate security layer:i:1
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:1
"""

terminal_expect = """#!/usr/bin/env expect -f
trap {{
    set rows [stty rows]
    set cols [stty columns]
    stty rows $rows columns $cols < $spawn_out(slave,name)
}} WINCH

set user "{user}"
set host "{host}"
set port "{port}"
set password "{password}"
exec tput reset >@ stdout
puts "connecting ..."
set timeout 20
log_user 0
set pid [spawn ssh $user\@$host -p $port]

expect {{
    "key fingerprint is" {{
        send "yes\\r"
        exp_continue
    }}
    "passphrase for key" {{
        send "\\r"
        exp_continue
    }}
    "Unable to negotiate with" {{
        puts "add 'HostkeyAlgorithms +ssh-dss' to ~/.ssh/config"
        exit 1
    }}
    -re {{[pP]assword:}} {{
        send -- "$password\\r"
        log_user 1
        exec tput reset >@ stdout
        interact
    }}
}}

log_user 1
exec tput reset >@ stdout
set status [split [wait $pid]]
set os_status [lindex $status 2]
set proc_status [lindex $status 3]
if {{$os_status == 0}} {{
    if {{$proc_status != 0}} {{
        puts "Could not connect to '$host' (port $port)"
    }}
}} else {{
    puts "ssh error"
}}
"""