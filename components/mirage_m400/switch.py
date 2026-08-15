import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_TYPE

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

DEPENDENCIES = ["mirage_m400"]

CONF_ZONE = "zone"
CONF_POWER = "power"
CONF_MUTE = "mute"

MirageM400Switch = mirage_m400_ns.class_("MirageM400Switch", switch.Switch)

SWITCH_TYPES = {
    CONF_POWER: MirageM400Switch,
    CONF_MUTE: MirageM400Switch,
}

CONFIG_SCHEMA = switch.switch_schema(MirageM400Switch).extend(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.enum(SWITCH_TYPES, lower=True),
    }
)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = await switch.new_switch(config)
    cg.add(parent.register_switch(var))
    cg.add(var.set_zone(config[CONF_ZONE]))
    cg.add(var.set_type(config[CONF_TYPE]))
