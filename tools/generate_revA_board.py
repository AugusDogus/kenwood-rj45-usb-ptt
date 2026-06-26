#!/usr/bin/env python3
from pathlib import Path
import os
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware" / "kicad" / "radio-mic-usb-ptt.kicad_pcb"

NETS = {
    "": 0,
    "GND": 1,
    "+3V3": 2,
    "MIC_RAW": 3,
    "MIC_AC": 4,
    "VREF": 5,
    "NINV": 6,
    "MIC_AMP": 7,
    "MIC_ADC": 8,
    "PTT_RAW": 9,
    "PTT_GPIO": 10,
    "UP_RAW": 11,
    "UP_GPIO": 12,
    "DOWN_RAW": 13,
    "DOWN_GPIO": 14,
    "PTT_LED_DRIVE": 15,
    "LED_A": 16,
    "MIC_PWR": 17,
    "SPARE_B": 18,
}


def u():
    return str(uuid4())


def net(name):
    return f'(net {NETS[name]} "{name}")' if name else '(net 0 "")'


def pad_net(name):
    return f'(net {NETS[name]} "{name}")' if name else ''


def xy(n):
    return f"{n:.3f}".rstrip("0").rstrip(".")


def prop(name, value, x, y, layer="F.Fab", hide=True):
    h = " hide" if hide else ""
    return f'''    (property "{name}" "{value}" (at {xy(x)} {xy(y)} 0) (layer "{layer}"){h}
      (effects (font (size 1 1) (thickness 0.15)))
    )'''


def fp_header(lib, name, ref, value, x, y, rot=0, attr="smd"):
    # Footprints are embedded directly in the board. Leaving off the library
    # nickname avoids KiCad DRC warnings about generated geometry not matching
    # a separate footprint library copy.
    return f'''  (footprint "{name}"
    (layer "F.Cu")
    (uuid "{u()}")
    (at {xy(x)} {xy(y)} {rot})
{prop("Reference", ref, 0, -1.6, "F.Fab", True)}
{prop("Value", value, 0, 1.6, "F.Fab", True)}
    (attr {attr})'''


def fp_end():
    return "  )"


def two_pad(lib, name, ref, value, x, y, nets, rot=0, dnp=False):
    attr = "smd" + (" dnp" if dnp else "")
    lines = [fp_header(lib, name, ref, value, x, y, 0, attr)]
    if rot == 90:
        p1 = (0, -0.8, 90)
        p2 = (0, 0.8, 90)
    else:
        p1 = (-0.8, 0, 0)
        p2 = (0.8, 0, 0)
    lines += [
        '    (fp_rect (start -1.55 -0.75) (end 1.55 0.75) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd") (uuid "%s"))' % u(),
        f'    (pad "1" smd roundrect (at {xy(p1[0])} {xy(p1[1])} {p1[2]}) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) {pad_net(nets[0])} (uuid "{u()}"))',
        f'    (pad "2" smd roundrect (at {xy(p2[0])} {xy(p2[1])} {p2[2]}) (size 0.8 0.95) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) {pad_net(nets[1])} (uuid "{u()}"))',
        fp_end(),
    ]
    return "\n".join(lines)


def testpoint(ref, value, x, y, netname):
    return f'''  (footprint "TestPoint_THTPad_D1.5mm"
    (layer "F.Cu")
    (uuid "{u()}")
    (at {xy(x)} {xy(y)} 0)
{prop("Reference", ref, 0, -1.5)}
{prop("Value", value, 0, 1.5, "F.Fab", True)}
    (attr exclude_from_pos_files)
    (pad "1" thru_hole circle (at 0 0) (size 1.5 1.5) (drill 0.7) (layers "*.Cu" "*.Mask") {pad_net(netname)} (uuid "{u()}"))
  )'''


def mounting(ref, x, y):
    return f'''  (footprint "MountingHole_3.2mm"
    (layer "F.Cu")
    (uuid "{u()}")
    (at {xy(x)} {xy(y)} 0)
{prop("Reference", ref, 0, -2)}
{prop("Value", "MountingHole_3.2mm", 0, 2, "F.Fab", True)}
    (attr exclude_from_pos_files exclude_from_bom)
    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask") (uuid "{u()}"))
  )'''


def rj45():
    x, y = 7, 21
    pad_defs = [
        ("1", 0, 0, "rect", ""),
        ("3", 2.032, 0, "circle", "GND"),
        ("5", 4.064, 0, "circle", "GND"),
        ("7", 6.096, 0, "circle", "GND"),
        ("2", 1.016, 1.78, "circle", ""),
        ("4", 3.048, 1.78, "circle", "PTT_RAW"),
        ("6", 5.08, 1.78, "circle", "MIC_RAW"),
        ("8", 7.112, 1.78, "circle", ""),
    ]
    lines = [fp_header("Connector_RJ", "RJ45_Amphenol_RJHSE5380", "J1", "KMC RJ45 MIC", x, y, 0, "through_hole")]
    lines += [
        '    (fp_rect (start -6.22 -8.5) (end 13.34 8.25) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd") (uuid "%s"))' % u(),
    ]
    for num, px, py, shape, netname in pad_defs:
        lines.append(f'    (pad "{num}" thru_hole {shape} (at {xy(px)} {xy(py)} 0) (size 1.5 1.5) (drill 0.89) (layers "*.Cu" "*.Mask") {pad_net(netname)} (uuid "{u()}"))')
    lines += [
        f'    (pad "" np_thru_hole circle (at -2.79 -2.54 0) (size 3.25 3.25) (drill 3.25) (layers "*.Cu" "*.Mask") (uuid "{u()}"))',
        f'    (pad "" np_thru_hole circle (at 9.91 -2.54 0) (size 3.25 3.25) (drill 3.25) (layers "*.Cu" "*.Mask") (uuid "{u()}"))',
        f'    (pad "SH" thru_hole circle (at 11.69 0.89 0) (size 2.3 2.3) (drill 1.57) (layers "*.Cu" "*.Mask") {pad_net("GND")} (uuid "{u()}"))',
        f'    (pad "SH" thru_hole circle (at -4.57 0.89 0) (size 2.3 2.3) (drill 1.57) (layers "*.Cu" "*.Mask") {pad_net("GND")} (uuid "{u()}"))',
        fp_end(),
    ]
    return "\n".join(lines)


def xiao():
    x, y = 46, 22.5
    nets = {
        "1": "MIC_ADC", "7": "PTT_GPIO",
        "11": "PTT_LED_DRIVE", "12": "+3V3", "13": "GND", "18": "GND", "20": "GND",
    }
    pads = [
        ("1", 0.835, -18.12, 2.75, 2, 0), ("2", 0.835, -15.58, 2.75, 2, 0),
        ("3", 0.835, -13.04, 2.75, 2, 0), ("4", 0.835, -10.5, 2.75, 2, 0),
        ("5", 0.835, -7.96, 2.75, 2, 0), ("6", 0.835, -5.42, 2.75, 2, 0),
        ("7", 0.835, -2.88, 2.75, 2, 0), ("8", 17, -2.88, 2.75, 2, 0),
        ("9", 17, -5.42, 2.75, 2, 0), ("10", 17, -7.96, 2.75, 2, 0),
        ("11", 17, -10.5, 2.75, 2, 0), ("12", 17, -13.04, 2.75, 2, 0),
        ("13", 17, -15.58, 2.75, 2, 0), ("14", 17, -18.12, 2.75, 2, 0),
    ]
    lines = [fp_header("Seeed_Studio_XIAO_Series", "XIAO-RP2040-SMD", "U1", "Seeed XIAO RP2040", x, y, 0, "smd")]
    lines += [
        '    (fp_rect (start 0 -21) (end 17.8 0) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd") (uuid "%s"))' % u(),
    ]
    for num, px, py, sx, sy, circle in pads:
        shape = "circle" if circle else "roundrect"
        rr = "" if circle else "(roundrect_rratio 0.25)"
        lines.append(f'    (pad "{num}" smd {shape} (at {xy(px)} {xy(py)} 0) (size {xy(sx)} {xy(sy)}) (layers "F.Cu" "F.Paste" "F.Mask") {rr} {pad_net(nets.get(num, ""))} (uuid "{u()}"))')
    lines.append(fp_end())
    return "\n".join(lines)


def msop():
    x, y = 31, 22
    nets = {"1":"MIC_AMP", "2":"NINV", "3":"MIC_AC", "4":"GND", "5":"VREF", "6":"", "7":"", "8":"+3V3"}
    pads = [("1",-1.75,-0.975),("2",-1.75,-0.325),("3",-1.75,0.325),("4",-1.75,0.975),("5",1.75,0.975),("6",1.75,0.325),("7",1.75,-0.325),("8",1.75,-0.975)]
    lines = [fp_header("radio-mic-usb-ptt", "MSOP-8_3x3mm_P0.65mm", "U2", "MCP6002T-E/MS", x, y, 0, "smd")]
    lines += ['    (fp_rect (start -2.55 -1.85) (end 2.55 1.85) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd") (uuid "%s"))' % u()]
    for num, px, py in pads:
        lines.append(f'    (pad "{num}" smd rect (at {xy(px)} {xy(py)} 0) (size 1 0.4) (layers "F.Cu" "F.Paste" "F.Mask") {pad_net(nets[num])} (uuid "{u()}"))')
    lines.append(fp_end())
    return "\n".join(lines)


def seg(netname, a, b, layer="F.Cu", width=0.25):
    return f'  (segment (start {xy(a[0])} {xy(a[1])}) (end {xy(b[0])} {xy(b[1])}) (width {width}) (layer "{layer}") (net {NETS[netname]}) (uuid "{u()}"))'


def via(netname, p, size=0.6, drill=0.3):
    return f'  (via (at {xy(p[0])} {xy(p[1])}) (size {size}) (drill {drill}) (layers "F.Cu" "B.Cu") (net {NETS[netname]}) (uuid "{u()}"))'


def path(netname, pts, layer="F.Cu", width=0.25):
    return "\n".join(seg(netname, a, b, layer, width) for a, b in zip(pts, pts[1:]))


footprints = [
    rj45(), xiao(), msop(),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R1", "2.2k", 21, 32, ["+3V3", "MIC_RAW"]),
    two_pad("radio-mic-usb-ptt", "C_0603_1608Metric", "C1", "1uF", 27, 34, ["MIC_RAW", "MIC_AC"]),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R13", "100k", 25, 24, ["MIC_AC", "VREF"]),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R2", "100k", 36, 16, ["+3V3", "VREF"], 90),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R3", "100k", 36, 19, ["VREF", "GND"], 90),
    two_pad("radio-mic-usb-ptt", "C_0603_1608Metric", "C2", "1uF", 40, 19, ["VREF", "GND"], 90),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R4", "10k", 27, 27, ["NINV", "VREF"]),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R5", "200k", 27, 19, ["MIC_AMP", "NINV"]),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R6", "1k", 38, 11, ["MIC_AMP", "MIC_ADC"]),
    two_pad("radio-mic-usb-ptt", "C_0603_1608Metric", "C3", "1nF", 42, 11, ["MIC_ADC", "GND"], 90),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R7", "10k", 30, 12, ["+3V3", "PTT_GPIO"], 90),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R8", "1k", 22, 10, ["PTT_RAW", "PTT_GPIO"]),
    two_pad("radio-mic-usb-ptt", "C_0603_1608Metric", "C4", "100nF", 25, 13, ["PTT_GPIO", "GND"], 90),
    two_pad("radio-mic-usb-ptt", "R_0603_1608Metric", "R11", "1k", 56, 28, ["PTT_LED_DRIVE", "LED_A"]),
    two_pad("radio-mic-usb-ptt", "LED_0603_1608Metric", "D1", "PTT_LED", 60, 28, ["LED_A", "GND"]),
    two_pad("radio-mic-usb-ptt", "C_0603_1608Metric", "C5", "100nF", 37, 25, ["+3V3", "GND"], 90),
    mounting("H1", 5, 5), mounting("H2", 67, 5), mounting("H3", 5, 37), mounting("H4", 67, 37),
]

routes = [
    # Local analog input path on top layer.
    path("MIC_RAW", [(11.08,22.78),(11.08,26),(17.8,27),(20.2,25)]),
    path("MIC_AC", [(21.8,25),(24.2,24),(29.25,22.325)]),
    path("VREF", [(25.8,24),(27.8,27),(32.75,22.975)]),
    path("VREF", [(32.75,22.975),(35,23),(35,18.2),(36,18.2),(36,16.8)]),
    path("VREF", [(36,18.2),(39,18.2)]),
    path("NINV", [(29.25,21.675),(27.8,19)]),
    path("NINV", [(29.25,21.675),(28.2,24),(26.2,27)]),
    path("MIC_AMP", [(29.25,21.025),(26.2,19),(37.2,11)]),
    path("MIC_ADC", [(38.8,11),(42,10.2)]),
    # MIC_ADC to XIAO ADC on bottom layer.
    path("MIC_ADC", [(42,10.2),(42,9.3)], "F.Cu"), via("MIC_ADC", (42,9.3)),
    path("MIC_ADC", [(42,9.3),(45.5,5),(46.835,4.38)], "B.Cu"), via("MIC_ADC", (45.5,5)), path("MIC_ADC", [(45.5,5),(46.835,4.38)], "F.Cu"),
    # PTT input.
    path("PTT_RAW", [(9.048,22.78),(19.2,20)]),
    path("PTT_GPIO", [(20.8,20),(23,18),(24,16),(25,12.2),(30,12.8)]),
    path("PTT_GPIO", [(30,12.8),(31,13)], "F.Cu"), via("PTT_GPIO", (31,13)),
    path("PTT_GPIO", [(31,13),(45.5,19.6)], "B.Cu"), via("PTT_GPIO", (45.5,19.6)), path("PTT_GPIO", [(45.5,19.6),(46.835,19.62)], "F.Cu"),
    # LED.
    path("PTT_LED_DRIVE", [(63,12),(55.2,15)]),
    path("LED_A", [(56.8,15),(59.2,15)]),
    # +3V3 distribution mostly on bottom layer.
    path("+3V3", [(63,9.46),(61.5,9.46)], "F.Cu"), via("+3V3", (61.5,9.46)),
    path("+3V3", [(61.5,9.46),(68,9.46),(68,34),(15,34),(15,27),(16.2,27)], "B.Cu"),
    via("+3V3", (15,27)), path("+3V3", [(15,27),(16.2,27)], "F.Cu"),
    path("+3V3", [(15,34),(15,17),(16.2,17)], "B.Cu"), via("+3V3", (15,17)), path("+3V3", [(15,17),(16.2,17)], "F.Cu"),
    path("+3V3", [(61.5,9.46),(34,9.46),(34,21),(32.75,21.025)], "B.Cu"), via("+3V3", (34,21)), path("+3V3", [(34,21),(32.75,21.025)], "F.Cu"),
    path("+3V3", [(34,9.46),(35,15),(36,15.2)], "B.Cu"), via("+3V3", (35,15)), path("+3V3", [(35,15),(36,15.2)], "F.Cu"),
    path("+3V3", [(35,15),(29,11),(30,11.2)], "B.Cu"), via("+3V3", (29,11)), path("+3V3", [(29,11),(30,11.2)], "F.Cu"),
    path("+3V3", [(34,21),(35,23.2),(34,23.2)], "B.Cu"), via("+3V3", (35,23.2)), path("+3V3", [(35,23.2),(34,23.2)], "F.Cu"),
    # Ground distribution on bottom layer with short top stubs.
    path("GND", [(1.43,21.89),(8.032,21),(10.064,21),(12.096,21),(17.69,21.89)], "B.Cu"),
    path("GND", [(17.69,21.89),(28,24),(41,24),(56.287,22),(61,16),(63,6.92)], "B.Cu"),
    via("GND", (28,24)), path("GND", [(28,24),(29.25,22.975)], "F.Cu"),
    via("GND", (35,25)), path("GND", [(35,25),(34,24.8)], "F.Cu"), path("GND", [(35,25),(41,24)], "B.Cu"),
    via("GND", (40,20)), path("GND", [(40,20),(39,19.8)], "F.Cu"), path("GND", [(40,20),(41,24)], "B.Cu"),
    via("GND", (43,12)), path("GND", [(43,12),(42,11.8)], "F.Cu"), path("GND", [(43,12),(41,24)], "B.Cu"),
    via("GND", (24,14)), path("GND", [(24,14),(25,13.8)], "F.Cu"), path("GND", [(24,14),(41,24)], "B.Cu"),
    via("GND", (61,16)), path("GND", [(61,16),(60.8,15)], "F.Cu"),
    via("GND", (61,6.92)), path("GND", [(61,6.92),(63,6.92)], "F.Cu"),
    via("GND", (56.287,22)), path("GND", [(56.287,22),(56.287,20.64)], "F.Cu"),
    via("GND", (56.287,7.5)), path("GND", [(56.287,7.5),(56.287,6.162)], "F.Cu"), path("GND", [(56.287,7.5),(61,6.92)], "B.Cu"),
]

board = f'''(kicad_pcb
  (version 20241229)
  (generator "radio-mic-usb-ptt-revA-generator")
  (generator_version "1.0")
  (general (thickness 1.6) (legacy_teardrops no))
  (paper "A4")
  (title_block (title "radio-mic-usb-ptt RevA") (date "2026-06-25"))
  (layers
    (0 "F.Cu" signal)
    (2 "B.Cu" signal)
    (9 "F.Adhes" user "F.Adhesive")
    (11 "B.Adhes" user "B.Adhesive")
    (13 "F.Paste" user)
    (15 "B.Paste" user)
    (5 "F.SilkS" user "F.Silkscreen")
    (7 "B.SilkS" user "B.Silkscreen")
    (1 "F.Mask" user)
    (3 "B.Mask" user)
    (17 "Dwgs.User" user "User.Drawings")
    (19 "Cmts.User" user "User.Comments")
    (21 "Eco1.User" user "User.Eco1")
    (23 "Eco2.User" user "User.Eco2")
    (25 "Edge.Cuts" user)
    (27 "Margin" user)
    (31 "F.CrtYd" user "F.Courtyard")
    (29 "B.CrtYd" user "B.Courtyard")
    (35 "F.Fab" user)
    (33 "B.Fab" user)
  )
  (setup
    (pad_to_mask_clearance 0)
    (allow_soldermask_bridges_in_footprints no)
    (tenting front back)
    (pcbplotparams (layerselection 0x00000000_00000000_55555555_5755f5ff) (plot_on_all_layers_selection 0x00000000_00000000_00000000_00000000) (disableapertmacros no) (usegerberextensions no) (usegerberattributes yes) (usegerberadvancedattributes yes) (creategerberjobfile yes) (outputformat 1) (outputdirectory ""))
  )
{chr(10).join('  ' + net(n) for n in NETS)}
  (embedded_fonts no)
  (gr_line (start 0 0) (end 72 0) (stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "{u()}"))
  (gr_line (start 72 0) (end 72 42) (stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "{u()}"))
  (gr_line (start 72 42) (end 0 42) (stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "{u()}"))
  (gr_line (start 0 42) (end 0 0) (stroke (width 0.1) (type default)) (layer "Edge.Cuts") (uuid "{u()}"))
  (gr_text "radio-mic-usb-ptt RevA" (at 36 38 0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 1.2 1.2) (thickness 0.15))))
  (gr_text "RJ45 MIC" (at 7 10 0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 1 1) (thickness 0.15))))
  (gr_text "USB-C ->" (at 58 2.2 0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 1 1) (thickness 0.15))))
{chr(10).join(footprints)}
{chr(10).join([] if os.environ.get("NO_ROUTES") == "1" else routes)}
)
'''

BOARD.write_text(board)
print(f"Wrote {BOARD}")
