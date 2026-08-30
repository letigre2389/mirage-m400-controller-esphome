import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@letigre2389"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["switch", "number", "select", "text_sensor"]
MULTI_CONF = True

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_(
    "MirageM400Component", cg.Component, uart.UARTDevice
)

# Shared config keys used by the switch/number/select/text_sensor platforms.
CONF_MIRAGE_M400_ID = "mirage_m400_id"
CONF_ZONE_OFFSET = "zone_offset"
CONF_ZONE_COUNT = "zone_count"
CONF_POLL_INTERVAL = "poll_interval"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(MirageM400Component),
            # protocol_zone = physical_zone - 1 + zone_offset. Confirmed on real
            # hardware: the wire protocol is 1-indexed and matches the amp's own zone
            # labels, so the default offset of 1 makes YAML "zone: 1" address Zone 1.
            # (The manual's examples hinted at 0-indexing; the hardware disagrees.)
            cv.Optional(CONF_ZONE_OFFSET, default=1): cv.int_range(min=0, max=31),
            cv.Optional(CONF_ZONE_COUNT, default=4): cv.int_range(min=1, max=32),
            cv.Optional(
                CONF_POLL_INTERVAL, default="15s"
            ): cv.positive_time_period_milliseconds,
        }
    )
    .extend(uart.UART_DEVICE_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    cg.add(var.set_zone_offset(config[CONF_ZONE_OFFSET]))
    cg.add(var.set_zone_count(config[CONF_ZONE_COUNT]))
    cg.add(var.set_poll_interval(config[CONF_POLL_INTERVAL]))
