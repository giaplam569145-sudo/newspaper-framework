"""Sample Newspaper Generation Script."""

from src.newspaper.core import Newspaper
from src.newspaper.content.quiz import QuizSystem
from src.newspaper.content.crossword import CrosswordGenerator

def create_sample_newspaper():
    """Creates a sample newspaper to demonstrate the framework's usage."""

    paper = Newspaper("AI Morning News")

    paper.add_article(
        title="New Framework Revolutionizes AI-Powered Newspaper Production",
        content="The Newspaper Framework allows LLMs to create high-quality newspapers with minimal effort. With integrated features for images, quizzes, and Sudoku, newspaper creation becomes a breeze.",
        author="AI Editor",
        category="Technology",
        priority=1
    )

    paper.add_article(
        title="Economy in Transition: AI-Based Analyses Gain Importance",
        content="New algorithms enable in-depth economic analyses in real-time. Companies are increasingly using AI systems for strategic decisions.",
        author="Economics AI",
        category="Business",
        priority=2
    )

    quiz = QuizSystem("Technology Quiz")
    quiz.add_question(
        "What is AI?",
        ["Artificial Intelligence", "Kitchen International", "Merchant Institute", "No Idea"],
        0,
        "Technology"
    )
    paper.add_quiz(quiz)

    paper.add_sudoku("medium")

    crossword_generator = CrosswordGenerator(
        words=["python", "html"],
        clues={
            "python": "A popular programming language.",
            "html": "A markup language for the web.",
        },
    )
    paper.add_crossword(crossword_generator.generate())

    paper.export_html("sample_newspaper.html")
    paper.export_json("sample_newspaper.json")

    return paper

if __name__ == "__main__":
    print("Starting Newspaper Framework Demo...")
    create_sample_newspaper()
    print("Demo successfully completed!")
    print("Files created: sample_newspaper.html, sample_newspaper.json")
