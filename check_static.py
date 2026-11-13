#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-frontend-resume-upload 静态检查脚本（仅标准库，无第三方依赖）。

校验目标（不做运行时 DOM 执行，只做关键元素/规则/事件绑定的存在性检查）：
  1. index.html：语义结构、隐藏 file input + 关联 label、两按钮、三步进度线、
     aria-live 状态区、插画 SVG 等关键元素存在。
  2. styles.css：桌面左右两列 flex、≤768px 上下布局、按钮 hover/active/focus、
     虚线上传区、拖拽高亮等关键规则存在。
  3. app.js：click / change / drop / dragover 等关键事件绑定存在。

退出码：全部通过返回 0，任一失败返回 1。
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read(name):
    return (BASE / name).read_text(encoding="utf-8")


def has(text, needle, label):
    if needle not in text:
        print(f"  [FAIL] 缺少：{label}  (未找到 {needle!r})")
        return False
    print(f"  [ok]   {label}")
    return True


def has_regex(text, pattern, label):
    if not re.search(pattern, text):
        print(f"  [FAIL] 缺少：{label}  (未匹配 {pattern!r})")
        return False
    print(f"  [ok]   {label}")
    return True


def main():
    results = []

    print("== 1. index.html 结构 ==")
    html = read("index.html")
    results += [
        has(html, '<html lang="en">', "html lang"),
        has(html, '<link rel="stylesheet" href="styles.css"', "引入 styles.css"),
        has(html, '<script src="app.js"></script>', "引入 app.js"),
        has(html, 'Upload Your Resume', "左列标题「Upload Your Resume」"),
        has(html, 'Finish!', "左列标题「Finish!」"),
        has(html, 'hero-illustration', "原创插画 SVG 容器"),
        has(html, '<svg', "插画使用内联 SVG"),
        has(html, 'Upload file', "卡片标题「Upload file」"),
        has(html, 'class="upload-area"', "上传区容器"),
        has(html, '<input type="file"', "隐藏 file input"),
        has(html, 'for="file-input"', "label 关联 file input"),
        has(html, 'class="sr-only"', "file input 视觉隐藏(sr-only)"),
        has(html, 'accept=".pdf,.doc,.docx', "accept 限定文件类型"),
        has(html, 'aria-live="polite"', "状态区 aria-live"),
        has(html, 'role="status"', "状态区 role=status"),
        has(html, 'id="btn-back"', "按钮「Last step」"),
        has(html, '>Last step<', "按钮文案「Last step」"),
        has(html, 'id="btn-finish"', "按钮「Finish」"),
        has(html, '>Finish<', "按钮文案「Finish」"),
        has(html, 'class="steps"', "三步进度线容器"),
        has(html, 'step-current', "进度线含当前步骤"),
        has(html, 'aria-label="Upload progress: step 3 of 3"', "进度线无障碍标注"),
    ]

    print("== 2. styles.css 关键规则 ==")
    css = read("styles.css")
    results += [
        has_regex(css, r"\.page\s*\{[^}]*display\s*:\s*flex", "桌面 flex 两列布局"),
        has_regex(css, r"@media\s*\(max-width:\s*768px\)", "≤768px 响应式断点"),
        has_regex(css, r"@media\s*\(max-width:\s*768px\)[^@]*flex-direction\s*:\s*column",
                  "断点内上下布局(flex-direction:column)"),
        has_regex(css, r"\.upload-area[^{]*\{[^}]*border\s*:\s*2px\s+dashed", "虚线浅蓝上传区"),
        has_regex(css, r"\.upload-area:hover", "上传区 hover 态"),
        has_regex(css, r"\.upload-area:focus-within", "上传区键盘 focus 态"),
        has_regex(css, r"\.is-dragging", "拖拽高亮态"),
        has_regex(css, r"\.btn-primary:hover", "Finish 按钮 hover"),
        has_regex(css, r"\.btn-primary:active", "Finish 按钮 active"),
        has_regex(css, r"\.btn-secondary:hover", "Last step 按钮 hover"),
        has_regex(css, r"\.btn-secondary:active", "Last step 按钮 active"),
        has_regex(css, r"\.btn:focus-visible", "按钮 focus-visible"),
        has_regex(css, r"box-shadow", "卡片阴影"),
        has_regex(css, r"border-radius", "卡片圆角"),
    ]

    print("== 3. app.js 关键事件绑定 ==")
    js = read("app.js")
    results += [
        has(js, 'getElementById("file-input")', "获取 file input"),
        has(js, 'getElementById("btn-finish")', "获取 Finish 按钮"),
        has(js, 'getElementById("btn-back")', "获取 Last step 按钮"),
        has(js, 'addEventListener("change"', "文件 change 事件"),
        has(js, 'addEventListener("click"', "按钮 click 事件"),
        has(js, 'addEventListener("drop"', "拖拽 drop 事件"),
        has(js, '"dragover"', "拖拽 dragover 事件名已注册"),
        has(js, '"dragenter"', "拖拽 dragenter 事件名已注册"),
        has(js, "e.dataTransfer", "拖拽读取 dataTransfer"),
        has(js, "fileName.textContent", "文件名以 textContent 写入(防 XSS)"),
        has(js, "Please choose a file", "未选文件提示文案"),
        has(js, "ALLOWED_EXTENSIONS", "校验 PDF/DOC/DOCX 扩展名"),
        has(js, "MAX_FILE_SIZE", "校验 5 MB 文件大小"),
        has(js, "File is larger than the 5 MB limit", "超限文件提示文案"),
    ]

    failed = [r for r in results if not r]
    total = len(results)
    passed = total - len(failed)

    print()
    print(f"== 结果：{passed}/{total} 项通过 ==")
    if failed:
        print(f"FAILED：{len(failed)} 项缺失。")
        sys.exit(1)
    print("ALL PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
