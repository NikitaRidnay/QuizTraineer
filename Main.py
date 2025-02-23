import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.questions = self.load_questions('questions.json')
        self.current_question = 0
        self.correct_answers = 0
        self.total_questions = len(self.questions)
        
        self.initUI()
        self.show_question()

    def load_questions(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def initUI(self):
        self.setWindowTitle('Python Quiz Trainer')
        self.setGeometry(300, 300, 600, 400)
        
        # Progress label
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("font-size: 16px; margin: 20px;")
        
        # Answer buttons
        self.option_buttons = []
        self.button_group = QButtonGroup()
        for i in range(4):
            btn = QPushButton()
            btn.setStyleSheet("QPushButton { font-size: 14px; padding: 10px; }")
            btn.clicked.connect(lambda _, idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)
            self.button_group.addButton(btn, i)
        
        # Skip button
        self.skip_btn = QPushButton('Пропустить вопрос')
        self.skip_btn.clicked.connect(self.next_question)
        self.skip_btn.setStyleSheet("background-color: #FFA500; font-size: 14px; padding: 10px;")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.question_label)
        
        options_layout = QVBoxLayout()
        for btn in self.option_buttons:
            options_layout.addWidget(btn)
        
        layout.addLayout(options_layout)
        layout.addWidget(self.skip_btn)
        self.setLayout(layout)
        
    def update_progress(self):
        self.progress_label.setText(
            f"Вопрос {self.current_question + 1}/{self.total_questions} | "
            f"Правильно: {self.correct_answers}"
        )
    
    def show_question(self):
        if self.current_question >= self.total_questions:
            self.question_label.setText("Вопросы закончились!")
            return
            
        question_data = self.questions[self.current_question]
        self.question_label.setText(question_data['question'])
        
        for i, btn in enumerate(self.option_buttons):
            btn.setText(question_data['options'][i])
            btn.setEnabled(True)
            btn.setStyleSheet("")
        
        self.update_progress()
    
    def check_answer(self, selected_idx):
        correct_idx = self.questions[self.current_question]['correct']
        
        for idx, btn in enumerate(self.option_buttons):
            btn.setEnabled(False)
            if idx == correct_idx:
                btn.setStyleSheet("background-color: #90EE90")
            elif idx == selected_idx:
                btn.setStyleSheet("background-color: #FF9999")
        
        if selected_idx == correct_idx:
            self.correct_answers += 1
        
        QTimer.singleShot(1500, self.next_question)
    
    def next_question(self):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.show_question()
        else:
            self.question_label.setText("Тест завершен!\n" + 
                f"Правильных ответов: {self.correct_answers}/{self.total_questions}")
            for btn in self.option_buttons:
                btn.setEnabled(False)
            self.skip_btn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())