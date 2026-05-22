import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from newspaper import Newspaper, QuizSystem


def create_advanced_newspaper():
    paper = Newspaper("AI Premium Morgenzeitung")

    paper.set_logo("newspaper_logo.png")

    paper.add_article(
        title="Neues Framework revolutioniert Zeitungsproduktion",
        content="Das erweiterte Newspaper Framework unterstuetzt jetzt Logo, Bilder und Unterhaltungselemente...",
        author="KI-Redakteur",
        category="Technologie",
        priority=1,
    )

    paper.add_article(
        title="Wirtschaft: KI-Analysen im Aufschwung",
        content="Neue Algorithmen ermoeglichen tiefgreifende Wirtschaftsanalysen...",
        author="Wirtschafts-KI",
        category="Wirtschaft",
        priority=2,
        image_path="wirtschafts_chart.png",
        image_caption="KI-generierte Wirtschaftsanalyse",
    )

    paper.add_article(
        title="Sudoku der Woche: Herausforderung fuer Leser",
        content="Das neue Framework kann automatisch Sudokus generieren und in die Zeitung integrieren...",
        author="Puzzle-Redaktion",
        category="Unterhaltung",
        priority=3,
    )

    paper.add_sudoku(difficulty="medium")

    html = paper.export_html("advanced_zeitung.html")
    json_data = paper.export_json("advanced_zeitung.json")

    print("Demo erfolgreich abgeschlossen!")


if __name__ == "__main__":
    create_advanced_newspaper()
