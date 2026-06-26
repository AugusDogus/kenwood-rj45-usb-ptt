# PCBWay Rev A Order Instructions

Upload these files for a PCB + assembly order:

- PCB fabrication: `radio-mic-usb-ptt-revA-gerbers-drill.zip`
- Assembly BOM: `BOM_pcbway_revA.csv`
- Pick-and-place / centroid: `positions_revA.csv`
- Notes: `PCBWAY_NOTES_revA.md`

Important assembly notes:

- Rev A is top-side assembly only.
- RJ45 pin 2 is intentionally left open.
- There are no DNP parts in the final Rev A BOM.
- Confirm whether PCBWay can source `U1` Seeed Studio XIAO RP2040, MPN `102010428`. If not, order it as consigned/kitted assembly or revise to a bare RP2040 design later.

Validation status:

- KiCad 9.0.9 DRC was run.
- DRC has zero violations and zero unconnected items.

Do not order large quantities from Rev A. This is the first hardware spin and still needs mic pinout and firmware validation.
