import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from . import mirage_m400

DEPENDENCIES = ['mirage_m400']

CONFIG_SCHEMA = cv.Schema({
    cv.Optional(switch.SWITCH_ID): cv.generate_id(),
    cv.Required(mirage_m400.CONF_ZONE): cv.int_range(1, 4),
    cv.Required(mirage_m400.CONF_TYPE): cv.enum(mirage_m400.SWITCH_TYPES),
}).extend(switch.CONFIG_SCHEMA)

async def to_code(config):
    hub = cg.get_variable(cv.get_id(mirage_m400.CONF_MIRAGE_M400_ID))

    # Correct C++ generation: var = new Class();
    sw = cg.new_Pvariable(cg.MirageM400Switch())
    cg.add_expression(" %s->set_parent(%s);" % (sw, hub))
    cg.add_expression(" %s->set_zone(%d);" % (sw, config[mirage_m400.CONF_ZONE]))
    cg.add_expression(" %s->set_type(%d);" % (sw, config[mirage_m400.CONF_TYPE]))
    cg.add_expression(" %s->register_switch(%s);" % (hub, sw))

    cg.register_switch(sw, config)
