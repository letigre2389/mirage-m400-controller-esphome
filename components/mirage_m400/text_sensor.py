import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor

from . import CONF_MIRAGE_M400_ID, MirageM400Component

CONFIG_SCHEMA = text_sensor.text_sensor_schema().extend(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = await text_sensor.new_text_sensor(config)
    cg.add(parent.set_last_response_text_sensor(var))
