import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

from . import mirage_m400_ns, MirageM400Component, MirageM400TextSensor, CONF_MIRAGE_M400_ID

TEXT_SENSOR_SCHEMA = text_sensor.TEXT_SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MirageM400TextSensor),
    }
)

async def to_code(config, parent=None):
    var = cg.new_variable(config[CONF_ID], MirageM400TextSensor)
    await cg.register_component(var, config)
    
    if parent is None:
        # Fallback for standalone use
        parent = await cg.get_variable(config.get(CONF_MIRAGE_M400_ID))
    
    cg.add(parent.register_text_sensor(var))
    cg.add(var.set_parent(parent))
    
    await text_sensor.register_text_sensor(var, config)
