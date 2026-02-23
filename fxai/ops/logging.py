import logging


def setup_logging(level: int = logging.INFO) -> None:
    """共通ロギング設定を初期化する。"""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
