# kenwood-rj45-usb-ptt

USB push-to-talk adapter for Kenwood-style RJ45 handheld microphones such as KMC-30 / KMC-32 compatible mics.

Rev A is a PCBWay-assemblable board. It uses a Seeed XIAO RP2040 module for USB and firmware, an MCP6002 analog front-end for the microphone, and an RJ45 jack for the hand mic.

## What To Upload To PCBWay

Use the files in `manufacturing/revA/`:

- `radio-mic-usb-ptt-revA-gerbers-drill.zip` for PCB fabrication
- `BOM_pcbway_revA.csv` for assembly BOM
- `positions_revA.csv` for pick-and-place / centroid
- `PCBWAY_NOTES_revA.md` for assembly notes

`manufacturing/revA/ORDER_INSTRUCTIONS.md` has the same checklist in upload order.

## Current Status

- KiCad DRC: 0 violations
- Unconnected items: 0
- Firmware: not implemented yet
- First hardware spin: order a small quantity only

## Repository Layout

- `hardware/kicad/` - KiCad 9 project, board, schematic, and vendored footprint/symbol libraries
- `manufacturing/revA/` - PCBWay-ready fabrication and assembly outputs
- `firmware/` - firmware plan and future XIAO RP2040 code
- `tools/` - board generation helper used for Rev A
- `docs/` - design/order notes

## Rev A Architecture

```text
Kenwood RJ45 hand mic
  mic audio -> electret bias -> MCP6002 preamp -> XIAO RP2040 ADC -> USB audio microphone
  PTT       -> debounced GPIO -> XIAO RP2040 USB HID keyboard -> F13 while held

Computer USB-C -> exposed USB-C connector on Seeed XIAO RP2040 module
```

RJ45 pin 2 is intentionally left open. Some Kenwood-style radios provide accessory power on that pin, but Rev A does not feed voltage into it.

## Open In KiCad

Open:

`hardware/kicad/radio-mic-usb-ptt.kicad_pro`

The KiCad project uses project-relative library tables, so it should open from this repo without global library setup.

## Regenerate Rev A Board

The final board file is already generated and routed. To regenerate the unrouted board from the helper script:

```sh
NO_ROUTES=1 python3 tools/generate_revA_board.py
```

Then autoroute/import in KiCad or with the MCP tooling. Do not run multi-attempt autorouting unless you explicitly want multiple confirmation prompts.
