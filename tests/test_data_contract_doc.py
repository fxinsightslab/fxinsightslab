from pathlib import Path


def test_data_contract_doc_exists() -> None:
    target = Path("docs/DATA_CONTRACT.md")
    assert target.exists(), "docs/DATA_CONTRACT.md が存在しません"


def test_data_contract_doc_contains_required_sections() -> None:
    text = Path("docs/DATA_CONTRACT.md").read_text(encoding="utf-8")
    required = [
        "`symbol`",
        "`ts_utc`",
        "`o`",
        "`h`",
        "`l`",
        "`c`",
        "`v`",
        "`spread`",
        "tz-aware必須",
        "open` = first",
        "high` = max",
        "low` = min",
        "close` = last",
        "drop_incomplete=True",
        "ffill",
        "bfill",
    ]
    for token in required:
        assert token in text, f"必須項目が不足しています: {token}"
