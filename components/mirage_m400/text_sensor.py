import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from . import mirage_m400_ns, MirageM400Component
from .constants import *

DEPENDENCIES = ["mirage_m400"]

MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", text_sensor.TextSensor)

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
    cv.Required(cv.CONF_NAME): cv.string,
}).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[cv.GenerateID()], config[cv.CONF_NAME])
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    cg.add(hub.register_text_sensor(var))