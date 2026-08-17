import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from .constants import *

DEPENDENCIES = ['mirage_m400']

CONFIG_SCHEMA = cv.Schema({
    cv.Optional("id"): cv.GenerateID(),
    cv.Required(CONF_ZONE): cv.int_range(1, 4),
    cv.Required(CONF_TYPE): cv.enum(SWITCH_TYPES),
})

async def to_code(config):
    hub = cg.get_variable(cv.get_id(CONF_MIRAGE_M400_ID))
    sw = cg.new_Pvariable(cg.MirageM400Switch())

    cg.add_expression(" %s->set_parent(%s);" % (sw, hub))
    cg.add_expression(" %s->set_zone(%d);" % (sw, config[CONF_ZONE]))
    cg.add_expression(" %s->set_type(%d);" % (sw, config[CONF_TYPE]))
    cg.add_expression(" %s->register_switch(%s);" % (hub, sw))

    cg.register_switch(sw, config)
