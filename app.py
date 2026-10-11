from flask import Flask, render_template, request, redirect, url_for
from database import get_connection
from datetime import date

app = Flask(__name__)


# ---------------- HOME ----------------

@app.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM lost_report WHERE status = 'ACTIVE'"
    )
    lost_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM found_report WHERE status = 'AVAILABLE'"
    )
    found_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM claim WHERE claim_status = 'PENDING'"
    )
    claim_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        lost_count=lost_count,
        found_count=found_count,
        claim_count=claim_count
    )


# ---------------- REPORT LOST ----------------

@app.route("/report-lost", methods=["GET", "POST"])
def report_lost():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        item_name = request.form["item_name"]
        description = request.form["description"]
        category_id = request.form["category_id"]
        color = request.form["color"]
        student_id = request.form["student_id"]
        location_id = request.form["location_id"]
        lost_date = request.form["lost_date"]

        # Insert item
        cursor.execute("""
            INSERT INTO item
            (item_name, description, category_id, color)
            VALUES (%s, %s, %s, %s)
        """, (
            item_name,
            description,
            category_id,
            color
        ))

        item_id = cursor.lastrowid

        # Insert lost report
        cursor.execute("""
            INSERT INTO lost_report
            (item_id, student_id, location_id, lost_date, status)
            VALUES (%s, %s, %s, %s, 'ACTIVE')
        """, (
            item_id,
            student_id,
            location_id,
            lost_date
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    # Get students
    cursor.execute(
        "SELECT student_id, name FROM student"
    )
    students = cursor.fetchall()

    # Get categories
    cursor.execute(
        "SELECT category_id, category_name FROM category"
    )
    categories = cursor.fetchall()

    # Get locations
    cursor.execute(
        "SELECT location_id, location_name FROM location"
    )
    locations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "report_lost.html",
        students=students,
        categories=categories,
        locations=locations,
        today=date.today()
    )


# ---------------- REPORT FOUND ----------------

@app.route("/report-found", methods=["GET", "POST"])
def report_found():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        item_name = request.form["item_name"]
        description = request.form["description"]
        category_id = request.form["category_id"]
        color = request.form["color"]
        student_id = request.form["student_id"]
        location_id = request.form["location_id"]
        found_date = request.form["found_date"]

        # Insert item
        cursor.execute("""
            INSERT INTO item
            (item_name, description, category_id, color)
            VALUES (%s, %s, %s, %s)
        """, (
            item_name,
            description,
            category_id,
            color
        ))

        item_id = cursor.lastrowid

        # Insert found report
        cursor.execute("""
            INSERT INTO found_report
            (item_id, student_id, location_id, found_date, status)
            VALUES (%s, %s, %s, %s, 'AVAILABLE')
        """, (
            item_id,
            student_id,
            location_id,
            found_date
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    # Get students
    cursor.execute(
        "SELECT student_id, name FROM student"
    )
    students = cursor.fetchall()

    # Get categories
    cursor.execute(
        "SELECT category_id, category_name FROM category"
    )
    categories = cursor.fetchall()

    # Get locations
    cursor.execute(
        "SELECT location_id, location_name FROM location"
    )
    locations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "report_found.html",
        students=students,
        categories=categories,
        locations=locations,
        today=date.today()
    )
# ---------------- SEARCH FOUND ITEMS ----------------

@app.route("/search")
def search():

    search_text = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            fr.found_id,
            i.item_name,
            c.category_name,
            i.color,
            l.location_name,
            fr.found_date,
            s.name AS finder,
            fr.status
        FROM found_report fr
        JOIN item i ON fr.item_id = i.item_id
        JOIN category c ON i.category_id = c.category_id
        JOIN location l ON fr.location_id = l.location_id
        JOIN student s ON fr.student_id = s.student_id
        WHERE fr.status = 'AVAILABLE'
        AND (
            i.item_name LIKE %s
            OR c.category_name LIKE %s
            OR l.location_name LIKE %s
        )
        ORDER BY fr.found_date DESC
    """

    search_pattern = "%" + search_text + "%"

    cursor.execute(
        query,
        (search_pattern, search_pattern, search_pattern)
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "search.html",
        results=results,
        search_text=search_text
    )

# ---------------- SUBMIT CLAIM ----------------

@app.route("/claim", methods=["GET", "POST"])
def submit_claim():

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        found_id = request.form["found_id"]
        student_id = request.form["student_id"]
        claim_date = request.form["claim_date"]

        # Check whether the found item is still available
        cursor.execute("""
            SELECT status
            FROM found_report
            WHERE found_id = %s
        """, (found_id,))

        result = cursor.fetchone()

        if result is None:
            cursor.close()
            connection.close()
            return "Found item does not exist."

        if result[0] != "AVAILABLE":
            cursor.close()
            connection.close()
            return "This item is no longer available for claiming."

        # Insert claim
        cursor.execute("""
            INSERT INTO claim
            (found_id, student_id, claim_date, claim_status)
            VALUES (%s, %s, %s, 'PENDING')
        """, (
            found_id,
            student_id,
            claim_date
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("home"))

    # Get available found items
    cursor.execute("""
        SELECT
            fr.found_id,
            i.item_name,
            c.category_name,
            l.location_name
        FROM found_report fr
        JOIN item i
            ON fr.item_id = i.item_id
        JOIN category c
            ON i.category_id = c.category_id
        JOIN location l
            ON fr.location_id = l.location_id
        WHERE fr.status = 'AVAILABLE'
        ORDER BY fr.found_date DESC
    """)

    found_items = cursor.fetchall()

    # Get students
    cursor.execute("""
        SELECT student_id, name
        FROM student
        ORDER BY name
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "claim.html",
        found_items=found_items,
        students=students,
        today=date.today()
    )

# ---------------- ADMIN VERIFICATION ----------------

@app.route("/admin", methods=["GET", "POST"])
def admin():

    connection = get_connection()
    cursor = connection.cursor()

    # Approve or reject claim
    if request.method == "POST":

        claim_id = request.form["claim_id"]
        decision = request.form["decision"]
        verification_date = date.today()

        # Get the found_id associated with this claim
        cursor.execute("""
            SELECT found_id
            FROM claim
            WHERE claim_id = %s
        """, (claim_id,))

        result = cursor.fetchone()

        if result is None:
            cursor.close()
            connection.close()
            return "Claim not found."

        found_id = result[0]

        if decision == "APPROVED":

            # Update claim
            cursor.execute("""
                UPDATE claim
                SET claim_status = 'APPROVED'
                WHERE claim_id = %s
            """, (claim_id,))

            # Mark item as returned
            cursor.execute("""
                UPDATE found_report
                SET status = 'RETURNED'
                WHERE found_id = %s
            """, (found_id,))

            remarks = "Claim approved and item marked as returned."

        else:

            # Update claim
            cursor.execute("""
                UPDATE claim
                SET claim_status = 'REJECTED'
                WHERE claim_id = %s
            """, (claim_id,))

            remarks = "Claim rejected after verification."

        # Check whether verification already exists
        cursor.execute("""
            SELECT verification_id
            FROM verification
            WHERE claim_id = %s
        """, (claim_id,))

        existing = cursor.fetchone()

        if existing:

            cursor.execute("""
                UPDATE verification
                SET verification_date = %s,
                    decision = %s,
                    remarks = %s
                WHERE claim_id = %s
            """, (
                verification_date,
                decision,
                remarks,
                claim_id
            ))

        else:

            cursor.execute("""
                INSERT INTO verification
                (claim_id, verification_date, decision, remarks)
                VALUES (%s, %s, %s, %s)
            """, (
                claim_id,
                verification_date,
                decision,
                remarks
            ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin"))

    # Get all claims
    cursor.execute("""
        SELECT
            cl.claim_id,
            i.item_name,
            s.name AS claimant,
            cl.claim_date,
            cl.claim_status,
            fr.found_id,
            l.location_name
        FROM claim cl
        JOIN found_report fr
            ON cl.found_id = fr.found_id
        JOIN item i
            ON fr.item_id = i.item_id
        JOIN student s
            ON cl.student_id = s.student_id
        JOIN location l
            ON fr.location_id = l.location_id
        ORDER BY cl.claim_date DESC
    """)

    claims = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin.html",
        claims=claims
    )
# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
