# israel-data (Python)

Israeli holidays 2025–2030 (Hebrew + English), VAT rate history, osek patur ceiling and minimum wage. Zero dependencies.
Full documentation, sources and CSV/JSON downloads: https://github.com/eitanco2005-cmd/road-to-glory/tree/main/data-il
· https://tichnun.netlify.app/data-il/

```bash
pip install "git+https://github.com/eitanco2005-cmd/road-to-glory.git#subdirectory=data-il/python"
```

```python
import israel_data as il
il.is_israeli_holiday("2026-04-22")   # [{'id': 'yom-haatzmaut', 'name_he': 'יום העצמאות', ...}]
il.add_vat(1000)                      # {'net': 1000.0, 'vat': 180.0, 'gross': 1180.0, 'rate': 0.18}
```
