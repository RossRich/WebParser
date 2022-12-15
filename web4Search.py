from flask import Flask, render_template, request, redirect



def search4letters(word: str, letters: str="aeiou") -> set:
  return set(word).intersection(set(letters))

app = Flask(__name__)

# @app.route("/")
# def hello() -> str:
  # return redirect("/entry")

@app.route("/")
@app.route("/entry")
def entry_page() -> str:
  return render_template("entry.html", page_title="Привет, это заголовок")

@app.route("/search4", methods=["POST"])
def do_search() -> str:
  phrase = request.form["phrase"]
  letters = request.form["letters"]
  title = "Результат бесполезного поиска"
  res = search4letters(phrase, letters)
  res = str(res) if len(res) > 0 else "Совпадений нет"
  return render_template("result.html", page_title=title, the_phrase=phrase, the_result=res)

if __name__ == "__main__":
  app.run(debug=True)