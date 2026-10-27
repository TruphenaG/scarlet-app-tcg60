# Scarlet Roasters

Class website for 33:136:440, Fall 2026.

Student: Truphena Getugi

This website uses the starter project provided for class.

## Page changes

- Home page headline: A Little Scarlet in Every Sip.
- About page: Site built by Truphena Getugi, 33:136:440, Fall 2026.

The Home page is in `templates/pages/home.html`.
The About page is in `templates/pages/about.html`.

The other website files come from the class starter project.

## Week 7 Status page

The models, Admin registrations, Status view/template, URL route, and schema
v1.1 SQL come from the instructor's `week7-files.zip`. The checker reads the
database; its expected counts and validation logic have not been changed.

Public submission URL: https://scarlet-app-tcg60.vercel.app/status/

### Finish the database connection

1. Use the existing class Neon PostgreSQL database containing the original
   eleven tables and class data. This ZIP does not contain `schema_v1.sql`
   or the original data import files. Do not create empty replacement tables.
2. In Vercel's **Production** environment, set `STUDENT_NETID` to `tcg60`,
   `DATABASE_URL` to that database's connection string, and `SECRET_KEY` to
   a private random value. Keep database credentials out of Git and chat.
   Copy `.env.example` to `.env` or `.env.local` for local configuration.
3. Check whether `order_lines` already has `line_id` as its primary key and
   a unique constraint on `(order_no, line_no)`. If the database is still
   schema v1.0, run the instructor's `sql/v1_1_order_lines.sql` **once** in
   the Neon SQL Editor, inside a transaction. Do not rerun it against v1.1.
4. Run `python manage.py migrate` against the intended database for Django's
   own auth/session/Admin tables. The eleven class models use
   `managed = False`, so this does not create or seed those tables.
   Create an Admin account with `python manage.py createsuperuser` if needed.
5. Redeploy after setting the Vercel environment variables. Open the public
   `/status/` URL signed out and verify `tcg60`, **11 of 11 tables in order**,
   all table matches, all Admin checkmarks, and the order-line inline check.

Expected counts: customers 92; addresses 93; employees 5; coffees 8;
products 25; inventory 25; sales_orders 987; order_lines 2660;
shipments 941; invoices 729; payments 896.

The Status page remains readable when a database is missing or unavailable;
it reports the failure instead of claiming the requirements pass.

### Local checks

Install `requirements.txt`, then run `python manage.py check`.
For tests using a disposable local SQLite database, run
`python manage.py test --settings=django_project.test_settings`.
These tests check routing, missing-database reporting and Admin registration;
the deployed PostgreSQL data must still be verified separately.
