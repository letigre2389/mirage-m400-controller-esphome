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
            # The manual's own protocol examples use "zone 0" as valid, which strongly
            # suggests the wire protocol is 0-indexed while the amp's front panel / app
            # label zones starting at 1. Default offset assumes physical Zone 1 ==
            # protocol zone 0. If commands land on the wrong zone, try zone_offset: 1.
            cv.Optional(CONF_ZONE_OFFSET, default=0): cv.int_range(min=0, max=31),
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
