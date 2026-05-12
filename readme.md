# 布布一二桌面宠物 | Bubu Yier Desktop Pet
✨ 免费开源、轻量级、跨平台的桌面宠物软件 ✨

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 项目介绍
布布一二桌面宠物是一款基于Python开发的免费开源桌面宠物软件，内置**布布、一二、布布&一二**三款可爱皮肤，支持动画播放、自动互动、自定义调节等丰富功能，无广告、无捆绑，完全免费供个人使用。

软件自带开发者版权标识，支持免费分享传播，旨在为用户带来轻松有趣的桌面体验。

## 核心功能
- 🎨 **多皮肤切换**：支持布布、一二、布布&一二 三款皮肤自由切换
- 🎭 **丰富状态**：静止（喜悦/平静/悲伤/生气）、走路、睡觉动画
- 🤖 **自动模式**：智能随机切换状态，自动走路互动
- 🎵 **音量调节**：自定义宠物音效音量，支持一键静音
- 📏 **大小调节**：自由调整宠物尺寸（60px-200px）
- 😴 **睡眠/叫醒**：一键让宠物睡觉/叫醒，睡眠模式自动静音
- 🖱️ **拖拽移动**：鼠标拖拽宠物到任意位置
- ℹ️ **作者信息**：内置开发者信息弹窗
- 🔒 **无广告捆绑**：纯绿色软件，免费使用

## 运行环境
- Python 3.8 及以上版本
- 依赖库：tkinter, Pillow, pygame

## 打包教程(一)
- 生成独立 exe 可执行文件：
- (在项目地址打开命令提示符)
### 1. Windows
```
pyinstaller -w -F --noconsole --add-data "pet_res;pet_res" --add-data "icon.png;." --icon=icon.ico bubuyier.py
```
### 2. macOS
```
pyinstaller -w -F --add-data "pet_res:pet_res" --add-data "icon.png:." --icon=icon.icns bubuyier.py
```
### 3. Linux
```
pyinstaller -w -F --add-data "pet_res:pet_res" --add-data "icon.png:." bubuyier.py
```

## 打包教程(二)
- 生成 exe 可执行文件，exe不内置表情包文件资源，可自行更换表情包，需保证文件路径正确（不变）：
- (在项目地址打开命令提示符)
### 1. Windows
```
pyinstaller -w -F --noconsole --add-data "icon.png;." --icon=icon.ico bubuyier.py
```
### 2. macOS
```
pyinstaller -w -F --add-data "icon.png:." --icon=icon.icns bubuyier.py
```
### 3. Linux
```
pyinstaller -w -F --add-data "icon.png:." bubuyier.py
```
## 操作说明
- 左键拖拽：移动宠物位置
- 右键单击：打开功能菜单
- 调节窗口：点击空白处自动关闭调节面板
### 跨平台说明
- ✅ Windows：完整支持所有功能（鼠标穿透、透明、无边框）
- ✅ macOS：支持核心功能（动画、拖拽、调节、皮肤切换）
- ✅ Linux：支持基础功能（适配主流桌面环境）
- 注：Windows 打包的 .exe 仅支持 Windows 系统，macOS/Linux 需运行源码或对应系统打包文件。
## 开源协议
- 本项目基于 MIT License 开源，允许免费使用、分享、二次开发，但需遵守以下规则：
- 保留原作者版权信息与标识，可自行添加新增作者信息
- 禁止用于商业用途、盈利行为
- 禁止篡改、移除软件内的开发者信息

## 版权声明
- 桌宠软件：布布一二桌宠
- 开发者（抖音昵称）：布布一二特效大王
- 抖音ID：38739236249
- 版权所有 © 2026 @Duang，保留所有权利
- 许可协议：非商业使用免费，转载/分发需保留完整版权信息
- 禁止未经授权的商业用途

## 支持项目
- 如果喜欢这个项目，欢迎 Star ⭐ 支持，也可以分享给更多朋友使用！




# Bubu Yier Desktop Pet
✨ Free Open-Source, Lightweight & Cross-Platform Desktop Pet Software ✨
## Project Introduction
Bubu Yier Desktop Pet is a free and open-source desktop pet software developed with Python. It has three built-in skins: **Bubu, Yier, Bubu & Yier**, supporting animation playback, automatic interaction, custom adjustment and many other features. Completely ad-free and no bundled software, free for personal use.
The software comes with built-in developer copyright marks and allows free sharing and distribution, aiming to bring users a relaxing and fun desktop experience.
## Core Features
- 🎨 Multiple Skin Switching: Freely switch among three skins: Bubu, Yier, Bubu & Yier
- 🎭 Rich Status Animations: Idle (Joyful/Calm/Sad/Angry), walking and sleeping animations
- 🤖 Auto Mode: Intelligently switch statuses randomly and walk around automatically
- 🎵 Volume Control: Customize pet sound effect volume, support one-click mute
- 📏 Size Adjustment: Freely resize the pet (60px-200px)
- 😴 Sleep/Wake Up: One-click to put the pet to sleep or wake it up; auto mute in sleep mode
- 🖱️ Drag & Move: Drag the pet to any position with the mouse; auto hide at screen edges
- ℹ️ Author Info: Built-in developer information popup window
- 🔒 No Ads & Bundles: Pure green software for free use
## System Requirements
- Python 3.8 or higher
- Dependencies: tkinter, Pillow, pygame
## Packaging Guide 1
- Generate standalone executable exe file:
- (Open Command Prompt in the project root directory)
### 1. Windows
```
pyinstaller -w -F --noconsole --add-data "pet_res;pet_res" --add-data "icon.png;." --icon=icon.ico bubuyier.py
```
### 2. macOS
```
pyinstaller -w -F --add-data "pet_res:pet_res" --add-data "icon.png:." --icon=icon.icns bubuyier.py
```
### 3. Linux
```
pyinstaller -w -F --add-data "pet_res:pet_res" --add-data "icon.png:." bubuyier.py
```
## Packaging Guide 2
- Generate exe file without embedding emoji resource files; you can replace emoji packs freely while keeping the original file path unchanged:
- (Open Command Prompt in the project root directory)
### 1. Windows
```
pyinstaller -w -F --noconsole --add-data "icon.png;." --icon=icon.ico bubuyier.py
```
### 2. macOS
```
pyinstaller -w -F --add-data "icon.png:." --icon=icon.icns bubuyier.py
```
### 3. Linux
```
pyinstaller -w -F --add-data "icon.png:." bubuyier.py
```
## Operation Instructions
- Left-click drag: Move the pet
- Right-click: Open function menu
- Adjustment Panel: Click blank area to close the panel automatically
## Cross-platform Compatibility
- ✅ Windows: Full support for all features (mouse penetration, transparency, borderless window)
- ✅ macOS: Support core features (animation, drag, adjustment, skin switching)
- ✅ Linux: Support basic features (compatible with mainstream desktop environments)
- Note: The Windows .exe file only works on Windows. Run the source code or system-specific packaged files for macOS/Linux.
## Open Source License
- This project is open-sourced under the MIT License. Free use, sharing and secondary development are permitted with the following rules:
- Keep the original author copyright information and marks; you may add your own contributor information
- Prohibit commercial use and profit-making activities
- Forbid tampering with or removing built-in developer information
## Copyright Statement
- Desktop Pet Name: Bubu Yier Desktop Pet
- Developer (Douyin Nickname): Bubu Yier Special Effects Master
- Douyin ID: 38739236249
- Copyright © 2026 @Duang. All Rights Reserved.
- License: Free for non-commercial use; retain complete copyright information for reproduction and distribution
- Unauthorized commercial use is strictly prohibited
## Support This Project
- If you like this project, please give it a Star ⭐ and share it with more friends!
