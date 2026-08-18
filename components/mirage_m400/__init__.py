import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from .constants import *

DEPENDENCIES = ["uart"]

CONFIG_SCHEMA = cv.Schema({
    cv.Optional(CONF_MIRAGE_M400_ID): cv.string,
    cv.Optional(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    uart_id = config.get(CONF_UART_ID, "uart_bus")
    uart_dev = cg.get_variable(cv.get_id(uart_id))
    
    hub = cg.new_Pvariable(cg.MirageM400Component)
    cg.add_expression(" %s = new MirageM400Component(%s);" % (hub, uart_dev))
    cg.add_component(hub)