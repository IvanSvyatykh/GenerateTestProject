import os
from openpyxl import Workbook
from docx import Document
from fpdf import FPDF
from datetime import datetime
import json


async def generate_docx(test_json, subject, user_id):
    if isinstance(test_json, str):
        try:
            test_json = json.loads(test_json)
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON")

    if not isinstance(test_json, dict) or 'questions' not in test_json:
        raise ValueError("test_json должен содержать ключ 'questions'")

    questions = test_json['questions']

    document = Document()
    document.add_heading(f"Тема теста: {subject}", level=1)

    for idx, question in enumerate(questions, 1):
        if not isinstance(question, dict) or 'question' not in question or 'answers' not in question or 'correct_answer' not in question:
            raise ValueError("Каждый вопрос должен быть словарем с ключами 'question', 'answers', и 'correct_answer'")

        document.add_paragraph(f"{idx}. {question['question']}")
        for answer in question['answers']:
            document.add_paragraph(f"   - {answer}")

    document.add_page_break()
    document.add_heading("Ответы на тест:", level=1)
    for idx, question in enumerate(questions, 1):
        document.add_paragraph(f"{idx}. Ответ: {question['correct_answer']}")

    directory = "./tests/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"tests/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    document.save(file_path)

    return file_path


async def generate_pdf(test_json, subject, user_id):
    if isinstance(test_json, str):
        try:
            test_json = json.loads(test_json)
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON")

    if not isinstance(test_json, dict) or 'questions' not in test_json:
        raise ValueError("test_json должен содержать ключ 'questions'")

    questions = test_json['questions']

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', '', 'ttf/Arial-Unicode-Regular.ttf', uni=True)
    pdf.set_font('ArialUnicode', size=12)

    pdf.cell(200, 10, txt=f"Тема теста: {subject[1:].strip()}", ln=True, align="C")

    for idx, question in enumerate(questions, 1):
        pdf.cell(200, 10, txt=f"{idx}. {question['question']}", ln=True)
        for answer in question['answers']:
            pdf.cell(200, 10, txt=f"   - {answer}", ln=True)

    pdf.add_page()
    pdf.cell(200, 10, txt="Ответы на тест:", ln=True, align="C")
    for idx, question in enumerate(questions, 1):
        pdf.cell(200, 10, txt=f"{idx}. Ответ: {question['correct_answer']}", ln=True)

    directory = "./tests/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"tests/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(file_path)

    return file_path


async def generate_excel(test_json, subject, user_id):
    if isinstance(test_json, str):
        try:
            test_json = json.loads(test_json)
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON")

    if not isinstance(test_json, dict) or 'questions' not in test_json:
        raise ValueError("test_json должен содержать ключ 'questions'")

    questions = test_json['questions']

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Тест"

    sheet["A1"] = f"Тема теста: {subject}"

    for idx, question in enumerate(questions, 1):
        sheet.append([f"{idx}. {question['question']}"])
        for answer in question['answers']:
            sheet.append([f"   - {answer}"])

    directory = "./tests/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    sheet.append(["Ответы на тест:"])
    for idx, question in enumerate(questions, 1):
        sheet.append([f"{idx}. Ответ: {question['correct_answer']}"])

    file_path = f"tests/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    workbook.save(file_path)

    return file_path
