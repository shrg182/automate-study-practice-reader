#!/usr/bin/env python3
"""Generate the AI course as a news-report-style study PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "ai_course_study_report.pdf"
REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1F5F99")
MID_BLUE = colors.HexColor("#486581")
MUTED = colors.HexColor("#627D98")
INK = colors.HexColor("#1F2933")
LINE = colors.HexColor("#BCCCDC")
PALE_BLUE = colors.HexColor("#F0F4F8")
PALE_GOLD = colors.HexColor("#FFF1B8")
PALE_GREEN = colors.HexColor("#E3F0DC")


def register_fonts() -> tuple[str, str]:
    if REGULAR.exists() and BOLD.exists():
        pdfmetrics.registerFont(TTFont("AIReportArial", str(REGULAR)))
        pdfmetrics.registerFont(TTFont("AIReportArialBold", str(BOLD)))
        return "AIReportArial", "AIReportArialBold"
    return "Helvetica", "Helvetica-Bold"


def build() -> None:
    regular, bold = register_fonts()
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName=bold, fontSize=24,
            leading=29, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8,
        ),
        "dek": ParagraphStyle(
            "Dek", parent=base["BodyText"], fontName=regular, fontSize=10.5,
            leading=15, textColor=MID_BLUE, alignment=TA_CENTER, spaceAfter=10,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=base["BodyText"], fontName=regular, fontSize=8.5,
            leading=11, textColor=MUTED, alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading2"], fontName=bold, fontSize=14,
            leading=18, textColor=colors.HexColor("#12355B"),
            spaceBefore=12, spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading3"], fontName=bold, fontSize=11,
            leading=14, textColor=BLUE, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName=regular, fontSize=9.5,
            leading=14, textColor=INK, spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName=regular, fontSize=7.8,
            leading=10.5, textColor=colors.HexColor("#334E68"),
        ),
        "cell": ParagraphStyle(
            "Cell", parent=base["BodyText"], fontName=regular, fontSize=8.2,
            leading=11, textColor=colors.HexColor("#243B53"),
        ),
        "cell_b": ParagraphStyle(
            "CellB", parent=base["BodyText"], fontName=bold, fontSize=8.2,
            leading=11, textColor=colors.white, alignment=TA_CENTER,
        ),
        "callout": ParagraphStyle(
            "Callout", parent=base["BodyText"], fontName=regular, fontSize=8.7,
            leading=13, textColor=colors.HexColor("#294955"),
        ),
        "russian": ParagraphStyle(
            "Russian", parent=base["BodyText"], fontName=regular, fontSize=10,
            leading=15, textColor=INK, spaceAfter=7,
        ),
    }

    def p(text: str, style: str = "body") -> Paragraph:
        return Paragraph(text, styles[style])

    def table(data, widths, *, header=False, first_column=False, padding=7) -> Table:
        item = Table(data, colWidths=widths, repeatRows=1 if header else 0)
        commands = [
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9E2EC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), padding),
        ]
        if header:
            commands += [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
            ]
        elif first_column:
            commands += [
                ("BACKGROUND", (0, 0), (0, -1), BLUE),
                ("BACKGROUND", (1, 0), (-1, -1), PALE_BLUE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        item.setStyle(TableStyle(commands))
        return item

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.62 * inch, bottomMargin=0.62 * inch,
        title="How AI Works: A Beginner's Journey",
        author="Codex, OpenAI",
        subject="News-report-style AI course and annotated study edition",
    )

    story = [
        p("How AI Works", "title"),
        p("A beginner’s journey inside the machine that learns", "dek"),
        p("Study report | Updated August 4, 2026", "meta"),
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=1.1, color=LINE),
        Spacer(1, 10),
    ]

    overview = [
        [p("Central question", "cell_b"), p("How can a computer learn useful patterns without containing a human mind?", "cell")],
        [p("Core process", "cell_b"), p("Examples → learning process → trained model → prediction", "cell")],
        [p("Course path", "cell_b"), p("AI basics, data, training, neural networks, language models, a Python project, and responsible use.", "cell")],
        [p("Study features", "cell_b"), p("Highlighted phrases, inline notes, editorial commentary, a pending-review item, reader notes, and a footnote.", "cell")],
    ]
    story += [table(overview, [1.2 * inch, 5.2 * inch], first_column=True)]

    story += [p("Opening Report: Inside the Machine That Learns", "h1")]
    story += [
        p(
            'Every day, <font backColor="#FFF1B8"><b>artificial intelligence quietly helps people</b></font> '
            "choose music, translate messages, find photographs, avoid spam, and answer questions. "
            "To a casual observer, these systems can seem almost magical. Behind the scenes, however, "
            "there is no tiny person thinking inside the computer. There are data, mathematical operations, "
            "learning algorithms, and many adjustable values<super><font color=\"#1F5F99\">1</font></super> "
            "working together at remarkable speed."
        ),
        Table(
            [[p("EDITORIAL COMMENT", "cell_b"), p(
                "The opening moves from familiar uses of AI to the less visible machinery beneath them. "
                "This contrast introduces the course’s central goal: replacing mystery with a clear account "
                "of learning from data.", "callout")]],
            colWidths=[1.35 * inch, 5.05 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), MID_BLUE),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#EDF4F6")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B9CCD6")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]),
        ),
        Spacer(1, 7),
        p(
            "This course follows the story of how an ordinary computer becomes a machine that can "
            "<u>recognize patterns</u>. We will begin by separating artificial intelligence from traditional "
            "rule-based software. Then we will enter the training room, where a model studies examples, "
            '<font backColor="#DCEBF0"><b>makes predictions, measures its mistakes, and gradually improves</b></font>. '
            "From there, we will explore neural networks, discover how language models learn relationships "
            "between words, and examine why even powerful AI can produce confident but incorrect answers."
        ),
        p(
            "Our investigation unfolds in seven stages: what AI is; learning from data; training a model; "
            "neural networks; tokens, context, and next-token prediction<super><font color=\"#1F5F99\">2</font></super>; "
            "building a small AI in Python; and responsible use. The final stage considers bias, privacy, "
            'reliability, and <font backColor="#D9C2F0">human judgment</font>.'
        ),
        p(
            "By the end, AI should feel less like magic and more like an understandable—though still "
            "impressive—engineering achievement. Each lesson includes a plain-language explanation, a "
            "familiar example, a quick question, and, when useful, a small experiment."
        ),
    ]

    story += [p("Lesson 1: What Is Artificial Intelligence?", "h1")]
    story += [
        p(
            "Artificial intelligence is the broad name for computer systems designed to perform tasks that "
            '<u>appear to require human abilities</u><super><font color="#A52D24">?</font></super>, '
            "such as recognizing speech, interpreting images, finding patterns, making predictions, or generating language."
        ),
        p(
            "Not every useful computer program is AI. A calculator follows precise rules written by a "
            "programmer. A machine-learning spam filter is different: it studies examples of spam and "
            "ordinary email, detects patterns in those examples, and uses the patterns to classify new messages."
        ),
        p(
            "The basic process is simple to describe: examples enter a learning process; the learning process "
            "produces a trained model<super><font color=\"#1F5F99\">3</font></super>; and the trained model makes "
            "a prediction about new information."
        ),
        p("Quick Check", "h2"),
        p(
            "Which system learns from data—a light switch, a calculator following fixed arithmetic rules, "
            "or an email filter trained on examples of spam? <b>Answer:</b> the email filter, because it learns "
            "patterns from labeled examples."
        ),
        p("Your turn: Name one AI system you encounter in daily life. What information or examples do you think it learned from?"),
    ]

    story += [p("Lesson 2: How Machines Learn from Data", "h1")]
    story += [
        p(
            'A machine-learning system <font backColor="#FFF1B8">learns from examples rather than receiving '
            "every rule directly</font>. Each example contains information the model can examine. The model "
            "searches across many examples for relationships that help it make a useful prediction."
        ),
        p(
            "Suppose we want a model to distinguish apples from oranges. We might give it examples described "
            "by color, weight, texture, and shape. These measurable properties are called features"
            "<super><font color=\"#1F5F99\">4</font></super>. The correct answer attached to each example—apple "
            "or orange—is called its label<super><font color=\"#1F5F99\">5</font></super>."
        ),
        p(
            'During training, the <font backColor="#E3F0DC">model studies the features and labels together</font>. '
            "At first, its predictions may be poor. A learning algorithm measures the errors and adjusts the "
            "model’s parameters so that later predictions are more accurate. Training is a repeated cycle: "
            "predict, compare, adjust, and try again."
        ),
        p(
            "Good performance on remembered examples is not enough. We normally divide the available data into "
            "a training set and a test set. The model learns from the training set, but the test set contains "
            '<font backColor="#DCEBF0">separate examples that were not used to adjust the model</font>. Testing '
            "helps reveal whether the model learned a general pattern or merely memorized its lessons."
        ),
        p(
            "Data quality matters as much as quantity<super><font color=\"#A52D24\">?</font></super>. If the examples "
            "are incorrect, incomplete, or unrepresentative, the model may learn misleading patterns. A fruit "
            "classifier trained only on green apples might wrongly treat redness as evidence that a fruit is an "
            'orange. The data should <font backColor="#D9C2F0">represent the real situations in which the model '
            "will be used</font>."
        ),
        p("Quick Check", "h2"),
        p(
            "A model scores perfectly on its training examples but performs badly on new examples. Did it "
            "necessarily learn a useful general pattern? <b>No.</b> It may have memorized the training data, a "
            "problem known as overfitting<super><font color=\"#1F5F99\">6</font></super>."
        ),
        p(
            "Your turn: Imagine training an AI system to identify whether a photograph was taken indoors or "
            "outdoors. Name three useful features and one possible source of bias in the training data."
        ),
    ]

    story += [p("Lesson 3: How Training Improves a Model", "h1")]
    story += [
        p(
            'Training <font backColor="#FFF1B8">turns mistakes into directions for improvement</font>. A model '
            "receives an input, makes a prediction, and compares that prediction with the known answer. The "
            "difference tells the training process how far the model is from the desired result."
        ),
        p(
            "Imagine a model predicting the price of a house. If the correct price is $300,000 and the model "
            "predicts $240,000, its error is $60,000. A loss function"
            "<super><font color=\"#1F5F99\">7</font></super> "
            '<font backColor="#E3F0DC">converts the difference between predictions and answers into a number</font>. '
            "A larger loss usually means that the prediction was worse."
        ),
        p(
            "The learning algorithm then asks which internal parameters contributed to the error. In a large "
            "model, millions or even billions of parameters may share responsibility. The algorithm "
            '<font backColor="#DCEBF0">calculates a small adjustment to many parameters</font>, aiming to make '
            "the loss slightly lower the next time similar data appears."
        ),
        p(
            "One widely used adjustment method is gradient descent"
            "<super><font color=\"#1F5F99\">8</font></super>. Imagine standing on a foggy hillside and trying "
            "to reach the lowest point. You cannot see the whole landscape, but you can feel which direction "
            "slopes downward. By taking repeated downhill steps, you may approach a low point"
            "<super><font color=\"#A52D24\">?</font></super>. Gradient descent similarly uses the local slope "
            "of the loss to choose a direction for updating parameters."
        ),
        p(
            "The size of each update is controlled by the learning rate"
            "<super><font color=\"#1F5F99\">9</font></super>. If the learning rate is too small, training may "
            "be extremely slow. If it is too large, the model may repeatedly jump past a useful solution. "
            'Effective training requires a <font backColor="#D9C2F0">balance between learning too slowly and '
            "overshooting</font>."
        ),
        p(
            "One complete pass through the training data is called an epoch. Models commonly train for many "
            "epochs, but more is not always better. We can monitor performance on a validation set while "
            "training. If training loss continues to improve while validation performance becomes worse, the "
            "model may be starting to overfit."
        ),
        p("Quick Check", "h2"),
        p(
            "Why not make the learning rate as large as possible? <b>A very large update can skip over better "
            "parameter settings or make training unstable.</b>"
        ),
        p(
            "Your turn: Picture yourself walking downhill in fog. What do the hill’s height, downhill direction, "
            "step size, and repeated steps represent in model training?"
        ),
    ]

    story += [p("Lesson 4: Neural Networks", "h1")]
    story += [
        p(
            "A neural network is a model built from layers of simple mathematical units often called artificial "
            "neurons<super><font color=\"#1F5F99\">10</font></super>. The name is loosely inspired by biological "
            'brains, but an artificial neural network is an <font backColor="#FFF1B8">engineered system of '
            "calculations, not a miniature human brain</font>."
        ),
        p(
            "Each artificial neuron receives several input numbers. It multiplies each input by a learned weight, "
            "adds the results together, and usually adds another adjustable value called a bias term. An activation "
            "function<super><font color=\"#1F5F99\">11</font></super> then transforms the total and determines the "
            "value passed forward."
        ),
        p(
            'The <font backColor="#E3F0DC">weights tell the network which inputs deserve more or less influence</font>. '
            "Consider a simple system estimating whether a student will complete an assignment. Time available, "
            "assignment length, and previous completion patterns might enter as numbers. Training adjusts their "
            "weights according to how strongly each input helps predict the answer."
        ),
        p(
            "Neurons are arranged in layers. The input layer receives the original information. One or more hidden "
            'layers <font backColor="#DCEBF0">transform it into increasingly useful internal patterns</font>. The '
            "output layer produces the final prediction. Information moving from input to output is called a forward pass."
        ),
        p(
            "Hidden layers allow a network to build representations in stages. In an image system, early layers may "
            "respond to edges or colors, middle layers may combine them into textures and shapes, and later layers may "
            "respond to larger structures. Training helps the network discover useful combinations without a separate "
            "programmed rule for every possible shape."
        ),
        p(
            "After a forward pass, the loss function measures prediction error. Backpropagation"
            "<super><font color=\"#1F5F99\">12</font></super> works backward through the network to calculate how "
            "each weight contributed to that error. Gradient descent then uses those calculations to update the weights."
        ),
        p(
            "Deep learning uses neural networks with multiple hidden layers. Greater depth can help represent complicated "
            "patterns, but a larger network is not automatically better. It may require more data, computation, careful "
            "evaluation, and safeguards against overfitting."
        ),
        p("Quick Check", "h2"),
        p(
            "Does an artificial neuron understand its inputs in the human sense? <b>No.</b> It performs numerical "
            'operations; <font backColor="#D9C2F0">useful behavior emerges from many trained operations working '
            "together</font>."
        ),
        p(
            "Your turn: Draw a tiny network with three input circles, two hidden-layer circles, and one output circle. "
            "What real-world quantities could the three inputs represent, and what could the output predict?"
        ),
        p(
            '<font backColor="#E3F0DC"><b>Искусственный интеллект учится на примерах</b></font>: '
            "система сравнивает свои прогнозы с известными ответами, замечает ошибки и постепенно изменяет "
            "внутренние параметры. Поэтому качество модели зависит не только от алгоритма, но и от данных, "
            "целей обучения и человеческой проверки.<super><font color=\"#1F5F99\">*</font></super>",
            "russian",
        ),
        p(
            "<b>Editor’s footnote *</b> — This independent Russian paragraph restates the training cycle: "
            "compare predictions with known answers, measure errors, and adjust parameters. It also emphasizes "
            "data quality and human review.",
            "small",
        ),
    ]

    note_rows = [
        [p("Marker", "cell_b"), p("Inline note", "cell_b")],
        [p("1", "cell"), p("Adjustable values are the model’s parameters.", "cell")],
        [p("2", "cell"), p("Next-token prediction estimates the next unit of text from preceding context.", "cell")],
        [p("3", "cell"), p("A trained model is the result of learning from examples and can be used on new input.", "cell")],
        [p("4", "cell"), p("Features are measurable properties or inputs used to make a prediction.", "cell")],
        [p("5", "cell"), p("A label is the known answer associated with a training example.", "cell")],
        [p("6", "cell"), p("Overfitting means learning the training examples too narrowly to generalize well.", "cell")],
        [p("7", "cell"), p("A loss function measures prediction error as a number training can minimize.", "cell")],
        [p("8", "cell"), p("Gradient descent updates parameters in a direction that reduces loss.", "cell")],
        [p("9", "cell"), p("The learning rate controls the size of each parameter update.", "cell")],
        [p("10", "cell"), p("Artificial neurons are mathematical units that combine and transform input values.", "cell")],
        [p("11", "cell"), p("An activation function transforms a neuron’s total before passing it onward.", "cell")],
        [p("12", "cell"), p("Backpropagation calculates how network parameters contributed to prediction error.", "cell")],
        [p("?", "cell"), p("Pending review: consider whether “imitate aspects of human abilities” would be more precise.", "cell")],
        [p("?", "cell"), p("Pending clarification: gradient descent is not guaranteed to find the best possible solution.", "cell")],
    ]
    story += [
        p("Inline Notes and Pending Review", "h1"),
        table(note_rows, [0.72 * inch, 5.68 * inch], header=True, padding=3),
    ]

    reader_rows = [
        [p("Reader’s note", "cell_b"), p(
            "The contrast between a calculator and a spam filter is useful. One follows rules supplied directly "
            "by a programmer; the other derives classification patterns from examples.", "cell")],
        [p("Reader’s question", "cell_b"), p(
            "If a model learns biased patterns from its training data, which parts of training and evaluation "
            "can reveal or reduce that bias?", "cell")],
        [p("Lesson 2 note", "cell_b"), p(
            "The apple-and-orange example makes features and labels concrete, while the separate test set "
            "explains why memorization is not the same as learning a general pattern.", "cell")],
        [p("Lesson 3 note", "cell_b"), p(
            "The foggy-hillside analogy connects loss, gradient direction, learning rate, and repeated updates "
            "without requiring calculus.", "cell")],
        [p("Lesson 4 note", "cell_b"), p(
            "A neural network is a system of layered numerical transformations. The brain analogy is historical "
            "and limited.", "cell")],
    ]
    story += [p("Reader’s Notes", "h1"), table(reader_rows, [1.3 * inch, 5.1 * inch], first_column=True)]

    glossary = [
        [p("Term", "cell_b"), p("Meaning in this course", "cell_b")],
        [p("artificial intelligence", "cell"), p("Computer systems designed to perform tasks associated with human intelligence.", "cell")],
        [p("machine learning", "cell"), p("Learning patterns from data rather than relying only on fixed rules.", "cell")],
        [p("model", "cell"), p("A trained mathematical system that produces predictions or generated output.", "cell")],
        [p("parameter", "cell"), p("An adjustable numerical value changed during training.", "cell")],
        [p("neural network", "cell"), p("A model made from connected layers of mathematical operations.", "cell")],
        [p("token", "cell"), p("A unit of text processed by a language model.", "cell")],
        [p("bias", "cell"), p("A systematic tendency that can produce uneven or unfair results.", "cell")],
        [p("feature", "cell"), p("A measurable property or input used by a model to make a prediction.", "cell")],
        [p("label", "cell"), p("The known answer associated with a training example.", "cell")],
        [p("training set", "cell"), p("The examples used to adjust a model during training.", "cell")],
        [p("test set", "cell"), p("Separate examples used to evaluate a model on unseen data.", "cell")],
        [p("overfitting", "cell"), p("Learning training examples too narrowly and performing poorly on new examples.", "cell")],
        [p("loss function", "cell"), p("A rule that converts prediction error into a number for training to minimize.", "cell")],
        [p("gradient descent", "cell"), p("A method for adjusting parameters in a direction that reduces loss.", "cell")],
        [p("learning rate", "cell"), p("The setting that controls the size of each parameter update.", "cell")],
        [p("epoch", "cell"), p("One complete pass through the training data.", "cell")],
        [p("validation set", "cell"), p("Separate data used during training to monitor generalization.", "cell")],
        [p("artificial neuron", "cell"), p("A mathematical unit that combines input values and passes a transformed value forward.", "cell")],
        [p("activation function", "cell"), p("A function that transforms a neuron’s combined input.", "cell")],
        [p("hidden layer", "cell"), p("An internal layer that transforms information into learned representations.", "cell")],
        [p("forward pass", "cell"), p("The movement and transformation of information from input to output.", "cell")],
        [p("backpropagation", "cell"), p("A method for calculating how network parameters contributed to error.", "cell")],
        [p("deep learning", "cell"), p("Machine learning using neural networks with multiple hidden layers.", "cell")],
    ]
    story += [
        KeepTogether([
            p("Course Vocabulary", "h1"),
            table(glossary, [1.7 * inch, 4.7 * inch], header=True),
        ])
    ]
    story += [
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.7, color=LINE),
        Spacer(1, 6),
        p(
            "This course was created by Codex, an AI coding agent from OpenAI.",
            "small",
        ),
    ]

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.7 * inch, 0.34 * inch, "How AI Works · Annotated Study Report")
        canvas.drawRightString(7.8 * inch, 0.34 * inch, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
