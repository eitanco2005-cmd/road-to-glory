"""Generate all W2 HTML pages into docs/.  python3 products/wedding-planner/web/build_pages.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guides, product_pages, tool_bar_mitzvah, tool_wedding_gift

if __name__ == "__main__":
    files = [tool_wedding_gift.build(), tool_bar_mitzvah.build()] + product_pages.build() + guides.build()
    for f in files:
        print(os.path.relpath(f))
