from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT = "Cybersecurity_Personal_Statement.docx"

TITLE = "Personal Statement"

PARAGRAPHS = [
    "My decision to pursue a career in cybersecurity comes from a long-standing curiosity about how technology works beneath the surface, and from a belief that understanding a problem properly is the first step towards solving it. When I was younger, I assumed that struggling with a subject meant I was not capable of it. My own experience of Mathematics taught me otherwise, and it shaped the way I now approach both technology and problems generally.",

    "Mathematics was not always easy for me. My perspective changed when I began to connect mathematical concepts to everyday situations and to understand where equations came from instead of simply memorising them. My elder brother, who was strong in Mathematics, helped me approach problems in simple steps. I gradually realised that equations come from underlying concepts and can be related to real-life situations. That approach gave me confidence, and it taught me something I have carried into my work with computers: difficulty often comes from the way something is explained or approached, not from a lack of ability. Looking for the underlying cause rather than accepting the surface is also the habit that draws me to cybersecurity, where understanding how a system really works is essential to understanding how it can fail.",

    "This experience encouraged me to help others. In Junior High School I supported around 25 classmates who were struggling with Mathematics, explaining concepts in ways they could follow. With the permission of their teacher, I also helped mark assignments, which improved my own understanding because teaching a concept forces you to think carefully about how to communicate it. Another important influence was one of my teachers, who had a speech impairment as I do. Even when he struggled to speak, particularly when tense, he taught effectively and made the subject understandable. Watching him showed me that communication is not about perfect delivery; it is about finding a way to connect with the person in front of you. As someone who also experiences difficulty speaking, that example gave me a determination to communicate technical ideas clearly and patiently — a skill I now see as central to cybersecurity, where explaining a risk to someone who is not a specialist matters as much as identifying it.",

    "My interest in Computing began with the same curiosity. I wanted to understand how computers worked, how a browser could display information from the internet and how applications and games operated behind the scenes. That curiosity grew into a serious interest in software development, and I went on to study for a Bachelor of Education in Computer Science, which allowed me to combine Computing and Mathematics with my interest in explaining both to others. The further I went, the clearer it became that building systems and understanding how they can be misused are closely connected. You cannot reason about where a web application places its trust, or where a user might be misled, unless you understand how it is put together.",

    "I now work as a full-stack developer with experience in web development, backend systems and mobile development. I enjoy turning ideas into products that solve practical problems, and I have developed systems and websites for organisations including Remgee Engineering Services Ghana Limited and Architecture and Engineering Services Limited. These projects have strengthened my problem-solving, creativity, communication and organisational skills, and they have taught me to understand what users need before developing a solution. That lesson matters in security too: many risks arise not from exotic technical faults but from the gap between how a system is designed and how people actually use it.",

    "Alongside my development work, I have shared what I know. Between 2022 and 2023 I taught ICT and Elective ICT at West African Senior High School to SHS 2 and SHS 3 students, in classes of roughly 30 to 45, covering introductory programming, web development and the information processing cycle. In 2023 I also taught Mathematics and ICT to JHS 2 and JHS 3 students at Nadat Junior High School for three months. These experiences taught me the value of preparation, patience and adapting an explanation to different levels of understanding. They also showed me that helping someone make sense of something technical is a skill in its own right. I am not making teaching my career; I want to carry that skill into cybersecurity, where documenting findings, explaining risks and helping colleagues use technology safely are part of the work.",

    "My professional experience gives me a practical foundation for that move. Software development requires breaking complicated problems into manageable steps, testing different approaches and learning from mistakes — the same habits that security work depends on. I have explained technical systems to clients and taught a complete beginner HTML, CSS, JavaScript and backend concepts. That reinforced how differently people learn and how an explanation sometimes has to change when the first one does not work. In cybersecurity, the ability to translate a technical detail into something a client or colleague can act on is often what turns a finding into a real improvement.",

    "I am drawn to cybersecurity because computing now shapes how we communicate, access information and solve problems, and that makes the trustworthiness of systems a practical concern rather than an abstract one. I want to work in a field where careful thinking has a direct, protective effect — where understanding a system properly helps keep it reliable and helps the people who depend on it use it with confidence. I also want technology to be something people can understand rather than simply consume, and I believe clear explanation and security awareness are part of that.",

    "The same belief in inclusion that guided my teaching still guides me. I think everyone should have the chance to understand and use technology safely, whatever their starting point. I would bring patience to that work: finding where understanding breaks down, adapting the explanation and recognising when someone needs a different route in, while still setting high standards. I want to help people who assume they are \"not technical\" see that they can be, because confidence and sound judgement are as important in security as specialist knowledge.",

    "I see a good security professional as rigorous, honest about the limits of their knowledge and willing to guide others. Technical skill matters, but so do conduct, communication and attitude — the qualities that make colleagues trust your judgement and act on your advice. Those are the qualities I want to keep developing.",

    "I am seeking a cybersecurity course to build on the technical knowledge and habits I already have. Learning from experienced practitioners and being exposed to structured approaches to security will deepen my understanding of how systems are protected and where they are vulnerable. Ultimately, I want to combine my practical experience in web and software development with focused cybersecurity training to build systems that are more secure and to help people use technology with confidence, curiosity and sound judgement.",
]


def set_run_font(run, size=12, bold=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), "Times New Roman")


doc = Document()

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal_rpr = normal.element.get_or_add_rPr()
normal_rfonts = normal_rpr.find(qn("w:rFonts"))
if normal_rfonts is None:
    normal_rfonts = normal_rpr.makeelement(qn("w:rFonts"), {})
    normal_rpr.insert(0, normal_rfonts)
for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
    normal_rfonts.set(qn(attr), "Times New Roman")

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.line_spacing = 1.5
set_run_font(title_p.add_run(TITLE), size=14, bold=True)

for text in PARAGRAPHS:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    set_run_font(p.add_run(text), size=12)

doc.save(OUTPUT)
print("Saved:", OUTPUT)
