import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import components

# Constants
CONF_MIRAGE_M400_ID = "mirage_m400_id"
CONF_ZONE = "zone"
CONF_TYPE = "type"

# Switch Types: 0 = Power, 1 = Mute
SWITCH_TYPES = {
    "power": 0,
    "mute": 1,
}

DEPENDENCIES = ["uart"]

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    # Get the UART component
    uart = cg.get_variable(cv.get_id("uart_id")) # Default UART ID

    # Create the Hub component: new MirageM400Component(uart);
    hub = cg.new_Pvariable(cg.MirageM400Component(uart))
    cg.add_expression(" %s->set_id(%s);" % (hub, cv.get_id(config[CONF_MIRAGE_M400_ID])))

    cg.add_component(hub)
    
