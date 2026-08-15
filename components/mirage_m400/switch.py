import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_TYPE
from . import mirage_m400_ns, MirageM400Switch, CONF_MIRAGE_M400_ID

CONF_ZONE = "zone"
CONF_POWER = "power"
CONF_MUTE = "mute"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Switch),
        cv.Optional(CONF_POWER): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(MirageM400Switch),
                cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
            }
        ),
        cv.Optional(CONF_MUTE): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(MirageM400Switch),
                cv.Required(CONF_ZONE): cv.int_range(min=1, max=16),
            }
        ),
    }
)


async def to_code(config):
    # Power switches
    if CONF_POWER in config:
        for power_config in config[CONF_POWER]:
            zone = power_config[CONF_ZONE]
            var = cg.new_variable(power_config[cv.GenerateID()], MirageM400Switch())
            await switch.register_switch(var, power_config)
            cg.add(var.set_zone(cg.int(zone)))
            cg.add(var.set_type(cg.int(0)))  # 0 = POWER

    # Mute switches
    if CONF_MUTE in config:
        for mute_config in config[CONF_MUTE]:
            zone = mute_config[CONF_ZONE]
            var = cg.new_variable(mute_config[cv.GenerateID()], MirageM400Switch())
            await switch.register_switch(var, mute_config)
            cg.add(var.set_zone(cg.int(zone)))
            cg.add(var.set_type(cg.int(1)))  # 1 = MUTE
