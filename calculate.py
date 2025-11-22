from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    targets = None

    if request.method == "POST":
        subject = request.form["subject"]

        # -----------------------------
        # J-TYPE SUBJECT CALCULATION
        # -----------------------------
        if subject in ["FAI", "ML", "RMPE"]:

            ct1_theory = float(request.form["ct1_theory"] or 0)
            ct1_prac = float(request.form["ct1_prac"] or 0)
            ct2_theory = float(request.form["ct2_theory"] or 0)
            ct2_prac = float(request.form["ct2_prac"] or 0)
            llj = float(request.form["llj"] or 0)
            quiz1 = float(request.form["quiz1"] or 0)
            quiz2 = float(request.form["quiz2"] or 0)

            scaled_CT1_theory = (ct1_theory / 40) * 15
            scaled_CT2_theory = (ct2_theory / 40) * 15
            scaled_quiz1 = (quiz1 / 15) * 2.5
            scaled_quiz2 = (quiz2 / 15) * 2.5

            internal_total = (
                scaled_CT1_theory + ct1_prac +
                scaled_CT2_theory + ct2_prac +
                llj + scaled_quiz1 + scaled_quiz2
            )

        # -----------------------------
        # T-TYPE SUBJECT CALCULATION
        # -----------------------------
        elif subject == "IS":
            ct1 = float(request.form["t_ct1_theory"] or 0)
            ct2 = float(request.form["t_ct2_theory"] or 0)
            llj = float(request.form["t_llj"] or 0)
            q1 = float(request.form["t_quiz1"] or 0)
            q2 = float(request.form["t_quiz2"] or 0)

            scaled_CT1 = (ct1 / 40) * 20
            scaled_CT2 = (ct2 / 40) * 20
            scaled_q1 = (q1 / 15) * 5
            scaled_q2 = (q2 / 15) * 5

            internal_total = scaled_CT1 + scaled_CT2 + llj + scaled_q1 + scaled_q2

        result = round(internal_total, 2)

        # Required theory marks (out of 40)
        targets = {}
        for t in [60, 70, 80,90]:
            needed = t - internal_total
            if needed < 0:
                needed = 0
            feasible = needed <= 40

            needed_100 = (needed / 40) * 100

            targets[t] = {
                "needed": round(needed, 2),  # out of 40
                "needed_100": round(needed_100, 2),  # out of 100
                "feasible": feasible

            }

    return render_template("index.html", result=result, targets=targets)


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="10.9.69.230", port=5000, debug=True)