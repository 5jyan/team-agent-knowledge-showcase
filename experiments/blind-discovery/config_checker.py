"""An intentionally generic error from a small fictional configuration checker."""

def validate(config):
    missing = [key for key in ('model', 'version') if key not in config]
    if missing:
        return f"설정 오류: {', '.join(missing)} 항목이 없습니다."
    return '설정 정상'
