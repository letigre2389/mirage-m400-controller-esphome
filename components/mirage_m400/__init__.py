import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@yourusername"]
AUTO_LOAD = ["uart"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Component = mirage_m400_ns.class_("MirageM400Component", cg.Component, uart.UARTDevice)
MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", cg.Component)
MirageM400Number = mirage_m400_ns.class_("MirageM400Number", cg.Component)
MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", cg.Component)

CONF_MIRAGE_M400_ID = "mirage_m400_id"

MIRAGE_M400_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400Component),
    cv.GenerateID(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MirageM400Component),
    cv.GenerateID(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    cg.add_includes("esphome/components/mirage_m400/mirage_m400.h")
    cg.add_define("MIRAGE_M400_COMPONENT")
    
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    
    var = cg.new_variable(config[CONF_ID], MirageM400Component)
    await cg.register_component(var, config)
    
    cg.add_global_ns(f"using mirage_m400_component_t = esphome::mirage_m400::MirageM400Component;")
    
    cg.add(var.set_uart_parent(uart_component))
