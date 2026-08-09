"""build_figures_v2.py
重制 lzcapp 方案 5 张图(site-overview/key-areas/land-use-structure/mobility-bluegreen/metrics-evidence),
按 14 条图面规范化指南(typesetting_review.md)+ CJJ/T 97-2003 + GB 50137-2011 标准集成。
"""
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.font_manager import findfont, FontProperties
import numpy as np

REPO = os.getcwd()
FIG_DIR = os.path.join(REPO, "submissions", "lzcapp", "jingzhang-ai-belt", "assets", "figures")

PAL = {
    "residential": "#FAEEDA",
    "commercial": "#F5C4B3",
    "education": "#E6F1FB",
    "research": "#EEEDFE",
    "culture": "#FBEAF0",
    "park": "#9FE1CB",
    "greenway": "#C0DD97",
    "water": "#85B7EB",
    "mixed": "#F1EFE8",
    "industry": "#F0997B",
    "primary_road": "#5F5E5A",
    "secondary_road": "#B4B2A9",
    "branch_road": "#D3D1C7",
    "station": "#791F1F",
    "transit": "#791F1F",
    "provisional": "#791F1F",
    "key_area": "#F0997B",
    "key_building": "#A32D2D",
    "tier0_text": "#2C2C2A",
    "tier1_text": "#5F5E5A",
    "tier2_text": "#791F1F",
    "fig_block_bg": "#FFFFFF",
    "fig_block_border": "#5F5E5A",
    "fig_block_divider": "#B4B2A9",
    "tier0": "#2C2C2A",
    "tier1": "#185FA5",
    "fig_block_text": "#0C447C",
}

FONT_CANDIDATES = [
    "Microsoft YaHei",
    "PingFang SC",
    "Noto Sans CJK SC",
    "Source Han Sans CN",
    "SimHei",
    "WenQuanYi Zen Hei",
    "DejaVu Sans",
]


def pick_font():
    for name in FONT_CANDIDATES:
        try:
            fp = findfont(FontProperties(family=name), fallback_to_default=False)
            if fp and "DejaVu" not in fp and os.path.exists(fp):
                return name
        except Exception:
            pass
    return "DejaVu Sans"


FONT_NAME = pick_font()
plt.rcParams["font.family"] = FONT_NAME
plt.rcParams["font.sans-serif"] = [FONT_NAME] + FONT_CANDIDATES
plt.rcParams["axes.unicode_minus"] = False


def text(ax, x, y, s, size=10, color=None, weight="normal", ha="left", va="center", bbox=None, zorder=None):
    kw = dict(fontsize=size, color=color or PAL["tier0_text"], fontweight=weight,
              ha=ha, va=va, family=FONT_NAME)
    if bbox:
        kw["bbox"] = bbox
    if zorder is not None:
        kw["zorder"] = zorder
    return ax.text(x, y, s, **kw)


def box(ax, x, y, w, h, fc=None, ec=None, lw=0.5, r=0.0):
    return ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.0,rounding_size={r}",
        linewidth=lw, facecolor=fc or PAL["fig_block_bg"],
        edgecolor=ec or PAL["fig_block_border"], clip_on=False))


def line(ax, x1, y1, x2, y2, color=None, lw=0.5, ls="-", zorder=1):
    return ax.plot([x1, x2], [y1, y2], color=color or PAL["fig_block_divider"],
                   linewidth=lw, linestyle=ls, solid_capstyle="round", zorder=zorder)[0]


def draw_three_tier_title(fig, fig_y_px, total_h_px, series, title, subtitle):
    s = fig.add_axes([0, 0, 1, 1])
    s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    y_top = (total_h_px - 20) / total_h_px
    y_main = (total_h_px - 60) / total_h_px
    y_sub = (total_h_px - 100) / total_h_px
    text(s, 0.03, y_top, series, size=11, color=PAL["tier1_text"], weight="500")
    text(s, 0.03, y_main, title, size=20, color=PAL["tier0_text"], weight="500")
    text(s, 0.03, y_sub, subtitle, size=12, color=PAL["tier1_text"])


def draw_title_block(fig, fig_id, fig_name, fig_idx):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.04, 0.26, 0.16
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "图签栏 / title block", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    fields = [
        ("图名", fig_name), ("图号", fig_id), ("比例尺", "1:8000 / A3 横向"),
        ("坐标系", "CGCS2000 / 3°GK 117°E"), ("高程基准", "1985 国家高程基准"),
        ("设计单位", "lzcapp (开源,无资质)"), ("成图日期", "2026-08-09"),
        ("版本", "v2.0"), ("密级", "公开 / public"),
    ]
    for i, (k, v) in enumerate(fields):
        ry = y0 + h - 0.045 - i * 0.014
        text(s, x0 + 0.012, ry, k, size=8)
        text(s, x0 + 0.08, ry, v, size=8, color=PAL["tier1_text"])


def draw_wind_rose(fig):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    cx, cy, r = 0.90, 0.92, 0.05
    box(s, cx - r - 0.03, cy - r - 0.01, 2 * r + 0.06, 2 * r + 0.04, r=0.004)
    s.add_patch(Circle((cx, cy), r, fill=False, ec=PAL["tier0_text"], lw=0.5))
    s.add_patch(Circle((cx, cy), r * 0.7, fill=False, ec=PAL["fig_block_divider"], lw=0.3))
    for ang_deg, w in [(0, 1.0), (90, 0.4), (180, 0.5), (270, 0.6)]:
        a = np.deg2rad(ang_deg)
        s.add_patch(mpatches.Wedge((cx, cy), r, ang_deg - 15, ang_deg + 15, color=PAL["tier0_text"], alpha=0.25 * w))
    for ang_deg in (0, 90, 180, 270):
        a = np.deg2rad(ang_deg)
        x1, y1 = cx + (r - 0.008) * np.cos(a), cy + (r - 0.008) * np.sin(a)
        x2, y2 = cx + (r + 0.008) * np.cos(a), cy + (r + 0.008) * np.sin(a)
        s.plot([x1, x2], [y1, y2], color=PAL["tier0_text"], lw=0.5)
    text(s, cx, cy + r + 0.018, "N", size=9, weight="500", ha="center")
    text(s, cx + r + 0.018, cy, "冬", size=7, color=PAL["tier1_text"], ha="right", va="center")
    text(s, cx - r - 0.018, cy, "夏", size=7, color=PAL["tier1_text"], ha="left", va="center")
    text(s, cx, cy - r - 0.025, "比例 · 1:8000 · 风玫瑰", size=7, color=PAL["tier1_text"], ha="center", va="center")


def draw_scale_bar(ax, x, y, length_m, segments=2, label="0..500..1000 m", color=None):
    color = color or PAL["tier0_text"]
    seg = length_m / segments
    for i in range(segments + 1):
        xi = x + i * seg
        ax.plot([xi, xi], [y - 0.0008, y + 0.0008], color=color, lw=1.2, transform=ax.transData, clip_on=False)
    ax.plot([x, x + length_m], [y, y], color=color, lw=2, transform=ax.transData, clip_on=False)
    for i in range(segments + 1):
        xi = x + i * seg
        text(ax, xi, y - 0.004, f"{int(i * (length_m / segments))}", size=8, color=PAL["tier1_text"], ha="center")
    text(ax, x + length_m / 2, y + 0.004, label, size=8, color=PAL["tier1_text"], ha="center")


def draw_metadata_block(fig):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.04, 0.04, 0.26, 0.10
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "资料来源 / data sources", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    src_lines = ["OSM、ESRI Land Cover、控规草案(待官方)", "本方案 PROV-SITE-001 (~11.4 km², provisional)"]
    for i, ln in enumerate(src_lines):
        text(s, x0 + 0.012, y0 + h - 0.045 - i * 0.018, ln, size=8, color=PAL["tier1_text"])


def draw_land_use_legend(fig, items, groups):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.42, 0.26, 0.40
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "用地分类图例(按大类分组)", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    col_x = [x0 + 0.012, x0 + 0.14]
    y_cursor = y0 + h - 0.05
    for g_name, keys in groups:
        text(s, x0 + 0.012, y_cursor, g_name, size=8, color=PAL["tier1_text"], weight="500")
        y_cursor -= 0.018
        per_col = (len(keys) + 1) // 2
        for i, key in enumerate(keys):
            if key not in items:
                continue
            label, color = items[key]
            col = 0 if i < per_col else 1
            row = i if col == 0 else i - per_col
            x = col_x[col]
            y = y_cursor - row * 0.018
            s.add_patch(Rectangle((x, y - 0.006), 0.012, 0.012, facecolor=color,
                                  edgecolor=PAL["fig_block_divider"], lw=0.3, clip_on=False))
            text(s, x + 0.016, y, label, size=8)
        y_cursor -= per_col * 0.018 + 0.01


def draw_structure_legend(fig, items):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.22, 0.26, 0.16
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "规划结构图例", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    for i, (k, draw_fn, label) in enumerate(items):
        ry = y0 + h - 0.05 - i * 0.022
        draw_fn(s, x0 + 0.025, ry)
        text(s, x0 + 0.05, ry, label, size=8)


def _swatch_circle(s, x, y):
    s.add_patch(Circle((x, y), 0.005, fill=False, ec=PAL["tier1"], lw=1.4, clip_on=False))
    s.add_patch(Circle((x, y), 0.002, fc=PAL["tier1"], clip_on=False))


def _swatch_water(s, x, y):
    s.plot([x - 0.008, x + 0.008], [y, y], color=PAL["water"], lw=1.6, solid_capstyle="round", clip_on=False)


def _swatch_wedge(s, x, y):
    s.plot([x - 0.008, x + 0.008], [y, y], color=PAL["greenway"], lw=3.5, alpha=0.5,
           dashes=(1, 1), solid_capstyle="round", clip_on=False)


def _swatch_prov(s, x, y):
    s.plot([x - 0.008, x + 0.008], [y, y], color=PAL["provisional"], lw=1.0,
           dashes=(1, 1), solid_capstyle="round", clip_on=False)


def _swatch_road_primary(s, x, y):
    s.plot([x - 0.008, x + 0.008], [y, y], color=PAL["primary_road"], lw=1.6, clip_on=False)


def _swatch_road_branch(s, x, y):
    s.plot([x - 0.008, x + 0.008], [y, y], color=PAL["branch_road"], lw=1.4, clip_on=False)


def _swatch_transit(s, x, y):
    s.add_patch(Rectangle((x - 0.004, y - 0.004), 0.008, 0.008, fc=PAL["transit"], clip_on=False))


def draw_caveats(fig, lines):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    line(s, 0.04, 0.21, 0.96, 0.21)
    for i, ln in enumerate(lines):
        text(s, 0.04, 0.20 - i * 0.022, ln, size=9, color=PAL["tier1_text"])


def draw_chapter_caption(fig, idx_str, descr):
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    text(s, 0.04, 0.25, f"图 {idx_str}　{descr}", size=10, color=PAL["tier1_text"], weight="500")


LU_ITEMS = {
    "residential": ("城镇住宅用地", PAL["residential"]),
    "commercial": ("商业服务业用地", PAL["commercial"]),
    "education": ("教育用地", PAL["education"]),
    "research": ("科研用地 (AI R&D)", PAL["research"]),
    "culture": ("文化用地", PAL["culture"]),
    "park": ("公园绿地", PAL["park"]),
    "greenway": ("防护/滨水绿地", PAL["greenway"]),
    "water": ("水系/蓝廊", PAL["water"]),
    "mixed": ("战略留白/混合", PAL["mixed"]),
    "industry": ("产业/工业", PAL["industry"]),
}

LU_GROUPS = [
    ("居住类", ["residential", "commercial"]),
    ("公共与产业类", ["education", "research", "culture", "industry"]),
    ("绿地与水系", ["park", "greenway", "water", "mixed"]),
]


def add_station(ax, x, y, label, side="right"):
    ax.add_patch(Rectangle((x - 0.001, y - 0.001), 0.002, 0.002, fc=PAL["station"], ec="none", zorder=10))
    text(ax, x + 0.004 if side == "right" else x - 0.004, y, label, size=8, color=PAL["tier0_text"],
         ha="left" if side == "right" else "right", va="center", zorder=10,
         bbox=dict(facecolor="white", edgecolor=PAL["fig_block_border"], lw=0.4, boxstyle="round,pad=0.15", alpha=0.92))


def add_key_area(ax, cx, cy, label, sublabel):
    ax.add_patch(Circle((cx, cy), 0.008, fill=True, fc="white", ec=PAL["tier1"], lw=2.0, zorder=9))
    ax.add_patch(Circle((cx, cy), 0.003, fc=PAL["tier1"], zorder=10))
    text(ax, cx, cy + 0.022, label, size=10, weight="500", color=PAL["fig_block_text"], ha="center", zorder=10,
         bbox=dict(facecolor="white", edgecolor=PAL["tier1"], lw=0.6, boxstyle="round,pad=0.3", alpha=0.95))


# (cx, cy, label, range_disc_radius)
CORRIDOR_KEYPOINTS = [
    (0.293, 0.84, "众智园 AI 自主创新加速区", 0.035),
    (0.293, 0.50, "北京 AI 原点社区", 0.045),
    (0.293, 0.13, "大钟寺 AI 产业聚集区", 0.040),
]


def add_corridor_keypoints(ax, with_range_disc=True):
    """Draw the three key areas (with optional semi-transparent range discs so labels
    sit over a visible color block) and four illustrative transit stations.

    The bottom station is repositioned to (0.405, 0.10) so its white-box label
    stays clear of the '大钟寺 AI 产业聚集区' key-area label above its circle.
    """
    if with_range_disc:
        for cx, cy, _, r in CORRIDOR_KEYPOINTS:
            ax.add_patch(Circle((cx, cy), r, fc=PAL["key_area"], ec=PAL["tier2_text"],
                                lw=1.0, alpha=0.45, zorder=4))
    for cx, cy, label, _ in CORRIDOR_KEYPOINTS:
        add_key_area(ax, cx, cy, label, "")
    add_station(ax, 0.355, 0.80, "北五环 站(示意)", "right")
    add_station(ax, 0.207, 0.74, "清华东路西口 站(示意)", "left")
    add_station(ax, 0.355, 0.50, "北沙滩 站(示意)", "right")
    # bottom station: shifted down-right so its label clears the key-area label
    add_station(ax, 0.405, 0.10, "大钟寺 站(示意)", "right")


def corridor_outline(ax, color="black", lw=1.0):
    pts = [
        (0.12, 0.06), (0.14, 0.10), (0.13, 0.18), (0.12, 0.28),
        (0.135, 0.36), (0.145, 0.44), (0.13, 0.52), (0.125, 0.60),
        (0.13, 0.68), (0.135, 0.74), (0.13, 0.80), (0.135, 0.86),
        (0.14, 0.92),
        (0.56, 0.92), (0.565, 0.86), (0.56, 0.80), (0.565, 0.74),
        (0.57, 0.68), (0.565, 0.60), (0.56, 0.52), (0.575, 0.44),
        (0.58, 0.36), (0.57, 0.28), (0.56, 0.18), (0.57, 0.10),
        (0.59, 0.06),
    ]
    poly = plt.Polygon(pts, closed=True, fill=False, ec=color, lw=lw)
    ax.add_patch(poly)


def fig_axes(fig, x_lim, y_lim, x_off=0.04, y_off=0.30, w=0.58, h=0.62):
    ax = fig.add_axes([x_off, y_off, w, h])
    ax.set_xlim(x_lim); ax.set_ylim(y_lim); ax.set_aspect("equal"); ax.axis("off")
    return ax


def build_fig_site_overview(out_path):
    fig = plt.figure(figsize=(13.65, 12.86), dpi=100)
    draw_three_tier_title(fig, 0, 1286,
        "百年京张AI创新带 · 智轨走廊城市设计提案 · A3 册页",
        "总览地图 · 智轨走廊城市设计提案",
        "一帯三核 · 蓝绿楔行复合环 · 11.4 km² (provisional boundary)")
    ax = fig_axes(fig, (0.10, 0.62), (0.05, 0.94), x_off=0.04, y_off=0.30, w=0.58, h=0.62)
    corridor_outline(ax, color=PAL["tier0_text"], lw=1.2)
    land_palette = [PAL["residential"], PAL["commercial"], PAL["education"], PAL["research"],
                    PAL["culture"], PAL["park"], PAL["mixed"], PAL["greenway"]]
    rng = np.random.default_rng(42)
    n_rows = 24
    row_h = 0.035
    for r in range(n_rows):
        yc = 0.07 + r * row_h
        x_start, x_end = 0.205 + rng.uniform(-0.01, 0.01), 0.39 - rng.uniform(-0.01, 0.01)
        n_cells = rng.integers(3, 7)
        cell_w = (x_end - x_start) / n_cells
        for c in range(n_cells):
            xc = x_start + c * cell_w
            color = land_palette[rng.integers(0, len(land_palette))]
            ax.add_patch(Rectangle((xc, yc), cell_w * 0.9, row_h * 0.85, fc=color,
                                   ec=PAL["fig_block_divider"], lw=0.2, zorder=2))
    ax.plot([0.293, 0.293], [0.07, 0.92], color=PAL["water"], lw=2.0, zorder=3, alpha=0.8)
    ax.plot([0.293, 0.293], [0.07, 0.92], color=PAL["greenway"], lw=8, zorder=2.5, alpha=0.4,
            dashes=(2, 1))
    add_corridor_keypoints(ax, with_range_disc=True)
    text(ax, 0.293, 0.04, "PROV-SITE-001 · ~11.4 km²", size=8, color=PAL["tier1_text"], ha="center")
    draw_scale_bar(ax, 0.21, 0.012, length_m=0.06, label="0..500..1000 m")
    draw_wind_rose(fig)
    draw_metadata_block(fig)
    draw_land_use_legend(fig, LU_ITEMS, LU_GROUPS)
    draw_structure_legend(fig, [
        ("core", _swatch_circle, "核心区(众智/原点/大钟寺)"),
        ("water", _swatch_water, "水系蓝廊(清河/小月河)"),
        ("wedge", _swatch_wedge, "蓝绿楔骨架(京张活力带)"),
        ("prov", _swatch_prov, "provisional 临时边界"),
        ("transit", _swatch_transit, "轨道站点(示意)"),
    ])
    draw_caveats(fig, [
        "① 临时边界(PROV-SITE-001)相对 OSM 实测京张铁路遗址公园约偏移 412.5 m;所有面积为内部复算值,非官方控规红线依据,official polygons 发布后整体重算。",
        "② 公共参与、连续无障碍、残障/老年/非智能机走查为设计推演;实施前须补充真实用户研究,不得表述为'已验证'。",
        "③ 配色与符号仅供仓库收录评审,不代表政府组织承诺;落地须经正式审批与部门授权。",
    ])
    draw_chapter_caption(fig, "1", "总览地图:一帯三核,蓝绿楔行复合环。")
    draw_title_block(fig, "JZ-OV-01", "总览地图 一帯三核", "1")
    fig.savefig(out_path, dpi=100, facecolor="white", bbox_inches=None)
    plt.close(fig)


def build_fig_key_areas(out_path):
    fig = plt.figure(figsize=(13.78, 12.86), dpi=100)
    draw_three_tier_title(fig, 0, 1286,
        "百年京张AI创新带 · 智轨走廊城市设计提案 · A3 册页",
        "三处重点区域详细设计",
        "众智园 / 北京 AI 原点 / 大钟寺 · provisional 范围与 agent_generated_design 详细")
    ax = fig_axes(fig, (0.10, 0.62), (0.05, 0.94), x_off=0.04, y_off=0.30, w=0.58, h=0.62)
    corridor_outline(ax, color=PAL["tier0_text"], lw=1.2)
    rng = np.random.default_rng(43)
    n_rows = 28
    row_h = 0.031
    for r in range(n_rows):
        yc = 0.06 + r * row_h
        x_start, x_end = 0.205 + rng.uniform(-0.005, 0.005), 0.39 - rng.uniform(-0.005, 0.005)
        n_cells = rng.integers(5, 9)
        cell_w = (x_end - x_start) / n_cells
        for c in range(n_cells):
            xc = x_start + c * cell_w
            color = PAL["key_building"] if rng.random() < 0.45 else (PAL["residential"] if rng.random() < 0.5 else PAL["mixed"])
            ax.add_patch(Rectangle((xc, yc), cell_w * 0.92, row_h * 0.85, fc=color, ec=PAL["fig_block_divider"], lw=0.2, zorder=2))
    add_corridor_keypoints(ax, with_range_disc=True)
    text(ax, 0.293, 0.04, "PROV-SITE-001 · ~11.4 km²", size=8, color=PAL["tier1_text"], ha="center")
    draw_scale_bar(ax, 0.21, 0.012, length_m=0.06, label="0..500..1000 m")
    draw_wind_rose(fig)
    draw_metadata_block(fig)
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.42, 0.26, 0.18
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "图例说明", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    items = [
        (PAL["key_area"], "重点区域范围 (provisional, 半透明)"),
        (PAL["key_building"], "重点区域内部建筑 (agent_generated_design)"),
        (PAL["mixed"], "全域用地结构 (浅色衬底)"),
    ]
    for i, (c, lab) in enumerate(items):
        ry = y0 + h - 0.05 - i * 0.025
        s.add_patch(Rectangle((x0 + 0.018, ry - 0.007), 0.014, 0.014, fc=c, ec=PAL["fig_block_divider"], lw=0.3, clip_on=False))
        text(s, x0 + 0.04, ry, lab, size=8)
    draw_structure_legend(fig, [
        ("core", _swatch_circle, "核心区(众智/原点/大钟寺)"),
        ("prov", _swatch_prov, "provisional 临时边界"),
        ("transit", _swatch_transit, "轨道站点(示意)"),
    ])
    draw_caveats(fig, [
        "① 重点区域范围为 provisional,非官方控规边界;详细设计为 agent_generated_design 概念稿,非审定方案。",
        "② 公共参与、连续无障碍、残障/老年/非智能机走查为设计推演,尚未发生真实调研。",
        "③ 三处重点区域配色与符号仅供仓库收录评审,不代表政府组织承诺。",
    ])
    draw_chapter_caption(fig, "2", "三处重点区域:众智园 / 北京 AI 原点 / 大钟寺 AI 产业。")
    draw_title_block(fig, "JZ-OV-02", "三处重点区域详细设计", "2")
    fig.savefig(out_path, dpi=100, facecolor="white", bbox_inches=None)
    plt.close(fig)


def build_fig_land_use_structure(out_path):
    fig = plt.figure(figsize=(13.65, 12.86), dpi=100)
    draw_three_tier_title(fig, 0, 1286,
        "百年京张AI创新带 · 智轨走廊城市设计提案 · A3 册页",
        "用地分区结构",
        "按用地单元数排序 · 8 类 · 商业 75 / 住宅 70 / 科研 44 / 文化 43 / 战略 40 / 教育 14 / 广场 6 / 防护 1")
    ax = fig_axes(fig, (0.10, 0.62), (0.05, 0.94), x_off=0.04, y_off=0.30, w=0.58, h=0.62)
    corridor_outline(ax, color=PAL["tier0_text"], lw=1.2)
    use_pal = [
        ("commercial", 75, PAL["commercial"]),
        ("residential", 70, PAL["residential"]),
        ("research", 44, PAL["research"]),
        ("culture", 43, PAL["culture"]),
        ("mixed", 40, PAL["mixed"]),
        ("education", 14, PAL["education"]),
        ("park", 4, PAL["park"]),
        ("greenway", 1, PAL["greenway"]),
    ]
    # 按比例列高 waffle: 列高 ∝ 单元数,全部落在走廊轮廓内(y=0.06..0.92)留上下 0.03 边距
    y_top = 0.89
    y_bot = 0.09
    avail_h = y_top - y_bot  # 0.80
    max_n = max(n for _, n, _ in use_pal)  # 75
    x_left, x_right = 0.165, 0.420
    n_cols = len(use_pal)
    col_w = (x_right - x_left) / n_cols  # 0.0319
    cell_pad = 0.0006
    cells_per_col = 2  # 每列每行 2 格,75 单元=38 行
    for col_idx, (key, n, color) in enumerate(use_pal):
        col_h = (n / max_n) * avail_h
        n_rows = int(np.ceil(n / cells_per_col))
        cell_h = col_h / n_rows
        cell_w = (col_w - cell_pad * (cells_per_col + 1)) / cells_per_col
        x_col = x_left + col_idx * col_w
        for i in range(n):
            row_from_bot = (n - 1 - i) // cells_per_col  # 从底向上数
            col_in_row = (n - 1 - i) % cells_per_col  # 0=左,1=右(从底向上从左到右填)
            xc = x_col + cell_pad + col_in_row * (cell_w + cell_pad)
            yc = y_bot + row_from_bot * cell_h
            ax.add_patch(Rectangle((xc, yc), cell_w, cell_h * 0.92, fc=color, ec=PAL["fig_block_divider"], lw=0.2, zorder=2))
        # 柱顶单元数标签
        text(ax, x_col + col_w / 2, y_bot + col_h + 0.010, f"{n}", size=8, color=PAL["tier1_text"], ha="center")
    # 基线(走廊内 0 单元参考线)
    ax.plot([x_left, x_right], [y_bot, y_bot], color=PAL["fig_block_divider"], lw=0.5, zorder=1)
    text(ax, 0.293, 0.04, "PROV-SITE-001 · 列高 ∝ 单元数(75..1)", size=8, color=PAL["tier1_text"], ha="center")
    draw_scale_bar(ax, 0.21, 0.012, length_m=0.06, label="0..500..1000 m")
    draw_wind_rose(fig)
    draw_metadata_block(fig)
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.40, 0.26, 0.42
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "用地结构(按单元数排序)", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    items_zh = {"commercial":"商业服务业用地","residential":"城镇住宅用地","research":"科研用地 (AI R&D)",
                "culture":"文化用地","mixed":"战略留白/混合","education":"教育用地",
                "park":"公园绿地","greenway":"防护/滨水绿地"}
    # 右侧图例:双行布局 — 细色条(宽 ∝ 单元数)在上,全名标签在下
    legend_max_w = w - 0.04
    for i, (key, n, color) in enumerate(use_pal):
        ry_bar = y0 + h - 0.05 - i * 0.044
        sw_w = legend_max_w * (n / 75)
        s.add_patch(Rectangle((x0 + 0.018, ry_bar - 0.004), sw_w, 0.008, fc=color, ec=PAL["fig_block_divider"], lw=0.3, clip_on=False))
        text(s, x0 + 0.018, ry_bar - 0.020, f"{items_zh[key]}  ({n} 单元)", size=8)
    draw_structure_legend(fig, [
        ("prov", _swatch_prov, "provisional 临时边界"),
    ])
    draw_caveats(fig, [
        "① 单元数按本方案提交包中的地块语义单元统计,非官方控规单元;与 PROV-SITE-001 整体范围一致。",
        "② 列高按单元数线性映射(列高 ∝ 单元数,75 单元顶到 0.89,1 单元仅 1 格),配色与单元分布为概念示意,落地须以官方控规单元为准。",
        "③ 单元数排序仅供本表阅读,不代表规划优先级。",
    ])
    draw_chapter_caption(fig, "3", "用地分区结构:8 类用地按单元数排序(列高 ∝ 单元数,商业 75 / 住宅 70 居前)。")
    draw_title_block(fig, "JZ-OV-03", "用地分区结构", "3")
    fig.savefig(out_path, dpi=100, facecolor="white", bbox_inches=None)
    plt.close(fig)


def build_fig_mobility_bluegreen(out_path):
    fig = plt.figure(figsize=(13.65, 12.86), dpi=100)
    draw_three_tier_title(fig, 0, 1286,
        "百年京张AI创新带 · 智轨走廊城市设计提案 · A3 册页",
        "交通慢行 · 蓝绿公共空间复合系统",
        "蓝绿楔骨架 + 慢行主轴 + 轨道连接 · 慢行优先 + 蓝绿连续")
    ax = fig_axes(fig, (0.10, 0.62), (0.05, 0.94), x_off=0.04, y_off=0.30, w=0.58, h=0.62)
    corridor_outline(ax, color=PAL["tier0_text"], lw=1.2)
    ax.add_patch(Rectangle((0.260, 0.07), 0.066, 0.85, fc=PAL["park"], ec=PAL["fig_block_divider"], lw=0.3, zorder=2))
    ax.plot([0.293, 0.293], [0.07, 0.92], color=PAL["water"], lw=2.0, zorder=3)
    for i, yc in enumerate(np.linspace(0.10, 0.90, 9)):
        ax.add_patch(Rectangle((0.215, yc - 0.012), 0.015, 0.024, fc=PAL["research"], ec=PAL["fig_block_divider"], lw=0.2, zorder=2))
        ax.add_patch(Rectangle((0.355, yc - 0.012), 0.015, 0.024, fc=PAL["research"], ec=PAL["fig_block_divider"], lw=0.2, zorder=2))
    ax.plot([0.205, 0.39], [0.55, 0.55], color=PAL["primary_road"], lw=2.0, zorder=3)
    ax.plot([0.205, 0.39], [0.30, 0.30], color=PAL["primary_road"], lw=2.0, zorder=3)
    ax.plot([0.205, 0.39], [0.75, 0.75], color=PAL["secondary_road"], lw=1.4, zorder=3)
    add_corridor_keypoints(ax, with_range_disc=True)
    text(ax, 0.293, 0.04, "PROV-SITE-001 · 蓝绿楔骨架", size=8, color=PAL["tier1_text"], ha="center")
    draw_scale_bar(ax, 0.21, 0.012, length_m=0.06, label="0..500..1000 m")
    draw_wind_rose(fig)
    draw_metadata_block(fig)
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.42, 0.26, 0.28
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "交通与蓝绿复合系统", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    items = [
        (PAL["park"], "蓝绿空间 (green_space)"),
        (PAL["water"], "公共空间 (public_space)"),
        (PAL["greenway"], "慢行主轴 (greenway)"),
        (PAL["primary_road"], "次干路 (secondary)"),
        (PAL["secondary_road"], "支路 (branch)"),
        (PAL["transit"], "轨道连接 (transit_connection)"),
    ]
    for i, (c, lab) in enumerate(items):
        ry = y0 + h - 0.05 - i * 0.035
        s.add_patch(Rectangle((x0 + 0.018, ry - 0.008), 0.014, 0.014, fc=c, ec=PAL["fig_block_divider"], lw=0.3, clip_on=False))
        text(s, x0 + 0.04, ry, lab, size=8)
    draw_structure_legend(fig, [
        ("water", _swatch_water, "水系蓝廊(清河/小月河)"),
        ("wedge", _swatch_wedge, "蓝绿楔骨架(京张活力带)"),
        ("prov", _swatch_prov, "provisional 临时边界"),
    ])
    draw_caveats(fig, [
        "① 慢行主轴沿京张活力带连续,串联三核,优先非机动车与无障碍通行;轨道连接示意,非规划承诺。",
        "② 蓝绿楔骨架为设计骨架(provisional),非官方控规绿线;落地须以官方蓝绿线为准。",
        "③ 公共空间与慢行系统的连续性、宽度、材质为概念建议,实施前须补充实地踏勘。",
    ])
    draw_chapter_caption(fig, "4", "交通慢行 + 蓝绿公共空间复合系统:慢行优先 + 蓝绿连续。")
    draw_title_block(fig, "JZ-OV-04", "交通慢行 · 蓝绿公共空间", "4")
    fig.savefig(out_path, dpi=100, facecolor="white", bbox_inches=None)
    plt.close(fig)


def build_fig_metrics_evidence(out_path):
    fig = plt.figure(figsize=(13.14, 8.76), dpi=100)
    draw_three_tier_title(fig, 0, 876,
        "百年京张AI创新带 · 智轨走廊城市设计提案 · A3 册页",
        "核心指标复算证据",
        "GeoJSON 投影面积 (EPSG:4548) · site/phasing 面积差 16.918 ㎡为 provisional 边界容差")
    ax = fig.add_axes([0.06, 0.30, 0.62, 0.55])
    ax.set_xlim(0, 1300); ax.set_ylim(0, 7); ax.set_facecolor("white")
    metrics = [
        ("重点区域 (万㎡)", 369.3),
        ("分期面积 (万㎡)", 1141.3),
        ("建筑基底 (万㎡)", 310.6),
        ("公共空间 (万㎡)", 76.2),
        ("蓝绿空间 (万㎡)", 211.9),
        ("用地面积 (万㎡)", 1141.3),
    ]
    bar_color = PAL["research"]
    y_positions = list(range(len(metrics), 0, -1))
    for i, ((label, val), y) in enumerate(zip(metrics, y_positions)):
        ax.barh(y, val, height=0.7, color=bar_color, edgecolor=PAL["tier0_text"], lw=0.3)
        text(ax, val + 10, y, f"≈{val}△", size=9, va="center", color=PAL["tier0_text"])
        text(ax, -5, y, label, size=9, ha="right", va="center", color=PAL["tier0_text"])
    ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
    ax.tick_params(axis="x", labelsize=8, colors=PAL["tier1_text"])
    ax.tick_params(axis="y", labelleft=False, length=0)
    ax.set_xlabel("面积 (万平方米)", fontsize=9, color=PAL["tier1_text"])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(PAL["fig_block_divider"])
    draw_wind_rose(fig)
    draw_metadata_block(fig)
    s = fig.add_axes([0, 0, 1, 1]); s.set_xlim(0, 1); s.set_ylim(0, 1); s.axis("off")
    x0, y0, w, h = 0.72, 0.42, 0.26, 0.20
    box(s, x0, y0, w, h, r=0.005)
    text(s, x0 + 0.012, y0 + h - 0.018, "比例指标 (recalculated)", size=10, weight="500")
    line(s, x0 + 0.012, y0 + h - 0.03, x0 + w - 0.012, y0 + h - 0.03)
    ratios = [("绿地率", "18.6%", PAL["park"]),
              ("公共空间占比", "6.7%", PAL["education"]),
              ("建筑密度", "27.2%", PAL["commercial"])]
    for i, (k, v, c) in enumerate(ratios):
        ry = y0 + h - 0.05 - i * 0.04
        s.add_patch(Rectangle((x0 + 0.018, ry - 0.008), 0.014, 0.014, fc=c, ec=PAL["fig_block_divider"], lw=0.3, clip_on=False))
        text(s, x0 + 0.04, ry, f"{k}", size=8)
        text(s, x0 + w - 0.018, ry, f"{v}", size=9, weight="500", ha="right", color=PAL["tier1_text"])
    draw_caveats(fig, [
        "① 比例指标由 GeoJSON 投影面积 (EPSG:4548) 复算;site/phasing 面积差 16.918 ㎡ 为 provisional 边界容差,待官方多边形重算。",
        "② △ 表示 provisional 临时面积,非精确规划指标,不得作为法定红线依据。",
        "③ 比例指标与复算细节详见 [source:METRICS-JSON] metrics.json;FAR/建筑高度/总建筑面积列为 unknown。",
    ])
    draw_chapter_caption(fig, "5", "核心指标复算:六项面积 + 三项比例,均以 GeoJSON 投影面积复算。")
    draw_title_block(fig, "JZ-OV-05", "核心指标复算证据", "5")
    fig.savefig(out_path, dpi=100, facecolor="white", bbox_inches=None)
    plt.close(fig)


def main():
    targets = [
        ("site-overview.png", build_fig_site_overview),
        ("key-areas.png", build_fig_key_areas),
        ("land-use-structure.png", build_fig_land_use_structure),
        ("mobility-bluegreen.png", build_fig_mobility_bluegreen),
        ("metrics-evidence.png", build_fig_metrics_evidence),
    ]
    for fname, fn in targets:
        out = os.path.join(FIG_DIR, fname)
        print(f"building {fname} -> {out}")
        fn(out)
    print("all 5 figures v2 built")


if __name__ == "__main__":
    main()
