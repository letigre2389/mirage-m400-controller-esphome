# VERSION: 3.0
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from .constants import *

DEPENDENCIES = ['mirage_m400']

CONFIG_SCHEMA = cv.Schema({
    cv.Optional("id"): cv.GenerateID(),
    cv.Optional("name"): cv.string,
    cv.Optional("icon"): cv.string,
    cv.Optional("internal"): cv.boolean,
    cv.Required(CONF_MIRAGE_M400_ID): cv.string,
})

async def to_code(config):
    hub = cg.get_variable(cv.get_id(config[CONF_MIRAGE_M400_ID]))
    sensor = cg.new_Pvariable(cg.MirageM400TextSensor())
    cg.add_expression(" %s->set_parent(%s);" % (sensor, hub))
    cg.add_expression(" %s->register_text_sensor(%s);" % (hub, sensor))
    cg.register_text_sensor(sensor, config)
