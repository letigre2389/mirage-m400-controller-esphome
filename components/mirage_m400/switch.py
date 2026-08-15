import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ICON, CONF_ID, CONF_NAME

from . import mirage_m400_ns, MirageM400Component

DEPENDENCIES = ["mirage_m400"]

CONF_ZONE = "zone"
CONF_TYPE = "type"

MirageSwitch = mirage_m400_ns.class_("MirageSwitch", switch.Switch, cg.Component)

SWITCH_TYPES = ["power", "mute"]

CONFIG_SCHEMA = switch.SWITCH_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageSwitch),
        cv.GenerateID("mirage_m400_id"): cv.use_id(MirageM400Component),
        cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*SWITCH_TYPES, lower=True),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config["mirage_m400_id"])
    var = cg.new_Pvariable(
        config[CONF_ID],
        parent,
        config[CONF_ZONE],
        config[CONF_TYPE],
    )
    await switch.register_switch(var, config)
    await cg.register_component(var, config)
