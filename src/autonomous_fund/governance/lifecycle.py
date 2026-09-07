"""Strategy lifecycle state machine."""

from enum import StrEnum


class StrategyStage(StrEnum):
    IDEA = "idea"
    SPEC = "spec"
    BACKTEST = "backtest"
    WALK_FORWARD = "walk_forward"
    STRESS = "stress"
    PAPER = "paper"
    SHADOW = "shadow"
    SMALL_LIVE = "small_live"
    PRODUCTION = "production"
    REVIEW = "review"
    RETIRED = "retired"


_ALLOWED: dict[StrategyStage, set[StrategyStage]] = {
    StrategyStage.IDEA: {StrategyStage.SPEC, StrategyStage.RETIRED},
    StrategyStage.SPEC: {StrategyStage.BACKTEST, StrategyStage.RETIRED},
    StrategyStage.BACKTEST: {StrategyStage.WALK_FORWARD, StrategyStage.RETIRED},
    StrategyStage.WALK_FORWARD: {StrategyStage.STRESS, StrategyStage.RETIRED},
    StrategyStage.STRESS: {StrategyStage.PAPER, StrategyStage.RETIRED},
    StrategyStage.PAPER: {StrategyStage.SHADOW, StrategyStage.RETIRED},
    StrategyStage.SHADOW: {StrategyStage.SMALL_LIVE, StrategyStage.REVIEW, StrategyStage.RETIRED},
    StrategyStage.SMALL_LIVE: {StrategyStage.PRODUCTION, StrategyStage.REVIEW, StrategyStage.RETIRED},
    StrategyStage.PRODUCTION: {StrategyStage.REVIEW, StrategyStage.RETIRED},
    StrategyStage.REVIEW: {StrategyStage.PAPER, StrategyStage.PRODUCTION, StrategyStage.RETIRED},
    StrategyStage.RETIRED: set(),
}


def transition(current: StrategyStage, target: StrategyStage) -> StrategyStage:
    if target not in _ALLOWED[current]:
        raise ValueError(f"invalid strategy transition: {current} -> {target}")
    return target
