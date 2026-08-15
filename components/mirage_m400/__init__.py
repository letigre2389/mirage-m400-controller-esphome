import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@your_username"]
DEPENDENCIES = ["uart"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)
MirageM400Number = mirage_m400_ns.class_("MirageM400Number", cg.Component)
MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", cg.Component)
MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", cg.Component)

CONF_MIRAGE_M400_ID = "mirage_m400_id"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Component),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    }
).extend(uart.UART_DEVICE_SCHEMA)


async def to_code(config):
    uart_component = await cg.get_variable(config[uart.CONF_UART_ID])
    var = cg.new_variable(config[cv.GenerateID()], MirageM400Component())
    await cg.register_component(var, config)
    cg.add(var.set_uart_parent(uart_component))
