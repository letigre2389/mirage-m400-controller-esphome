#include "mirage_m400.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mirage_m400 {

void MirageM400Component::setup() {
  ESP_LOGI(TAG, "Mirage M-400 component initialized");
}

void MirageM400Component::loop() {
  // Read responses from the amplifier
  while (this->available()) {
    uint8_t byte = this->read();
    this->response_buffer_ += (char)byte;

    // Check for end of response (carriage return or newline)
    if (byte == '\r' || byte == '\n') {
      if (this->response_buffer_.length() > 0) {
        // Remove trailing whitespace
        this->response_buffer_.erase(
            this->response_buffer_.find_last_not_of(" \n\r\t") + 1);
        
        ESP_LOGI(TAG, "Response: %s", this->response_buffer_.c_str());

        // Call all response callbacks
        for (auto &callback : this->response_callbacks_) {
          callback(this->response_buffer_);
        }

        this->response_buffer_ = "";
      }
    }
  }
}

void MirageM400Component::dump_config() {
  ESP_LOGCONFIG(TAG, "Mirage M-400:");
}

void MirageM400Component::send_command(const char *command) {
  // Add carriage return to command if not present
  std::string cmd(command);
  if (cmd.back() != '\r') {
    cmd += '\r';
  }

  this->write_str(cmd.c_str());
  ESP_LOGI(TAG, "Sent command: %s", command);

  // Add small delay to ensure transmission
  delay(50);
}

}  // namespace mirage_m400
}  // namespace esphome
