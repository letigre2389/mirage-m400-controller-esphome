import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@letigre2389"]
DEPENDENCIES = ["uart", "text_sensor", "switch", "number"]
AUTO_LOAD = ["uart", "text_sensor", "switch", "number"]

CONF_MIRAGE_M400 = "mirage_m400"
CONF_MIRAGE_M400_ID = "mirage_m400_id"

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)

CONF_TEXT_SENSORS = "text_sensors"
CONF_SWITCHES = "switches"
CONF_NUMBERS = "numbers"

TEXT_SENSOR_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(cg.MockObj),
        cv.Required(cv.string): cv.string,
    }
)

SWITCH_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(cg.MockObj),
        cv.Required(cv.string): cv.string,
        cv.Required("zone"): cv.int_range(min=1, max=16),
        cv.Required("type"): cv.enum({"power": 0, "mute": 1}),
    }
)

NUMBER_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(cg.MockObj),
        cv.Required(cv.string): cv.string,
        cv.Required("zone"): cv.int_range(min=1, max=16),
        cv.Optional("min_value", default=0): cv.float_,
        cv.Optional("max_value", default=100): cv.float_,
        cv.Optional("step", default=1): cv.float_,
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(MirageM400Component),
        cv.Optional(CONF_TEXT_SENSORS): cv.ensure_list(TEXT_SENSOR_SCHEMA),
        cv.Optional(CONF_SWITCHES): cv.ensure_list(SWITCH_SCHEMA),
        cv.Optional(CONF_NUMBERS): cv.ensure_list(NUMBER_SCHEMA),
    }
).extend(uart.UART_DEVICE_SCHEMA)


async def to_code(config):
    cg.add_global(cg.RawExpression('#include "esphome/components/mirage_m400/mirage_m400.h"'))
    
    uart_component = await cg.get_variable(config[uart.CONF_UART_ID])
    var = cg.new_Pvariable(config[CONF_ID], uart_component)
    await cg.register_component(var, config)
    
    if CONF_TEXT_SENSORS in config:
        for conf in config[CONF_TEXT_SENSORS]:
            var_id = conf[CONF_ID]
            cg.variable(cg.MockObj, var_id)
    
    if CONF_SWITCHES in config:
        for conf in config[CONF_SWITCHES]:
            var_id = conf[CONF_ID]
            cg.variable(cg.MockObj, var_id)
    
    if CONF_NUMBERS in config:
        for conf in config[CONF_NUMBERS]:
            var_id = conf[CONF_ID]
            cg.variable(cg.MockObj, var_id)
