请帮我开发一个“Excel 表格座位图自动生成 SVG 矢量座位图”的 Windows 桌面/命令行工具。

一、背景

我的工作中经常会拿到剧院座位图材料，常见输入包括：

1. Excel 表格形式的座位图，单元格里有座位号、加座、区域名、排号、舞台、统计信息等。
2. 有时也会拿到剧院原始 SVG 矢量图，但它主要作为视觉参考或底图，不一定和 Excel 完全同源。
3. 最终需要输出 SVG 格式的矢量座位图，方便后续编辑、展示、交付或接入前端系统。

我会提供两个示例文件：

歌剧院座位图—加座版.xlsx
矢量图.svg

注意：这两个示例文件不是同一个剧院，不要求强行对齐。Excel 用来说明输入座位表格式，SVG 用来说明最终矢量图大致风格和结构。

二、目标

请开发一个工具，可以根据 Excel 表格座位图自动生成 SVG 矢量座位图。

第一版优先实现：

1. 读取 Excel 文件。
2. 选择 sheet。
3. 选择扫描范围，例如 A1:AX103。
4. 识别座位单元格。
5. 根据单元格内容、颜色、合并单元格信息生成 SVG。
6. 输出 .svg 文件。
7. 输出座位统计报告，例如原座位、加座、不可用座位、总座位数。
8. 支持 Windows 系统直接使用。

三、技术栈要求

优先使用 Python 3.11+ 开发。

推荐依赖：

* openpyxl：读取 Excel。
* PyYAML：读取配置文件。
* svgwrite 或直接使用 xml.etree.ElementTree 生成 SVG。
* Pillow 或 cairosvg 可选，用于生成预览图，不是必须。
* PyInstaller：用于 Windows 打包 exe。

不要依赖商业软件，不要要求用户安装 Office。

四、工具形态

请同时提供两种使用方式：

1. 命令行方式

示例：

python seatmap_svg.py --input samples/歌剧院座位图—加座版.xlsx --sheet 净版 --range A1:AX103 --output output/seatmap.svg

或者：

python seatmap_svg.py --config configs/default.yaml

2. Windows 直接使用方式

请提供 Windows 可用的交付方式：

* build_windows.bat
* requirements.txt
* README.md
* 打包配置
* PyInstaller 打包命令
* 生成 dist/SeatmapSVGTool.exe
* 生成 release/SeatmapSVGTool-windows-x64.zip

如果无法在当前环境直接生成 exe，也必须提供完整的 Windows 打包脚本和 GitHub Actions workflow，要求 workflow 使用 windows-latest 构建 exe 并上传 artifact。

五、配置文件设计

请设计 YAML 配置文件，例如：

app:
name: SeatmapSVGTool

input:
file: samples/歌剧院座位图—加座版.xlsx
sheet: 净版
range: A1:AX103

output:
svg: output/seatmap.svg
report: output/report.json
preview_png: output/preview.png

seat:
regex: "^\d+(?:\+\d+)?$"
width: 28
height: 20
gap_x: 4
gap_y: 4
radius: 4
font_size: 9

layout:
origin_x: 40
origin_y: 40
cell_width: 32
cell_height: 24

style:
normal_fill: "#f04b5f"
added_fill: "#f28c28"
disabled_fill: "#4b4b4b"
label_fill: "#d9d9d9"
stage_fill: "#6fa8dc"
stroke: "#333333"
text_fill: "#111111"

rules:
added_seat:
by_text_regex: "^\d+\+\d+$"
disabled_seat:
by_fill_keys:
- "theme:0"
normal_seat:
by_default: true

ignore:
ranges:
- BB1:BF103

六、座位识别规则

默认规则：

1. 单元格内容匹配数字，例如 1、2、23、158，识别为普通座位。
2. 单元格内容匹配 23+1、8+1 这类格式，识别为加座。
3. 单元格有特殊填充色时，可按颜色识别为普通座位、加座或不可用座位。
4. 合并单元格如果不是座位，应该作为区域标签、楼层标签、舞台标签或说明文本处理。
5. 空白单元格不生成座位。
6. 表格右侧的统计区、说明区应该可以通过 ignore.ranges 排除。
7. 程序必须保留 Excel 的行列空间关系，不能把座位压缩成连续矩阵。

七、SVG 输出要求

输出 SVG 必须是标准矢量图。

每个座位建议生成如下结构：

<g class="seat seat-normal" data-cell="D6" data-row-label="1排" data-seat="41" data-status="normal">
  <rect x="..." y="..." width="..." height="..." rx="..." />
  <text x="..." y="...">41</text>
</g>

要求：

1. 每个座位有 data-cell，记录 Excel 坐标。
2. 每个座位有 data-seat，记录座位号。
3. 每个座位有 data-status，例如 normal、added、disabled。
4. SVG 中要包含 CSS 样式。
5. 座位号文字居中。
6. 支持中文区域名。
7. 支持合并单元格作为大标签。
8. 支持舞台、包厢、楼层等文本块。
9. 输出 SVG 尺寸根据 Excel 范围自动计算。

八、统计报告要求

生成 JSON 或 TXT 报告，包含：

1. 扫描的文件、sheet、range。
2. 识别到的座位总数。
3. 普通座位数量。
4. 加座数量。
5. 不可用座位数量。
6. 被忽略的单元格数量。
7. 无法识别但有内容的单元格列表。
8. 每种 Excel 填充色对应的单元格数量。
9. 如果 Excel 中存在统计表，尽量读取并和程序识别结果比对；如果无法自动比对，也要在报告里输出程序统计结果。

九、项目结构要求

请按下面结构组织项目：

seatmap-svg-tool/
README.md
requirements.txt
seatmap_svg.py
seatmap_svg/
**init**.py
config.py
excel_reader.py
parser.py
svg_writer.py
report.py
cli.py
configs/
default.yaml
samples/
歌剧院座位图—加座版.xlsx
矢量图.svg
output/
.gitkeep
scripts/
build_windows.bat
run_sample.bat
.github/
workflows/
build-windows.yml
tests/
test_parser.py
test_svg_writer.py

十、Windows 封装要求

请确保工具可以在 Windows 系统直接使用。

必须提供：

1. scripts/run_sample.bat

双击后可以用 samples/歌剧院座位图—加座版.xlsx 生成 output/seatmap.svg 和 output/report.json。

2. scripts/build_windows.bat

双击后执行：

* 创建虚拟环境。
* 安装依赖。
* 使用 PyInstaller 打包。
* 输出 dist/SeatmapSVGTool.exe。
* 生成 release/SeatmapSVGTool-windows-x64.zip。

3. .github/workflows/build-windows.yml

要求：

* 使用 windows-latest。
* 安装 Python。
* 安装依赖。
* 运行测试。
* 使用 PyInstaller 打包 exe。
* 上传 exe 或 zip artifact。

十一、README 要求

README.md 必须写清楚：

1. 工具用途。
2. Windows 用户如何直接运行。
3. 如何修改配置文件。
4. 如何指定 Excel、sheet、range、output。
5. 如何打包 exe。
6. 常见问题：

   * 中文乱码怎么办。
   * Excel 颜色识别不准怎么办。
   * 统计数量和人工统计不一致怎么办。
   * 如何排除右侧统计区。
   * 如何调整座位大小和间距。
7. 示例命令。

十二、验收标准

请完成后确保：

1. 可以读取 samples/歌剧院座位图—加座版.xlsx。
2. 可以生成 output/seatmap.svg。
3. SVG 用浏览器可以直接打开。
4. SVG 中能看到座位、区域标签、舞台/说明文字。
5. report.json 中能看到座位统计。
6. Windows 下运行 scripts/run_sample.bat 能成功生成结果。
7. Windows 下运行 scripts/build_windows.bat 能成功打包 exe。
8. GitHub Actions 的 build-windows.yml 可以在 windows-latest 上构建 exe。
9. 代码中有清晰注释。
10. 不要只给代码片段，要提交完整可运行项目。

十三、开发注意事项

1. 不要假设所有剧院 Excel 格式都一样，所以解析规则要尽量配置化。
2. 不要把示例 Excel 的坐标逻辑写死到代码里。
3. 对颜色识别要输出调试信息，因为 Excel 的主题色、RGB 色、索引色可能不同。
4. 如果遇到无法识别的单元格，不要报错退出，应该写入 report。
5. SVG 坐标要基于 Excel 行列换算，保留表格布局。
6. 代码要兼容中文文件名、中文 sheet 名、中文输出内容。
7. 如果无法在当前运行环境生成 Windows exe，请说明原因，并确保 Windows 打包脚本和 GitHub Actions 已经完整实现。

十四、最终交付物

请交付完整项目，并在最后说明：

1. 修改了哪些文件。
2. 如何运行示例。
3. 如何打包 Windows exe。
4. 示例输出文件在哪里。
5. 有哪些已知限制。
6. 下一步如何支持“原始 SVG 底图 + Excel 座位图叠加”。
