import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from .constants import *

DEPENDENCIES = ["mirage_m400"]

mirage_m400_ns = cg.esphome_ns.namespace("mirage_m400")
MirageM400Switch = mirage_m400_ns.class_(
    "MirageM400Switch", switch.Switch, cg.Component
)

CONFIG_SCHEMA = switch.switch_schema(MirageM400Switch).extend({
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(mirage_m400_ns.class_("MirageM400Component")),
    cv.Required(CONF_ZONE): cv.int_range(min=1, max=17),
    cv.Required(CONF_TYPE): cv.enum(SWITCH_TYPES),
})


async def to_code(config):
    hub = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[cv.CONF_ID], hub)
    await switch.register_switch(var, config)