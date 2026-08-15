import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNER = ["@yourusername"]
DEPENDENCIES = ["uart"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)

CONF_UART_ID = "uart_id"
CONF_MIRAGE_M400_ID = "mirage_m400_id"

CONFIG_SCHEMA = (
    cv.COMPONENT_SCHEMA.extend(uart.UART_DEVICE_SCHEMA).extend(
        {
            cv.GenerateID(): cv.declare_id(MirageM400Component),
        }
    )
)

async def to_code(config):
    uart_component = await cg.get_variable(config[uart.CONF_UART_ID])
    var = cg.new_variable(config[CONF_ID], MirageM400Component)
    cg.add(var.set_uart_parent(uart_component))
    cg.add(cg.register_component(var, config))
