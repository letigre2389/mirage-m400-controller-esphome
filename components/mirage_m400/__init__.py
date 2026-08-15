import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@yourusername"]
AUTO_LOAD = ["uart"]

# Declare the namespace
mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")

# Declare all classes
MirageM400Component = mirage_m400_ns.class_(
    "MirageM400Component", cg.Component, uart.UARTDevice
)
MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", cg.Component)
MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", cg.Component)
MirageM400Number = mirage_m400_ns.class_("MirageM400Number", cg.Component)

# Configuration keys
CONF_UART_ID = "uart_id"
CONF_MIRAGE_M400_ID = "mirage_m400_id"

# Import schemas from subcomponents
from . import text_sensor as text_sensor_
from . import switch as switch_
from . import number as number_

CONFIG_SCHEMA = cv.COMPONENT_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Component),
        cv.GenerateID(CONF_UART_ID): cv.use_id(uart.UARTComponent),
        cv.Optional("text_sensors"): cv.ensure_list(text_sensor_.TEXT_SENSOR_SCHEMA),
        cv.Optional("switches"): cv.ensure_list(switch_.SWITCH_SCHEMA),
        cv.Optional("numbers"): cv.ensure_list(number_.NUMBER_SCHEMA),
    }
)


async def to_code(config):
    # Include the header file
    cg.add_includes("esphome/components/mirage_m400/mirage_m400.h")
    
    # Get the UART component
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    
    # Create the main component
    var = cg.new_variable(config[CONF_ID], MirageM400Component)
    await cg.register_component(var, config)
    
    # Set the UART parent
    cg.add(var.set_uart_parent(uart_component))
    
    # Process text sensors
    if "text_sensors" in config:
        for sensor_config in config["text_sensors"]:
            await text_sensor_.to_code(sensor_config, var)
    
    # Process switches
    if "switches" in config:
        for switch_config in config["switches"]:
            await switch_.to_code(switch_config, var)
    
    # Process numbers
    if "numbers" in config:
        for number_config in config["numbers"]:
            await number_.to_code(number_config, var)
