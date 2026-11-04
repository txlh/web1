# Campus Plant Corner · 校园绿植小店

一个静态落地页，设计语言参考 [vestris.ai](https://vestris.ai)：奶油纸底、编辑感衬线标题、
水彩笔触（用 Canvas 有序抖动 Bayer 算法做出颗粒状的边缘）、编号细线分割、一段深绿反色区块。

## 打开方式

直接双击 `index.html` 即可（纯静态，无构建、无依赖、无联网字体）。
如果想让字体和图片缓存更正常，也可以在本目录起一个静态服务：

```powershell
python -m http.server 8080
# 然后访问 http://localhost:8080
```

## 目录

```
index.html                 页面结构（单页，含 8 个区块）+ 背景音乐开关
assets/css/styles.css      全部样式：色板变量、排版、版式、响应式、动效
assets/js/app.js           交互：吸顶导航、移动菜单、滚动进场、数字滚动、
                           跑马灯、hero 视差、Canvas 抖动画笔、背景音乐
assets/img/                从原始幻灯片裁切出的图片 + SVG logo
assets/audio/sunset.mp3    背景音乐（原文件 103 MB，见下方说明）
tools/crop_assets.py       图片裁切的脚本（坐标按幻灯片比例，可复现）
```

## 背景音乐

页面加载后会尝试自动播放 `assets/audio/sunset.mp3`，右下角有一个圆形开关
（播放时是跳动的音量条，悬停展开「背景音乐 Music」）。

- **浏览器会拦截有声自动播放**：Chrome / Edge / Safari 都要求用户先有交互，
  所以代码先尝试 `play()`，被拒后监听第一次点击、按键、滚动或触屏，那一刻开始播放；
  右下角的按钮会轻微呼吸三次提示可以点。
- 首次播放音量从 0 淡入到 0.32，避免突然出声；关闭时会淡出再暂停。
- 开关状态记在 `localStorage` 的 `cpc:music`：手动关掉后，下次进入不会自动播放。
- 想换音乐：替换 `assets/audio/sunset.mp3` 即可（保持文件名），或改 `index.html` 里
  `<audio id="bgm" src="...">` 的路径。

> **文件体积**：原始 mp3 有 103 MB，浏览器打开页面时会按需流式读取——从本地磁盘打开
> 没有感觉，但放到服务器上会让首屏和缓存变重。如果要上线，建议压成 96–128 kbps 的版本
> （约 5–15 MB），或截取 2–3 分钟做循环。仓库里没有音频转码工具，所以保留了原文件。

## 内容（中英双文）

页面采用「中文为主、英文为辅」的双语排版：所有段落成对出现（中文正文 + 英文衬线小字），
标签、按钮、导航、元信息里的英文以斜体小字内联。

| 要求 | 落点 |
| --- | --- |
| 公司名称 | 导航、Hero、页脚：Campus Plant Corner · 校园绿植小店 |
| Logo | 按幻灯片 2 重绘的 ∞＋「＋/－」SVG（导航 38px 到大尺寸都清晰，另附 [logo.svg](assets/img/logo.svg) 作 favicon） |
| 简介 | 01 About Us：「我们卖小盆栽／我们帮学生养植物」＋出摊照片与数据条 |
| 产品 | 02 Our Products：多肉 / 绿萝 / 花盆，各带价格、说明、悬浮放大 |
| 公司架构 | 06 Our Team：店长 → 销售组 ／ 养护组 的组织架构图，蓝／绿／赭三个岗位色块沿用幻灯片 5 |

## 修改指引

- **文案**：直接改 `index.html`。统计数字在 `data-count` 属性里（如 `data-count="1240"`）。
- **配色**：`styles.css` 顶部 `:root` 里的 `--paper / --ink / --jade / --ochre / --blue`。
- **Logo**：三处内联 SVG（导航、Logo 区块、页脚），改 `stroke-width` 附近即可；
  `assets/img/logo.svg` 是 favicon 版本。
- **图片**：替换 `assets/img/` 下同名文件即可（保持 4:5 或 3:2 比例最稳）。
- **联系方式**：搜索 `hello@campusplantcorner.cn`。

## 备注

- 页面里的价格、统计数字、"已提醒 32 位同学"等均为示例文案，请按实际情况替换。
- 无外部字体依赖：中文用 Noto Serif SC / Noto Sans SC，拉丁文用 Sitka Display，均为系统字体，
  缺失时自动回落到 Georgia / 系统无衬线。
- 已做响应式：1080px 以下改单列，900px 以下切换汉堡菜单，760px 以下卡片单列。
- 尊重 `prefers-reduced-motion`：开启后关闭进场动画与跑马灯。

## 配套 PPT

`Campus_Plant_Corner_校园绿植小店_新版.pptx`（7 页，16:9，中英双文），沿用网页的视觉系统：

| 页 | 内容 |
| --- | --- |
| 1 | 封面：主标语、拱形照片、时间与联系方式 |
| 2 | 关于我们：两条编号介绍 + 现场照片 |
| 3 | 我们的产品：三张产品图卡（价格、中英名、说明） |
| 4 | 怎么买：2×2 步骤网格 |
| 5 | 我们的 Logo：矢量无限符号 + 两条释义 |
| 6 | 我们的团队：店长 → 销售组 / 养护组的架构图 |
| 7 | 想说的话 / 谢谢你：森林照片上的深色收尾页 |

Logo 是 PowerPoint 原生矢量（自定义路径），不是图片，可以直接改颜色和描边；
照片用形状填充（拱形、圆角矩形）实现网页里的裁切效果。
重新生成：`python tools/build_deck.py`（需要 `tools/deck_lib.py` 与 `assets/img/`）。
