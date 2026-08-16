import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@letigre2389"]
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

CONFIG_SCHEMA = cv.COMPONENT_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Component),
        cv.GenerateID(CONF_UART_ID): cv.use_id(uart.UARTComponent),
        cv.Optional("text_sensors"): cv.ensure_list(
            cv.COMPONENT_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
                    cv.Required("name"): cv.string,
                }
            )
        ),
        cv.Optional("switches"): cv.ensure_list(
            cv.COMPONENT_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(MirageM400Switch),
                    cv.Required("name"): cv.string,
                    cv.Required("zone"): cv.int_range(min=1, max=16),
                    cv.Required("type"): cv.one_of("power", "mute"),
                }
            )
        ),
        cv.Optional("numbers"): cv.ensure_list(
            cv.COMPONENT_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(MirageM400Number),
                    cv.Required("name"): cv.string,
                    cv.Required("zone"): cv.int_range(min=1, max=16),
                    cv.Optional("min_value", default=0): cv.int_,
                    cv.Optional("max_value", default=100): cv.int_,
                    cv.Optional("step", default=1): cv.positive_int,
                }
            )
        ),
    }
)


async def to_code(config):
    # Include the header file
    cg.add_global(cg.RawExpression('#include "esphome/components/mirage_m400/mirage_m400.h"'))
    
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
            sensor_var = cg.new_variable(
                sensor_config[CONF_ID], MirageM400TextSensor
            )
            cg.add(var.register_text_sensor(sensor_var))
    
    # Process switches
    if "switches" in config:
        for switch_config in config["switches"]:
            switch_var = cg.new_variable(
                switch_config[CONF_ID], MirageM400Switch
            )
            cg.add(switch_var.set_zone(switch_config["zone"]))
            cg.add(switch_var.set_type(switch_config["type"]))
            cg.add(var.register_switch(switch_var))
    
    # Process numbers
    if "numbers" in config:
        for number_config in config["numbers"]:
            number_var = cg.new_variable(
                number_config[CONF_ID], MirageM400Number
            )
            cg.add(number_var.set_zone(number_config["zone"]))
            cg.add(number_var.set_range(
                number_config["min_value"],
                number_config["max_value"],
                number_config["step"]
            ))
            cg.add(var.register_number(number_var))
