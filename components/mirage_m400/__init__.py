import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@yourusername"]
AUTO_LOAD = ["uart"]

# Declare the namespace and component
mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)

CONF_UART_ID = "uart_id"
CONF_MIRAGE_M400_ID = "mirage_m400_id"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400Component),
    cv.GenerateID(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    # Add include BEFORE any class usage
    cg.add_includes("esphome/components/mirage_m400/mirage_m400.h")
    
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    
    var = cg.new_variable(config[CONF_ID], MirageM400Component)
    await cg.register_component(var, config)
    
    cg.add(var.set_uart_parent(uart_component))
