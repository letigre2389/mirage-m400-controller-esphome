# ESPHome Mirage M-400 Controller

Control an Autonomic Mirage M-400 amplifier via RS-232 serial communication using an ESP32 and ESPHome.

This is a rewrite based on the actual protocol documented in the Autonomic M-400 manual
("Ethernet / RS232 Protocol" section), which differs from earlier assumptions in this
project in a few important ways — see **What Changed** below if you're migrating from
the previous version.

## Hardware Requirements

| Component        | Details                            |
| ----------------- | ---------------------------------- |
| Microcontroller   | ESP32 (e.g., ESP32 DevKit V1 / WROOM-32) |
| RS-232 Converter  | MAX3232 TTL ↔ RS-232 level shifter |
| Cable             | DB9 straight-through (per manual)  |
| GPIO Pins         | TX: GPIO17 (`TX2`), RX: GPIO16 (`RX2`) |

## Wiring

On a MAX3232, `T1IN`/`T1OUT` is the **transmit** channel (TTL in → RS-232 out) and
`R1IN`/`R1OUT` is the **receive** channel (RS-232 in → TTL out). Wire it as:

- **ESP32 TX (GPIO17, silkscreen `TX2`)** → **MAX3232 T1IN**
- **MAX3232 T1OUT** → **Mirage M-400 RX (DB9 pin 3)**
- **Mirage M-400 TX (DB9 pin 2)** → **MAX3232 R1IN**
- **MAX3232 R1OUT** → **ESP32 RX (GPIO16, silkscreen `RX2`)**
- **ESP32 3V3** → **converter VCC** (3.3V, not 5V — ESP32 GPIO is not 5V tolerant)
- **GND** → **GND** (both sides)

On a breakout board with only `VCC` / `GND` / `TXD` / `RXD` broken out, `TXD`/`RXD` are
named from the module's perspective, so cross them: ESP32 TX (GPIO17) → module `RXD`,
module `TXD` → ESP32 RX (GPIO16).

### DB9 pin directions

The M-400's rear panel port is a **DB9 female**, and the manual requires a
**straight-through** cable to a PC. A PC is DTE and drives pin 3, so the amp must be
wired DCE: **pin 3 is the amp's receive input, pin 2 is its transmit output**, pin 5 is
ground. Those are the only three pins that carry anything.

> An earlier version of this README had these reversed (amp RX on pin 2, TX on pin 3).
> If your converter board also presents a female DB9, note that female breakouts are
> often wired DCE like the amp — check the schematic on the back of the board, and if
> you see no response, swap pins 2 and 3 with a null-modem adapter. Miswiring TX to TX
> won't damage anything; RS-232 drivers are short-circuit protected.

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
    tx_pin: GPIO17
    rx_pin: GPIO16
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
  command: "010A01"   # power zone 0x0A ON (see Standby note below)
```

## Command Format

`<command><zone><data>`, sent as ASCII hex characters, terminated with a line feed.

| Function      | Command | Data                                                   |
| ------------- | ------- | ------------------------------------------------------- |
| Standby       | `01`    | `00`=zone OFF, `01`=zone ON, `04`=Toggle (see note)     |
| Mute          | `02`    | `00`=Mute, `01`=Un-mute, `02`=Toggle                    |
| Source Select | `03`    | `00`=S5 `01`=S6 `02`=S7 `03`=S4 `04`=S8 `05`=S1 `06`=S2 `07`=S3 |
| Volume        | `04`    | `00`–`A0` (0–160 decimal)                                |
| Bass          | `05`    | `F4`–`0C` (-12dB to +12dB)                                |
| Treble        | `06`    | `F4`–`0C` (-12dB to +12dB)                                |
| Balance       | `07`    | `EC`–`14` (Left -20dB to Right -20dB)                     |
| Send All Parameters | `09` | value ignored — triggers a full status dump (>144 bytes) |

> **Standby polarity:** the manual's table lists `00` as "Standby OFF" (zone on) and
> `01` as "Standby ON" (zone off). A real M-400 does the opposite — it reports `00`
> for a zone that is powered off — so this project treats the byte as a plain power
> state: `00` = off, `01` = on, in both directions. If your amp's firmware follows the
> manual instead, flip both `on_mirage_update` and `write_state` in
> `MirageStandbySwitch` together; changing only one gives you a switch whose state
> display disagrees with what it commands.

### Zone byte

The zone byte's lower 5 bits encode the zone (0–31); `FF` addresses all zones. The
manual's own examples use **zone 0** as valid (e.g. "Zone 10 = hex 0A" implies zones
count from 0), which suggests the wire protocol is 0-indexed even though the front
panel and web app label zones starting at 1.

## Zone Addressing

`zone_offset` (default `1`) controls the mapping from the zone numbers you use in your
YAML (1, 2, 3, 4 — matching the amp's labeling) to the protocol's zone byte:
`protocol_zone = physical_zone - 1 + zone_offset`.

**The default of `1` is confirmed against real hardware**: the zone byte is 1-indexed
and matches the amp's own labels, so `zone: 1` in your YAML controls Zone 1. The
manual's examples suggest 0-indexing, but with `zone_offset: 0` every entity lands one
zone low — YAML Zone 2 drives amp Zone 1, YAML Zone 3 drives Zone 2, and YAML Zone 1
addresses a zone 0 that doesn't exist (so it appears to do nothing).

If yours behaves differently, turn on the Last Response text sensor with
`logger: level: DEBUG`, toggle Zone 1's power switch, and check which zone reacts.

### Adding more zones

The M-400 has four zones. To control more, stack amplifiers with the RJ45 expansion bus
— the whole stack is addressed over the one RS-232 connection, and the zone byte's lower
5 bits cover zones 0–31. To add them:

1. Add `switch` / `number` / `select` entries to your YAML with the new zone numbers.
2. Raise `zone_count` to the highest zone number you use, so the status poller covers
   them (it round-robins physical zones `1..zone_count`, one per `poll_interval`).
3. Reinstall.

No code or wiring changes are needed.

## What Changed (vs. the earlier version of this project)

These came directly out of reading the manual's protocol appendix and are the most
likely causes of "the ESP32 sends something but the amp doesn't do the right thing":

1. **Standby polarity.** The manual says `00` = Standby OFF (zone *on*) and `01` =
   Standby ON (zone *off*), and an earlier revision of this project followed it.
   Testing on a real M-400 showed the amp reports `00` for a zone that is powered
   off, which made Home Assistant display every power switch backwards, so the byte
   is now treated as a plain power state (`00` = off, `01` = on) in both directions.
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
6. **Wiring**: TX/RX were mapped to the wrong MAX3232 channels, and the DB9 pin
   directions were reversed — see Wiring above.

## Troubleshooting

- **Nothing happens at all**: verify wiring per the corrected diagram above, and
  confirm baud rate (9600 8N1).
- **Commands seem to hit the wrong zone**: try flipping `zone_offset` between `1`
  (default, matches the amp's labels) and `0`. Every entity landing one zone low is
  the classic symptom of `zone_offset: 0`.
- **Power toggles show backwards**: the Standby byte is treated as `00` = off,
  `01` = on, matching observed hardware. If yours is inverted, flip both
  `on_mirage_update` and `write_state` in `MirageStandbySwitch` together.
- **Mute toggles backwards**: mute still follows the manual (`00` = Mute,
  `01` = Un-mute). Since Standby turned out to be documented backwards, mute may be
  too — watch the Last Response sensor with a zone known to be unmuted to confirm.
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
