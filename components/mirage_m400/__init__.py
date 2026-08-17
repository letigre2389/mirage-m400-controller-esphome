import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from .constants import *

DEPENDENCIES = ["uart"]

CONFIG_SCHEMA = cv.Schema({
    cv.Optional(CONF_MIRAGE_M400_ID): cv.GenerateID(),
    cv.Optional(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    if CONF_UART_ID in config:
        uart_id = config[CONF_UART_ID]
    else:
        uart_id = "uart_bus"

    uart_dev = cg.get_variable(cv.get_id(uart_id))
    hub = cg.new_Pvariable(cg.MirageM400Component(uart_dev))
    cg.add_component(hub)
