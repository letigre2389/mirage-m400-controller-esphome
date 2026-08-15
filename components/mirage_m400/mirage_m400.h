#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/number/number.h"
#include <string>
#include <queue>

namespace esphome {
namespace mirage_m400 {

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component() = default;

  void setup() override;
  void loop() override;
  void send_command(const std::string &command);
  void register_number(class MirageM400Number *number_entity, uint8_t zone);
  std::string last_response;

 private:
  std::queue<std::string> response_buffer_;
  std::string current_response_;
  std::vector<class MirageM400Number *> numbers_;
};

class MirageM400Number : public number::Number, public Component {
 public:
  void set_parent(MirageM400Component *parent) { parent_ = parent; }
  void set_zone(uint8_t zone) { zone_ = zone; }

 protected:
  void control(float value) override;
  MirageM400Component *parent_;
  uint8_t zone_;
};

}  // namespace mirage_m400
}  // namespace esphome
#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/number/number.h"
#include <string>
#include <queue>

namespace esphome {
namespace mirage_m400 {

// Forward declaration
class MirageM400Number;

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component() = default;

  void setup() override;
  void loop() override;
  void send_command(const std::string &command);
  void register_number(MirageM400Number *number_entity, uint8_t zone);
  std::string last_response;

 private:
  std::queue<std::string> response_buffer_;
  std::string current_response_;
  std::vector<MirageM400Number *> numbers_;
};

class MirageM400Number : public number::Number, public Component {
 public:
  void set_parent(MirageM400Component *parent) { parent_ = parent; }
  void set_zone(uint8_t zone) { zone_ = zone; }

 protected:
  void control(float value) override;
  MirageM400Component *parent_;
  uint8_t zone_;
};

}  // namespace mirage_m400
}  // namespace esphome
