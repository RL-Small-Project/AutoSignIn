class CountClassStudents:
    def execute(self, all_students: int, skip_class: int):
        print("應到人數:", all_students)
        print("實到人數:", all_students - skip_class)
