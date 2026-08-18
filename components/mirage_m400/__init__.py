import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from .constants import *

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["switch", "number", "text_sensor"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")

MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)
MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", cg.Component)
MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", cg.Component)
MirageM400Number = mirage_m400_ns.class_("MirageM400Number", cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400Component),
    cv.Optional(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    uart_component = await cg.get_variable(config.get(CONF_UART_ID, "uart_bus"))
    hub = cg.new_Pvariable(config[cv.CONF_ID], uart_component)
    await cg.register_component(hub, config)
    cg.add_global(cg.RawExpression('#include "mirage_m400.h"'))