import sys

from PySide6.QtWidgets import QApplication

from exercise_window import ExerciseWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ExerciseWindow()
    main_window.show()
    sys.exit(app.exec())
