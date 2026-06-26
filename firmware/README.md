# Firmware Plan

Target: Seeed XIAO RP2040.

Required USB functions:

- USB HID keyboard: hold `F13` while `PTT_GPIO` is active.
- USB Audio Class microphone: stream ADC samples from `MIC_ADC`.

Rev A pin mapping:

| Function | XIAO pin | RP2040 GPIO | Schematic net |
| --- | --- | ---: | --- |
| Mic ADC | D0 | GPIO26 / ADC0 | `MIC_ADC` |
| PTT input | D6 | GPIO0 | `PTT_GPIO` |
| Optional UP input | D7 | GPIO1 | `UP_GPIO` |
| Optional DOWN input | D8 | GPIO2 | `DOWN_GPIO` |
| PTT/status LED | D10 | GPIO3 | `PTT_LED_DRIVE` |

Recommended firmware stack:

- Pico SDK
- TinyUSB device stack
- Composite USB descriptors for Audio Class + HID keyboard

PTT behavior:

```c
if (ptt_pressed && !held) {
    hid_keyboard_press(F13);
    held = true;
}

if (!ptt_pressed && held) {
    hid_keyboard_release(F13);
    held = false;
}
```

Audio behavior:

- Sample ADC0 at a speech-oriented rate such as 16 kHz or 48 kHz.
- Center samples around the ADC midscale produced by the analog `VREF` circuit.
- Present mono 16-bit PCM over USB Audio Class.
