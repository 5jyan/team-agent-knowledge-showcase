"""Standalone configuration validation example."""


def check_config(config: dict) -> str:
    """Check presence of the example's required keys without exposing values."""
    missing = [key for key in ("model", "version") if key not in config]
    if missing:
        return f"설정 오류: {', '.join(missing)} 항목이 없습니다"
    return "설정 정상"
