import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

MirageM400Number = mirage_m400_ns.class_("MirageM400Number", cg.Component)

CONF_ZONE = "zone"

NUMBER_SCHEMA = number.NUMBER_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400Number),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_variable(config[CONF_ID], MirageM400Number)
    await cg.register_component(var, config)
    
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    cg.add(parent.register_number(var))
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
    
    await number.register_number(var, config)
