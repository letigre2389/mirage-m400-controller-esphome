import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import CONF_ID

from . import CONF_MIRAGE_M400_ID, MirageM400Component, mirage_m400_ns

CONF_ZONE = "zone"

MirageSourceSelect = mirage_m400_ns.class_(
    "MirageSourceSelect", select.Select, cg.Component
)

CONFIG_SCHEMA = (
    select.select_schema(MirageSourceSelect)
    .extend(
        {
            cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
            cv.Required(CONF_ZONE): cv.int_range(min=1, max=32),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(
        var, config, options=["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    )
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
