import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from .constants import *

DEPENDENCIES = ['mirage_m400']

CONFIG_SCHEMA = cv.Schema({
    cv.Optional("id"): cv.string,
    cv.Optional("name"): cv.string,
    cv.Optional("icon"): cv.string,
    cv.Optional("internal"): cv.boolean,
    cv.Required(CONF_ZONE): cv.int_range(1, 4),
    cv.Required(CONF_MIRAGE_M400_ID): cv.string,
})

async def to_code(config):
    hub = cg.get_variable(cv.get_id(config[CONF_MIRAGE_M400_ID]))
    num = cg.new_Pvariable(cg.MirageM400Number())
    cg.add_expression(" %s->set_parent(%s);" % (num, hub))
    cg.add_expression(" %s->set_zone(%d);" % (num, config[CONF_ZONE]))
    cg.add_expression(" %s->register_number(%s);" % (hub, num))
    cg.register_number(num, config)