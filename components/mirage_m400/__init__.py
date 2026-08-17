import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import components
from esphome.components import uart

# Constants
CONF_MIRAGE_M400_ID = "mirage_m400_id"
CONF_ZONE = "zone"
CONF_TYPE = "type"
CONF_UART_ID = "uart_id"

# Switch Types: 0 = Power, 1 = Mute
SWITCH_TYPES = {
    "power": 0,
    "mute": 1,
}

DEPENDENCIES = ["uart"]

CONFIG_SCHEMA = cv.Schema({
    # FIXED: Use generate_id() instead of use_id() for the component's own ID
    cv.Optional(CONF_MIRAGE_M400_ID): cv.generate_id(),
    # Allow the user to specify which UART to use, otherwise it will look for 'uart_bus'
    cv.Optional(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    # 1. Determine which UART to use
    if CONF_UART_ID in config:
        uart_id = config[CONF_UART_ID]
    else:
        # Default to 'uart_bus' which is the ESPHome default for the first UART
        uart_id = "uart_bus"

    uart_dev = cg.get_variable(cv.get_id(uart_id))

    # 2. Create the Hub component: new MirageM400Component(uart_dev);
    hub = cg.new_Pvariable(cg.MirageM400Component(uart_dev))

    # 3. Register the component with ESPHome
    cg.add_component(hub)
