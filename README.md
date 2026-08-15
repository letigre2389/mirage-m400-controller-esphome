# ESPHome Mirage M-400 Controller

Control an Autonomics Mirage M-400 amplifier via RS-232 serial communication using an ESP32 and ESPHome.

## Overview

This external component provides seamless integration between ESPHome and the Autonomics Mirage M-400 amplifier, enabling zone-based control of power, mute, volume, and other parameters through Home Assistant.

## Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Wiring](#wiring)
- [Installation](#installation)
  - [1. Add the External Component](#1-add-the-external-component)
  - [2. Configure UART](#2-configure-uart)
  - [3. Initialize the Component](#3-initialize-the-component)
- [Usage](#usage)
  - [Switches (Power & Mute)](#switches-power--mute)
  - [Numbers (Volume Control)](#numbers-volume-control)
  - [Text Sensors (Status Response)](#text-sensors-status-response)
  - [Home Assistant Service](#home-assistant-service)
- [Command Format](#command-format)
- [Supported Zones](#supported-zones)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Hardware Requirements

| Component | Details |
| :--- | :--- |
| Microcontroller | ESP32 (e.g., ESP32-DevKitC-v1) |
| RS-232 Converter | MAX3232 TTL ↔ RS-232 level shifter |
| Cable | DB9 straight-through (or custom) |
| GPIO Pins | TX: GPIO16, RX: GPIO17 |

## Wiring

Connect the MAX3232 converter between the ESP32 and Mirage M-400:

- **ESP32 TX (GPIO16)** → **MAX3232 R1IN**
- **ESP32 RX (GPIO17)** → **MAX3232 T1OUT**
- **MAX3232 T1IN** → **Mirage M-400 RX (DB9 pin 2)**
- **MAX3232 R1OUT** → **Mirage M-400 TX (DB9 pin 3)**
- **GND** → **GND** (both sides)

## Installation

### 1. Add the External Component

In your ESPHome YAML configuration:

```yaml
external_components:
  - source: github://yourusername/esphome-mirage-m400
    components: [mirage_m400]
```

Or for local development:

```yaml
external_components:
  - source: local
    path: /path/to/esphome-mirage-m400
    components: [mirage_m400]
```

### 2. Configure UART

```yaml
uart:
  - id: mirage_uart
    tx_pin: GPIO16
    rx_pin: GPIO17
    baud_rate: 9600
    data_bits: 8
    parity: NONE
    stop_bits: 1
```

### 3. Initialize the Component

```yaml
mirage_m400:
  uart_id: mirage_uart
  id: mirage_m400_device
```

## Usage

### Switches (Power & Mute)

```yaml
switch:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Power"
    type: power
    zone: 1

  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 2 Mute"
    type: mute
    zone: 2
```

### Numbers (Volume Control)

```yaml
number:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Zone 1 Volume"
    zone: 1
    min_value: 0
    max_value: 100
    step: 1
    unit_of_measurement: "%"
```

### Text Sensors (Status Response)

```yaml
text_sensor:
  - platform: mirage_m400
    mirage_m400_id: mirage_m400_device
    name: "Mirage M-400 Status"
```

### Home Assistant Service

Send raw commands directly to the amplifier from your ESPHome configuration:

```yaml
api:
  services:
    - service: send_mirage_command
      variables:
        command: string
      then:
        - lambda: |-
            id(mirage_m400_device)->send_command(command.c_str());
            ESP_LOGI("mirage_service", "Sent command: %s", command.c_str());
```

Call it from Home Assistant:

```yaml
service: esphome.mirage_m400_controller_send_mirage_command
data:
  command: "010A01"  # Zone 10 Power ON
```

## Command Format

Commands follow the structure: `<command><zone><data>`

| Function | Command | Zone | Data | Example |
| :--- | :--- | :--- | :--- | :--- |
| Power | `01` | Zone (01–16, 0A–0F hex) | `00`=OFF, `01`=ON | `010A01` = Zone 10 ON |
| Mute | `02` | Zone | `00`=Mute, `01`=Un-mute | `020301` = Zone 3 Un-mute |
| Source | `03` | Zone | Source ID | `030301` = Zone 3, Source 3 |
| Volume | `0401` | Zone | 00–64 (0–100%) | `04010132` = Zone 1, 50% volume |
| Treble | `05` | Zone | 00–0C (±6dB) | `050106` = Zone 1, +3dB |
| Query Status | `FF` | Zone | `00` | `FF0100` = Query Zone 1 |

All commands end with a carriage return (`\r`).

## Supported Zones

Zones 1–16 are supported via the `zone` parameter in switches, numbers, and text sensors.

## File Structure

```text
esphome-mirage-m400/
├── components/mirage_m400/
│   ├── __init__.py          # Component registration & namespace
│   ├── mirage_m400.h        # C++ header
│   ├── mirage_m400.cpp      # Main component logic
│   ├── switch.py            # Power & Mute switches
│   ├── number.py            # Volume control
│   └── text_sensor.py       # Status responses
└── README.md
```

## Troubleshooting

### Component Not Loading

Ensure the external component path is correct and all Python files are present.

### No Serial Communication

- Verify UART GPIO pins (`TX=GPIO16`, `RX=GPIO17`).
- Check MAX3232 wiring and power supply.
- Confirm baud rate is set to `9600`.
- Monitor logs using the ESPHome CLI: `esphome logs mirage-m400-controller`.

### Conflicting ID Names

Avoid using `mirage_m400` as the component ID; use `mirage_m400_device` instead.
