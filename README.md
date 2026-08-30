# ESPHome Mirage M-400 Controller

Control an Autonomic Mirage M-400 amplifier via RS-232 serial communication using an ESP32 and ESPHome.

This is a rewrite based on the actual protocol documented in the Autonomic M-400 manual
("Ethernet / RS232 Protocol" section), which differs from earlier assumptions in this
project in a few important ways — see **What Changed** below if you're migrating from
the previous version.

## Hardware Requirements

| Component        | Details                            |
| ----------------- | ---------------------------------- |
| Microcontroller   | ESP32 (e.g., ESP32-DevKitC-v1)      |
| RS-232 Converter  | MAX3232 TTL ↔ RS-232 level shifter |
| Cable             | DB9 straight-through (per manual)  |
| GPIO Pins         | TX: GPIO16, RX: GPIO17             |

## Wiring

On a MAX3232, `T1IN`/`T1OUT` is the **transmit** channel (TTL in → RS-232 out) and
`R1IN`/`R1OUT` is the **receive** channel (RS-232 in → TTL out). Wire it as:

- **ESP32 TX (GPIO16)** → **MAX3232 T1IN**
- **MAX3232 T1OUT** → **Mirage M-400 RX (DB9 pin 2)**
- **Mirage M-400 TX (DB9 pin 3)** → **MAX3232 R1IN**
- **MAX3232 R1OUT** → **ESP32 RX (GPIO17)**
- **GND** → **GND** (both sides)

> An earlier version of this README had ESP32 TX wired into `R1IN` and ESP32 RX wired
> into `T1OUT` — that's backwards (TX into the receive channel, RX into the transmit
> channel) and will break communication. Double check your actual wiring against the
> above before assuming it's a software bug.

The manual also notes the RS232 cable must be **straight-through**, not a null-modem cable.

## Installation

```yaml
external_components:
  - source: github://letigre2389/mirage-m400-controller-esphome
    components: [mirage_m400]

uart:
  - id: mirage_uart
    tx_pin: GPIO16
    rx_pin: GPIO17
    baud_rate: 9600
    data_bits: 8
    parity: NONE
    stop_bits: 1

mirage_m400:
  id: mirage_m400_device
  uart_id: mirage_uart
  zone_offset: 0     # see "Zone Addressing" below
  zone_count: 4
  poll_interval: 15s
```

## Usage

### Switches (Power & Mute)

```yaml
switch:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Power"
    zone: 1
    type: power

  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Mute"
    zone: 1
    type: mute
```

### Number (Volume)

```yaml
number:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Volume"
    zone: 1
```

Range is fixed at 0–160 to match the amp's protocol (see below) — no need to set
`min_value`/`max_value`/`step` yourself.

### Select (Source)

```yaml
select:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Source"
    zone: 1
```

Exposes S1–S8 as select options.

### Text Sensor (raw last response)

```yaml
text_sensor:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Mirage M-400 Last Response"
```

Useful for reverse-engineering/verifying the protocol against your actual unit —
turn on `logger: level: DEBUG` and watch this entity plus the ESPHome logs.

### Home Assistant Service (raw command)

```yaml
api:
  services:
    - service: send_mirage_command
      variables:
        command: string
      then:
        - lambda: |-
            id(mirage_m400_device)->send_raw_command(command);
```

```yaml
service: esphome.mirage_m400_controller_send_mirage_command
data:
  command: "010A00"   # Standby OFF (zone ON) for protocol zone 0x0A
```

## Command Format

`<command><zone><data>`, sent as ASCII hex characters, terminated with a line feed.

| Function      | Command | Data                                                   |
| ------------- | ------- | ------------------------------------------------------- |
| Standby       | `01`    | `00`=Standby OFF (zone ON), `01`=Standby ON (zone OFF), `04`=Toggle |
| Mute          | `02`    | `00`=Mute, `01`=Un-mute, `02`=Toggle                    |
| Source Select | `03`    | `00`=S5 `01`=S6 `02`=S7 `03`=S4 `04`=S8 `05`=S1 `06`=S2 `07`=S3 |
| Volume        | `04`    | `00`–`A0` (0–160 decimal)                                |
| Bass          | `05`    | `F4`–`0C` (-12dB to +12dB)                                |
| Treble        | `06`    | `F4`–`0C` (-12dB to +12dB)                                |
| Balance       | `07`    | `EC`–`14` (Left -20dB to Right -20dB)                     |
| Send All Parameters | `09` | value ignored — triggers a full status dump (>144 bytes) |

### Zone byte

The zone byte's lower 5 bits encode the zone (0–31); `FF` addresses all zones. The
manual's own examples use **zone 0** as valid (e.g. "Zone 10 = hex 0A" implies zones
count from 0), which suggests the wire protocol is 0-indexed even though the front
panel and web app label zones starting at 1.

## Zone Addressing

`zone_offset` (default `0`) controls the mapping from the physical zone numbers you
use in your YAML (1, 2, 3, 4 — matching the amp's labeling) to the protocol's zone
byte: `protocol_zone = physical_zone - 1 + zone_offset`.

**Verify this against your actual amp** — turn on the Last Response text sensor and
`logger: level: DEBUG`, toggle Zone 1's power switch, and confirm zone 1 (not zone 2)
actually responds. If it's off by one, set `zone_offset: 1`.

## What Changed (vs. the earlier version of this project)

These came directly out of reading the manual's protocol appendix and are the most
likely causes of "the ESP32 sends something but the amp doesn't do the right thing":

1. **Standby polarity was inverted.** The old code (and README) assumed `01` = ON,
   `00` = OFF for the power command. The manual says the opposite: `00` = Standby OFF
   (i.e. the zone is *on*), `01` = Standby ON (i.e. the zone is *off*). If your power
   switches were toggling the wrong direction, or seemed to do nothing, this is
   almost certainly why.
2. **Source data bytes are not sequential.** `S1`–`S8` map to `05, 06, 07, 03, 00, 01,
   02, 04` — not `00`–`07` in order. Selecting "S1" with the naive mapping actually
   selected S6.
3. **Volume range is 0–160 (`0x00`–`0xA0`), not 0–100.** A number entity capped at
   100 can never reach the amp's actual maximum, and treating the raw byte as a
   percentage misrepresents the true level.
4. **Terminator is a line feed**, not a carriage return as previously documented.
5. **Zone byte is likely 0-indexed** — see "Zone Addressing" above. This is
   configurable (`zone_offset`) since it's an inference from the manual's examples,
   not explicitly stated as "physical zone 1 = protocol zone 0".
6. **Wiring**: TX/RX were mapped to the wrong MAX3232 channels — see Wiring above.

## Troubleshooting

- **Nothing happens at all**: verify wiring per the corrected diagram above, and
  confirm baud rate (9600 8N1).
- **Commands seem to hit the wrong zone**: try flipping `zone_offset` between `0` and `1`.
- **Power/mute toggle the wrong way**: this rewrite already accounts for the inverted
  Standby polarity — if you're still seeing inversion, your amp firmware may differ
  from the manual; watch the Last Response sensor to confirm.
- **Volume does nothing**: confirm you're not sending values above 160 (0xA0) or a
  malformed 2-part command; this rewrite sends a single `04<zone><value>` triplet
  which matches the manual's command table.
- Monitor everything with `esphome logs mirage-m400-controller` and `logger: level: DEBUG`.

## File Structure

```
components/mirage_m400/
├── __init__.py          # Hub component registration & config schema
├── mirage_m400.h         # Hub + switch/number/select entity class declarations
├── mirage_m400.cpp        # Hub implementation (UART TX/RX, parsing)
├── switch.py             # Power & Mute switches
├── number.py             # Volume control
├── select.py             # Source selection
└── text_sensor.py        # Raw last-response sensor
```
