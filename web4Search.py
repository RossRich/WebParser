from flask import Flask, render_template, request, redirect, session
import check_logged
import datetime

log_file_name: str = "parser_log.log"


def search4letters(word: str, letters: str = "aeiou") -> set:
    return set(word).intersection(set(letters))


def log_request(req: str, res: str) -> None:
    try:
        with open(log_file_name, "a") as logs:
            line_for_write: str = "{0} - req: {1}; res: {2}\n"
            logs.write(line_for_write.format(
                datetime.datetime.now(), req, res))
    except OSError:
        print("[{0}] Failed to open file {1}".format(
            log_request.__name__, log_file_name))


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
    log_request("phrase-{0} letter-{1}".format(phrase, letters), res)
    return render_template("result.html", page_title=title, the_phrase=phrase, the_result=res)


@app.route("/viewlog")
def view_log() -> str:
    res: str = ""
    try:
        with open(log_file_name, "r") as logs:
            title: str = "<dt>{0}</dt>"
            des: str = "<dd>{0}</dd>"
            for log in logs:
                data_list = str.split(log, " - ")
                # print(data_list)
                res += title.format(data_list[0]) + des.format(data_list[1])
    except OSError:
        print("[{0}] Failed to open file {1}".format(
            log_request.__name__, log_file_name))

    return render_template("viewlog.html", page_title="View log", list_log=res)


@app.route("/login")
def do_login() -> str:
    session["logged_in"] = True
    print(session)
    return "Теперь вы в системе"


@app.route("/status")
@check_logged.check_logged_in
def get_status() -> str:
    msg_logged = "Вы вошли в систему под именем: {0}"
    # msg_not_logged = "Вы не вошли в систему"
    return msg_logged.format("")


@app.route("/logout")
@check_logged.check_logged_in
def do_logout() -> str:
    if session["logged_in"]:
        session["logged_in"] = False

    return str(True)


if __name__ == "__main__":
    app.secret_key = "TheSecretKey"
    app.run(debug=True)
    session.setdefault("logged_in", False)
