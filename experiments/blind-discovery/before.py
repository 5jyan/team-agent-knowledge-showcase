"""Initial input supplied to the separate Codex session."""

def validate(config):
    if 'model' not in config or 'version' not in config:
        return '설정 오류'
    return '설정 정상'
