# PCBWay Rev A Assembly Notes

## Assembly Intent

This is intended as a fully assembled PCBWay PCBA order. The Seeed XIAO RP2040 is treated as an SMD castellated module, not as a hand-soldered development board.

## Do Not Populate / Do Not Install

- Rev A does not connect RJ45 pin 2 to anything. This intentionally avoids feeding power into an unknown microphone accessory-power pin.
- There are no DNP components in the final Rev A PCBWay BOM.

## Through-Hole Parts

- `J1` is an RJ45 through-hole connector footprint.
- `TP1`-`TP4` are test pads and can be omitted if PCBWay treats them as through-hole assembly cost adders.
- Mounting holes are NPTH and should not be plated.

## Placement Intent

- RJ45 mic jack should sit on the left edge of the board.
- XIAO RP2040 USB-C connector should be exposed on the opposite edge.
- Keep `MIC_RAW`, `MIC_AC`, `VREF`, and `MIC_ADC` traces short and away from digital GPIO where practical.
- Put `C5` close to `U2` VDD/VSS.
- Put `C3` close to the XIAO ADC input pad.

## Required Order Files

PCBWay requests these for PCBA:

- Gerbers
- Drill files
- BOM CSV/XLSX
- Pick-and-place / centroid / XYRS file

Use `manufacturing/revA/BOM_pcbway_revA.csv` as the assembly BOM for Rev A.
