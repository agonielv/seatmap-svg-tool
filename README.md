# Seatmap SVG Tool

Seatmap SVG Tool 是一个用 Python 3.11+ 开发的“Excel 表格座位图自动生成 SVG 矢量座位图”工具。它可以读取剧院座位 Excel，按指定 sheet 和扫描范围识别普通座位、加座、不可用座位、区域标签、舞台/说明文字，并输出可在浏览器和矢量编辑软件中打开的 SVG，以及 JSON 统计报告。

## 功能

- 读取 `.xlsx`，无需安装 Microsoft Office。
- 支持中文文件名、中文 sheet 名和中文标签。
- 支持命令行参数和 YAML 配置文件。
- 保留 Excel 行列空间关系，不压缩座位矩阵。
- 输出 SVG：每个座位包含 `data-cell`、`data-seat`、`data-status`、`data-row-label`。
- 输出 `report.json`：包含座位统计、忽略单元格、无法识别内容、填充色统计、合并单元格列表。
- 提供 Windows 双击运行脚本、PyInstaller 打包脚本和 GitHub Actions Windows 构建工作流。

## 快速开始

### 1. 安装依赖

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. 运行示例

```bash
python seatmap_svg.py --input samples/歌剧院座位图—加座版.xlsx --sheet 净版 --range A1:AX103 --output output/seatmap.svg --report output/report.json
```

或使用配置文件：

```bash
python seatmap_svg.py --config configs/default.yaml
```

生成文件：

- `output/seatmap.svg`
- `output/report.json`

## Windows 用户如何直接运行

双击：

```text
scripts\run_sample.bat
```

脚本会：

1. 进入项目根目录。
2. 创建 `.venv` 虚拟环境（如果不存在）。
3. 安装 `requirements.txt`。
4. 运行 `configs/default.yaml` 示例配置。
5. 生成 `output\seatmap.svg` 和 `output\report.json`。

## 命令行参数

```bash
python seatmap_svg.py \
  --input samples/歌剧院座位图—加座版.xlsx \
  --sheet 净版 \
  --range A1:AX103 \
  --output output/seatmap.svg \
  --report output/report.json
```

参数说明：

- `--config`：YAML 配置文件路径。
- `--input`：Excel 文件路径。
- `--sheet`：工作表名称；省略时使用配置或默认值。
- `--range`：扫描范围，例如 `A1:AX103`。
- `--output`：SVG 输出路径。
- `--report`：JSON 报告输出路径。

命令行参数会覆盖配置文件中的同名设置。

## 配置文件

默认配置位于 `configs/default.yaml`。常用配置如下：

```yaml
input:
  file: samples/歌剧院座位图—加座版.xlsx
  sheet: 净版
  range: A1:AX103
output:
  svg: output/seatmap.svg
  report: output/report.json
seat:
  regex: "^\\d+(?:\\+\\d+)?$"
  width: 28
  height: 20
  radius: 4
layout:
  origin_x: 40
  origin_y: 40
  cell_width: 32
  cell_height: 24
ignore:
  ranges:
    - BB1:BF103
```

### 调整座位大小和间距

修改：

- `seat.width` / `seat.height`：座位矩形大小。
- `layout.cell_width` / `layout.cell_height`：Excel 单元格映射到 SVG 的格距。
- `layout.origin_x` / `layout.origin_y`：整体边距。

### 排除右侧统计区

在 `ignore.ranges` 添加 Excel 范围：

```yaml
ignore:
  ranges:
    - BB1:BF103
    - A105:AX120
```

### 颜色识别

程序会在报告的 `fill_color_counts` 中输出填充色键，例如：

- `none`
- `rgb:FF0000`
- `theme:0`
- `indexed:64`

如果某种颜色表示不可用座位，可复制颜色键到：

```yaml
rules:
  disabled_seat:
    by_fill_keys:
      - "theme:0"
      - "rgb:4B4B4B"
```

## Windows 打包 exe

双击或在命令行运行：

```bat
scripts\build_windows.bat
```

脚本会：

1. 创建虚拟环境。
2. 安装依赖。
3. 运行测试。
4. 使用 PyInstaller 打包。
5. 输出 `dist\SeatmapSVGTool.exe`。
6. 输出 `release\SeatmapSVGTool-windows-x64.zip`。

如果当前非 Windows 环境无法直接生成 Windows exe，可把代码推送到 GitHub，使用 `.github/workflows/build-windows.yml` 在 `windows-latest` 上自动构建并上传 artifact。

## GitHub Actions

工作流文件：`.github/workflows/build-windows.yml`。

触发方式：

- `push`
- `pull_request`
- 手动 `workflow_dispatch`

产物：`SeatmapSVGTool-windows-x64.zip`。

## 常见问题

### 中文乱码怎么办？

SVG 使用 UTF-8 写入，并在 CSS 中优先使用 `Microsoft YaHei`、`SimHei`。如果浏览器显示异常，请确认 SVG 文件以 UTF-8 保存，并在系统中安装常见中文字体。

### Excel 颜色识别不准怎么办？

Excel 颜色可能是 RGB、主题色或索引色。请先查看 `output/report.json` 中的 `fill_color_counts`，再把对应键加入 YAML 规则。主题色不会强行转换成 RGB，以避免不同工作簿主题导致误判。

### 统计数量和人工统计不一致怎么办？

先检查：

1. `input.range` 是否覆盖了所有座位。
2. `ignore.ranges` 是否误排除了座位区域。
3. `seat.regex` 是否匹配你的座位号格式。
4. `rules.disabled_seat.by_fill_keys` 是否配置了正确颜色。
5. `unrecognized_non_empty_cells` 中是否有本应识别为座位的内容。

### 如何排除右侧统计区？

在 `configs/default.yaml` 的 `ignore.ranges` 中添加统计区范围，例如 `BB1:BF103`。

### 如何调整座位大小和间距？

调整 `seat.width`、`seat.height`、`layout.cell_width`、`layout.cell_height`。座位矩形会在对应 Excel 单元格映射区域内居中。

## 已知限制

- 第一版以 Excel 单元格网格为布局基础，不会自动拟合已有原始 SVG 底图。
- 主题色只输出 `theme:N` 调试键，不自动按工作簿主题转换为 RGB。
- 统计表自动比对只输出程序统计和可疑文本，不保证理解所有人工统计表格式。

## 下一步：支持原始 SVG 底图 + Excel 座位图叠加

后续可增加：

1. `background_svg` 配置项，把原始 SVG 作为底图引入。
2. SVG 坐标校准参数，如缩放、旋转、偏移。
3. 选择 Excel 中若干锚点座位和底图锚点进行仿射变换。
4. 输出分层 SVG：`background`、`seats`、`labels` 分组，方便编辑。
