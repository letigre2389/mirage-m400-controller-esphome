import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_NAME

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", cg.Component)

CONF_TYPE = "type"
CONF_ZONE = "zone"

SWITCH_SCHEMA = switch.SWITCH_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Switch),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required(CONF_TYPE): cv.one_of("power", "mute"),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
    }
)

async def to_code(config):
    var = cg.new_variable(config[CONF_ID], MirageM400Switch)
    await cg.register_component(var, config)
    
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    cg.add(parent.register_switch(var))
    
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
    
    # Map type string to integer
    type_value = 0 if config[CONF_TYPE] == "power" else 1
    cg.add(var.set_type(cg.int(type_value)))
    
    await switch.register_switch(var, config)
