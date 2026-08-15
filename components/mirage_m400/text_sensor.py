import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

DEPENDENCIES = ["mirage_m400"]

MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", text_sensor.TextSensor)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    }
).extend(text_sensor.SCHEMA)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvt_var(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)
    cg.add(parent.register_text_sensor(var))
