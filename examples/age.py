from datetime import date

birth_year = input("Give me your birth year: ")
print("You are (about) {} years old.".format(date.today().year - birth_year))
