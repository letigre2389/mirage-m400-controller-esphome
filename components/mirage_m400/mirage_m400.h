#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"
#include "esphome/components/select/select.h"

#include <vector>
#include <string>
#include <cstdio>
#include <cstdlib>

namespace esphome {
namespace mirage_m400 {

// RS232 command bytes, from the Autonomic M-400 manual's
// "Ethernet / RS232 Protocol" section. Command structure is:
//   <command (1 byte hex)><zone (1 byte hex)><data (1 byte hex)><line feed>
// all sent as ASCII hex characters (e.g. sending 0x01 is the two ASCII
// characters '0' and '1', NOT the raw byte 0x01).
enum class MirageCommand : uint8_t {
  STANDBY = 0x01,
  MUTE = 0x02,
  SOURCE = 0x03,
  VOLUME = 0x04,
  BASS = 0x05,
  TREBLE = 0x06,
  BALANCE = 0x07,
  SEND_ALL = 0x09,
  REQUEST_INFO = 0x14,
};

// Source data-byte mapping is NOT sequential in the amp's protocol (per manual):
//   S1=0x05  S2=0x06  S3=0x07  S4=0x03  S5=0x00  S6=0x01  S7=0x02  S8=0x04
static const uint8_t MIRAGE_SOURCE_DATA[8] = {0x05, 0x06, 0x07, 0x03, 0x00, 0x01, 0x02, 0x04};

class MirageM400Listener {
 public:
  virtual ~MirageM400Listener() = default;
  virtual uint8_t get_zone() const = 0;
  virtual MirageCommand get_command() const = 0;
  virtual void on_mirage_update(uint8_t data) = 0;
};

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;

  void set_zone_offset(uint8_t offset) { this->zone_offset_ = offset; }
  void set_zone_count(uint8_t count) { this->zone_count_ = count; }
  void set_poll_interval(uint32_t ms) { this->poll_interval_ = ms; }
  void set_last_response_text_sensor(text_sensor::TextSensor *s) { this->last_response_sensor_ = s; }

  void register_listener(MirageM400Listener *listener) { this->listeners_.push_back(listener); }

  // Build and send <command><zone><data> for a 1-based physical zone number.
  void send_command(uint8_t command, uint8_t physical_zone, uint8_t data);
  // Send an already hex-formatted command string, e.g. "010A01" (used by the
  // send_mirage_command Home Assistant service for raw/manual commands).
  void send_raw_command(const std::string &command);
  // Ask the amp to report all current parameters for a zone (command 0x09).
  void request_zone_status(uint8_t physical_zone);

 protected:
  uint8_t to_protocol_zone_(uint8_t physical_zone) const {
    return (uint8_t) (physical_zone - 1 + this->zone_offset_);
  }
  uint8_t to_physical_zone_(uint8_t protocol_zone) const {
    return (uint8_t) (protocol_zone + 1 - this->zone_offset_);
  }
  void process_line_(const std::string &line);
  void handle_triplet_(uint8_t command, uint8_t zone_byte, uint8_t data);
  static bool hex_byte_(const std::string &s, size_t pos, uint8_t *out);

  std::string rx_buffer_;
  std::vector<MirageM400Listener *> listeners_;
  text_sensor::TextSensor *last_response_sensor_{nullptr};

  uint8_t zone_offset_{0};
  uint8_t zone_count_{4};
  uint32_t poll_interval_{15000};
  uint32_t last_poll_{0};
  uint8_t poll_index_{0};
};

// ---------------------------------------------------------------------------
// Switch entities: Power (Standby) and Mute
// ---------------------------------------------------------------------------

class MirageSwitch : public switch_::Switch, public Component, public MirageM400Listener {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_zone(uint8_t zone) { this->zone_ = zone; }
  void setup() override { this->parent_->register_listener(this); }
  uint8_t get_zone() const override { return this->zone_; }

 protected:
  MirageM400Component *parent_{nullptr};
  uint8_t zone_{1};
};

class MirageStandbySwitch : public MirageSwitch {
 public:
  MirageCommand get_command() const override { return MirageCommand::STANDBY; }

  // Standby data per the manual: 0x00 = Standby OFF (zone playing/powered on),
  // 0x01 = Standby ON (zone powered off). This is the OPPOSITE of a naive
  // "0=off, 1=on" power switch, and inverting it is the most likely reason
  // your power switches weren't behaving.
  void on_mirage_update(uint8_t data) override { this->publish_state(data == 0x00); }

 protected:
  void write_state(bool state) override {
    uint8_t data = state ? 0x00 : 0x01;
    this->parent_->send_command((uint8_t) MirageCommand::STANDBY, this->zone_, data);
    this->publish_state(state);
  }
};

class MirageMuteSwitch : public MirageSwitch {
 public:
  MirageCommand get_command() const override { return MirageCommand::MUTE; }

  // Mute data: 0x00 = Mute, 0x01 = Un-mute
  void on_mirage_update(uint8_t data) override { this->publish_state(data == 0x00); }

 protected:
  void write_state(bool state) override {
    uint8_t data = state ? 0x00 : 0x01;
    this->parent_->send_command((uint8_t) MirageCommand::MUTE, this->zone_, data);
    this->publish_state(state);
  }
};

// ---------------------------------------------------------------------------
// Number entity: Volume. The manual specifies a raw protocol range of
// 0x00-0xA0 (0-160 decimal), NOT 0-100/percent.
// ---------------------------------------------------------------------------

class MirageVolumeNumber : public number::Number, public Component, public MirageM400Listener {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_zone(uint8_t zone) { this->zone_ = zone; }
  void setup() override { this->parent_->register_listener(this); }

  uint8_t get_zone() const override { return this->zone_; }
  MirageCommand get_command() const override { return MirageCommand::VOLUME; }

  void on_mirage_update(uint8_t data) override { this->publish_state((float) data); }

 protected:
  void control(float value) override {
    uint8_t data = (uint8_t) value;
    this->parent_->send_command((uint8_t) MirageCommand::VOLUME, this->zone_, data);
    this->publish_state(value);
  }

  MirageM400Component *parent_{nullptr};
  uint8_t zone_{1};
};

// ---------------------------------------------------------------------------
// Select entity: Source (S1-S8). Uses the amp's non-sequential data bytes,
// see MIRAGE_SOURCE_DATA above.
// ---------------------------------------------------------------------------

class MirageSourceSelect : public select::Select, public Component, public MirageM400Listener {
 public:
  void set_parent(MirageM400Component *parent) { this->parent_ = parent; }
  void set_zone(uint8_t zone) { this->zone_ = zone; }
  void setup() override { this->parent_->register_listener(this); }

  uint8_t get_zone() const override { return this->zone_; }
  MirageCommand get_command() const override { return MirageCommand::SOURCE; }

  void on_mirage_update(uint8_t data) override {
    for (uint8_t i = 0; i < 8; i++) {
      if (MIRAGE_SOURCE_DATA[i] == data) {
        char buf[4];
        snprintf(buf, sizeof(buf), "S%u", (unsigned) (i + 1));
        this->publish_state(std::string(buf));
        return;
      }
    }
  }

 protected:
  void control(const std::string &value) override {
    if (value.size() < 2 || value[0] != 'S')
      return;
    int idx = atoi(value.c_str() + 1) - 1;
    if (idx < 0 || idx > 7)
      return;
    uint8_t data = MIRAGE_SOURCE_DATA[idx];
    this->parent_->send_command((uint8_t) MirageCommand::SOURCE, this->zone_, data);
    this->publish_state(value);
  }

  MirageM400Component *parent_{nullptr};
  uint8_t zone_{1};
};

}  // namespace mirage_m400
}  // namespace esphome
