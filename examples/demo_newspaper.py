"""
Demo für das erweiterte Newspaper Framework
Mit Logo, Bildern und Sudoku-Funktionalität
"""

from newspaper_framework import NewspaperFrameWork

def create_advanced_newspaper():
    """
    Erweiterte Demo mit allen neuen Features
"""

# Framework mit Logo-Funktionalität erstellen
paper = NewspaperFrameWork("AI Premium Morgenzeitung")

# Logo setzen (symbolisch)
paper.set_logo("newspaper_logo.png")

# Verschiedene Artikel mit unterschiedlichen Features
paper.add_article(
    title="Neues Framework revolutioniert Zeitungsproduktion",
    content="Das erweiterte Newspaper Framework unterstuetzt jetzt Logo, Bilder und Unterhaltungselemente...",
    author="KI-Redakteur",
    category="Technologie",
    priority=1
)

paper.add_article(
    title="Wirtschaft: KI-Analysen im Aufschwung",
    content="Neue Algorithmen ermoeglichen tiefgreifende Wirtschaftsanalysen...",
    author="Wirtschafts-KI",
    category="Wirtschaft",
    priority=2,
    image_path="wirtschafts_chart.png",
    image_caption="KI-generierte Wirtschaftsanalyse"
)

paper.add_article(
    title="Sudoku der Woche: Herausforderung für Leser",
    content="Das neue Framework kann automatisch Sudokus generieren und in die Zeitung integrieren...",
    author="Puzzle-Redaktion",
    category="Unterhaltung",
    priority=3
)

# Exportieren
paper.export_html("advanced_zeitung.html")
paper.export_json("advanced_zeitung.json")

print("Erweiterte Demo erfolgreich abgeschlossen!")

if __name__ == "__main__":
    create_advanced_newspaper()