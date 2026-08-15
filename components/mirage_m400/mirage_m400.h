#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mirage_m400 {

static const char *const TAG = "mirage_m400";

class MirageM400Component : public Component, public uart::UARTDevice {
 public:
  MirageM400Component(uart::UARTComponent *parent) : uart::UARTDevice(parent) {}

  void setup() override;
  void loop() override;
  void dump_config() override;

  void send_command(const char *command);

  // Callbacks for response data
  using response_callback_t = std::function<void(const std::string &)>;
  void add_response_callback(response_callback_t callback) {
    this->response_callbacks_.push_back(callback);
  }

 protected:
  std::vector<response_callback_t> response_callbacks_;
  std::string response_buffer_;
};

}  // namespace mirage_m400
}  // namespace esphome
