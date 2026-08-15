import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, CONF_MIRAGE_M400_ID

MirageM400TextSensor = mirage_m400_ns.class_("MirageM400TextSensor", cg.Component)

TEXT_SENSOR_SCHEMA = text_sensor.TEXT_SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    }
)

async def to_code(config):
    var = cg.new_variable(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)
    
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    cg.add(parent.register_text_sensor(var))
    cg.add(var.set_parent(parent))
    
    await text_sensor.register_text_sensor(var, config)
