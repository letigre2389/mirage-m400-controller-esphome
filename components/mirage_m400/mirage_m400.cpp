#include "mirage_m400.h"
#include "esphome/core/log.h"
#include <cctype>
#include <cstdlib>

namespace esphome {
namespace mirage_m400 {

static const char *const TAG = "mirage_m400";

void MirageM400Component::setup() { this->last_poll_ = millis(); }

void MirageM400Component::dump_config() {
  ESP_LOGCONFIG(TAG, "Mirage M-400:");
  ESP_LOGCONFIG(TAG, "  Zone offset: %u", this->zone_offset_);
  ESP_LOGCONFIG(TAG, "  Zone count: %u", this->zone_count_);
  ESP_LOGCONFIG(TAG, "  Poll interval: %u ms", (unsigned) this->poll_interval_);
}

void MirageM400Component::send_command(uint8_t command, uint8_t physical_zone, uint8_t data) {
  uint8_t zone_byte = this->to_protocol_zone_(physical_zone);
  char buf[7];
  snprintf(buf, sizeof(buf), "%02X%02X%02X", command, zone_byte, data);
  this->send_raw_command(std::string(buf));
}

void MirageM400Component::send_raw_command(const std::string &command) {
  ESP_LOGD(TAG, "TX: %s", command.c_str());
  this->write_str(command.c_str());
  // Manual's command structure ends with <line feed>.
  this->write_byte(0x0A);
}

void MirageM400Component::request_zone_status(uint8_t physical_zone) {
  this->send_command((uint8_t) MirageCommand::SEND_ALL, physical_zone, 0x00);
}

void MirageM400Component::loop() {
  while (this->available()) {
    uint8_t c;
    if (!this->read_byte(&c))
      break;
    if (c == '\r' || c == '\n') {
      if (!this->rx_buffer_.empty()) {
        this->process_line_(this->rx_buffer_);
        this->rx_buffer_.clear();
      }
    } else if (std::isprint(c)) {
      this->rx_buffer_ += (char) c;
      if (this->rx_buffer_.size() > 512) {
        ESP_LOGW(TAG, "RX buffer overflow, discarding");
        this->rx_buffer_.clear();
      }
    }
  }

  if (this->zone_count_ > 0) {
    uint32_t now = millis();
    if (now - this->last_poll_ >= this->poll_interval_) {
      this->last_poll_ = now;
      uint8_t physical_zone = this->poll_index_ + 1;
      this->request_zone_status(physical_zone);
      this->poll_index_ = (uint8_t) ((this->poll_index_ + 1) % this->zone_count_);
    }
  }
}

bool MirageM400Component::hex_byte_(const std::string &s, size_t pos, uint8_t *out) {
  if (pos + 2 > s.size())
    return false;
  char buf[3] = {s[pos], s[pos + 1], '\0'};
  if (!std::isxdigit((unsigned char) buf[0]) || !std::isxdigit((unsigned char) buf[1]))
    return false;
  *out = (uint8_t) strtol(buf, nullptr, 16);
  return true;
}

void MirageM400Component::process_line_(const std::string &line) {
  ESP_LOGD(TAG, "RX: %s", line.c_str());
  if (this->last_response_sensor_ != nullptr) {
    this->last_response_sensor_->publish_state(line);
  }

  // Treat the line as a sequence of back-to-back <cmd><zone><data> hex triplets.
  // A single-command echo is exactly one triplet; the "Send All Parameters" (09)
  // reply is documented as containing the same command fields concatenated
  // together, so scanning in fixed 6-character chunks picks up both cases.
  //
  // NOTE: if real captures show extra framing/header bytes before the first
  // triplet, adjust the starting offset here accordingly -- turn on DEBUG
  // logging (logger: level: DEBUG) and watch the "RX:" lines to check.
  for (size_t i = 0; i + 6 <= line.size(); i += 6) {
    uint8_t command, zone_byte, data;
    if (!hex_byte_(line, i, &command))
      continue;
    if (!hex_byte_(line, i + 2, &zone_byte))
      continue;
    if (!hex_byte_(line, i + 4, &data))
      continue;
    this->handle_triplet_(command, zone_byte, data);
  }
}

void MirageM400Component::handle_triplet_(uint8_t command, uint8_t zone_byte, uint8_t data) {
  uint8_t protocol_zone = zone_byte & 0x1F;
  uint8_t physical_zone = this->to_physical_zone_(protocol_zone);
  for (auto *listener : this->listeners_) {
    if (listener->get_zone() == physical_zone && (uint8_t) listener->get_command() == command) {
      listener->on_mirage_update(data);
    }
  }
}

}  // namespace mirage_m400
}  // namespace esphome
