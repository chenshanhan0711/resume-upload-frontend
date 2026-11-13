# 01 · Figma 简历上传页面

方向一前端：参照浏览器可见 Figma 设计稿实现的简历上传页（HTML / CSS / 原生 JS，无构建步骤）。

## 运行

```bash
# 方式一：直接双击 index.html
# 方式二：本地静态服务器
python -m http.server 8000
# 浏览器打开 http://127.0.0.1:8000/
```

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 语义化结构 + 内联 SVG 插画 |
| `styles.css` | 两列布局、上传卡、三步进度线、响应式 |
| `app.js` | 交互逻辑（原生 JS） |
| `check_static.py` | 静态检查（仅标准库，50 项断言） |

## 功能

- 桌面左右两列：左「Finish! / Upload Your Resume」+ 灰色说明 + 蓝灰插画；
  右白圆角阴影「Upload file」上传卡。
- 浅蓝虚线上传区：点击 / 键盘 Enter 打开文件选择框；支持拖拽文件（dragover / drop）。
- 选中后显示文件名（`textContent` 写入，防 XSS），并校验 PDF/DOC/DOCX 与 5 MB
  上限；未选点 Finish 给 aria-live 可访问提示。
- 按钮 hover / active / focus-visible 态；Last step 重置，Finish 校验。
- 底部三步进度线。
- ≤ 768px 响应式改为上下结构。

## 静态检查

```bash
python check_static.py
# 实测 50/50 通过（ALL PASS）
```

另用真实浏览器验证了桌面/移动端布局、未选文件提示，以及不受支持文件类型的拒绝逻辑。

## 诚实声明（限制）

- Figma API 无法读取，仅依据浏览器可见稿实现，**非像素级还原**。
- 题面明确要求提交 GitHub Link；本目录即为可直接上传的仓库内容，链接需在上传后填写到邮件中。
- 候选人信息和简历只放在邮件附件目录中，不写入公开仓库，以免公开手机号和邮箱。
