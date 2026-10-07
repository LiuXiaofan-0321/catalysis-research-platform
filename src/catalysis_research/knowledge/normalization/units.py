from __future__ import annotations

import math
import re
from typing import Any

from .rules import alias_key, compact


NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def number(value: Any, raw_value: Any = None) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        result = float(value)
        return result if math.isfinite(result) else None
    match = NUMBER_RE.search(compact(value) or compact(raw_value))
    if not match:
        return None
    result = float(match.group(0))
    return result if math.isfinite(result) else None


def _unit(value: Any) -> str:
    return alias_key(value).replace("−", "-")


def normalize_condition(name: Any, value: Any, unit: Any, raw: Any) -> tuple[dict[str, Any] | None, str]:
    key = alias_key(name)
    unit_key = _unit(unit)
    numeric = number(value, raw)
    if numeric is None:
        return None, "non_numeric_value"

    if key in {"temperature", "temp", "reactiontemperature", "温度"}:
        if unit_key in {"c", "oc", "degc", "celsius", "摄氏度"}:
            numeric += 273.15
        elif unit_key not in {"k", "kelvin", "开尔文"}:
            return None, "ambiguous_temperature_unit"
        return {"name": "temperature", "value": round(numeric, 8), "unit": "K"}, "temperature_to_K"

    if key in {"pressure", "reactionpressure", "压力"}:
        factors = {"pa": 0.001, "kpa": 1.0, "mpa": 1000.0, "bar": 100.0, "mbar": 0.1, "atm": 101.325}
        if unit_key not in factors:
            return None, "ambiguous_pressure_unit"
        return {"name": "pressure", "value": round(numeric * factors[unit_key], 8), "unit": "kPa"}, "pressure_to_kPa"

    if key in {"time", "duration", "reactiontime", "residencetime", "时间"}:
        factors = {"s": 1.0, "sec": 1.0, "second": 1.0, "seconds": 1.0, "min": 60.0, "minute": 60.0, "minutes": 60.0, "h": 3600.0, "hr": 3600.0, "hour": 3600.0, "hours": 3600.0}
        if unit_key not in factors:
            return None, "ambiguous_time_unit"
        return {"name": "time", "value": round(numeric * factors[unit_key], 8), "unit": "s"}, "time_to_s"

    if key in {"whsv", "ghsv"}:
        accepted = {"h1", "hr1", "hour1", "1h", "1hr"}
        if unit_key not in accepted:
            return None, "ambiguous_space_velocity_unit"
        return {
            "name": key.upper(),
            "value": round(numeric, 8),
            "unit": "h^-1",
            "basis": key.upper(),
        }, "space_velocity_to_h-1"

    if key in {"flow", "flowrate", "gasflow", "feedflow", "流量"}:
        volumetric_factors = {
            "mlmin": (1.0, "reported_volumetric"),
            "cm3min": (1.0, "reported_volumetric"),
            "lmin": (1000.0, "reported_volumetric"),
            "sccm": (1.0, "standard_volumetric"),
        }
        if unit_key in volumetric_factors:
            factor, basis = volumetric_factors[unit_key]
            return {
                "name": "flow",
                "value": round(numeric * factor, 8),
                "unit": "mL/min",
                "basis": basis,
            }, "volumetric_flow_to_mL_min"
        mass_factors = {"gh": 1.0, "kgh": 1000.0, "mgh": 0.001}
        if unit_key in mass_factors:
            return {
                "name": "flow",
                "value": round(numeric * mass_factors[unit_key], 8),
                "unit": "g/h",
                "basis": "mass_flow",
            }, "mass_flow_to_g_h"
        return None, "ambiguous_flow_unit_or_basis"

    return None, "unsupported_condition"


def normalize_metric(name: Any, value: Any, unit: Any, raw: Any) -> tuple[dict[str, Any] | None, str]:
    metric = alias_key(name)
    numeric = number(value, raw)
    if numeric is None:
        return None, "non_numeric_value"
    if metric not in {"conversion", "selectivity", "yield", "转化率", "选择性", "收率"}:
        return None, "unsupported_or_basis_sensitive_metric"
    canonical_names = {"转化率": "conversion", "选择性": "selectivity", "收率": "yield"}
    unit_key = _unit(unit)
    if compact(unit) == "%" or unit_key in {"percent", "percentage", "pct"}:
        pass
    elif unit_key in {"", "fraction", "ratio", "1"}:
        if 0.0 <= numeric <= 1.0:
            numeric *= 100.0
        else:
            return None, "unitless_metric_outside_fraction_range"
    else:
        return None, "ambiguous_metric_unit_or_basis"
    if not 0.0 <= numeric <= 100.0:
        return None, "percent_metric_out_of_range"
    return {
        "metric_name": canonical_names.get(metric, metric),
        "value": round(numeric, 8),
        "unit": "%",
    }, "fraction_or_percent_to_percent"
