import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import CONF_ID, CONF_NAME

from . import CONF_MIRAGE_M400_ID, MirageM400Component, mirage_m400_ns

CONF_ZONE = "zone"
CONF_SOURCES = "sources"
CONF_ENABLED = "enabled"

MAX_SOURCES = 8

MirageSourceSelect = mirage_m400_ns.class_(
    "MirageSourceSelect", select.Select, cg.Component
)

# One entry per physical source, in order (first entry = S1, second = S2, ...).
# Only "name" and/or "enabled" need to be set; omit trailing entries to leave
# the rest at their defaults (name "Sn", enabled).
SOURCE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_NAME): cv.string_strict,
        cv.Optional(CONF_ENABLED, default=True): cv.boolean,
    }
)


def validate_sources(value):
    if len(value) > MAX_SOURCES:
        raise cv.Invalid(f"Only {MAX_SOURCES} sources (S1-S{MAX_SOURCES}) are supported")
    return value


CONFIG_SCHEMA = (
    select.select_schema(MirageSourceSelect)
    .extend(
        {
            cv.GenerateID(CONF_MIRAGE_M400_ID): cv.use_id(MirageM400Component),
            cv.Required(CONF_ZONE): cv.int_range(min=1, max=32),
            # Rename and/or hide individual sources for this zone. Hidden
            # sources are dropped from the option list entirely, so anything
            # that cycles through the entity's options (a dashboard tile
            # stepper, a "next input" automation) skips them automatically.
            cv.Optional(CONF_SOURCES): cv.All(
                cv.ensure_list(SOURCE_SCHEMA), validate_sources
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIRAGE_M400_ID])

    names = [f"S{i + 1}" for i in range(MAX_SOURCES)]
    enabled = [True] * MAX_SOURCES
    for i, source in enumerate(config.get(CONF_SOURCES, [])):
        if CONF_NAME in source:
            names[i] = source[CONF_NAME]
        enabled[i] = source[CONF_ENABLED]

    options = [name for name, is_enabled in zip(names, enabled) if is_enabled]

    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(var, config, options=options)
    cg.add(var.set_parent(parent))
    cg.add(var.set_zone(config[CONF_ZONE]))
    cg.add(var.set_source_names(names))
