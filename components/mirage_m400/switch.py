import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from . import mirage_m400_ns, MirageM400Component
from .constants import *

DEPENDENCIES = ["mirage_m400"]

MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", switch.Switch)

CONFIG_SCHEMA = switch.SWITCH_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(MirageM400Switch),
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    cv.Required(CONF_ZONE): cv.int_range(1, 17),
    cv.Required(CONF_TYPE): cv.enum(SWITCH_TYPES),
    cv.GenerateID(): cv.declare_id(MirageM400Switch),
    cv.Required(cv.CONF_NAME): cv.string,
})


async def to_code(config):
    hub = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(
        config[cv.GenerateID()],
        config[cv.CONF_NAME],
        cg.RawExpression(f"(uint8_t){config[CONF_ZONE]}"),
        cg.RawExpression(f"(uint8_t){SWITCH_TYPES[config[CONF_TYPE]]}"),
    )
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    cg.add(hub.register_switch(var))