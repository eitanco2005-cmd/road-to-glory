"""Content for the Bar/Bat Mitzvah and Jewish Wedding planners (English, US)."""
import datetime as dt
import random

D = dt.date
TODAY = D(2026, 11, 17)

FIRST_NAMES = ["Cohen", "Levine", "Goldberg", "Katz", "Friedman", "Shapiro", "Rosen", "Klein", "Weiss", "Stern",
               "Adler", "Berman", "Kaplan", "Siegel", "Schwartz", "Miller", "Garcia", "Nguyen", "Patel", "O'Brien",
               "Greenberg", "Horowitz", "Marcus", "Bloom", "Feldman", "Gross", "Hirsch", "Lerner", "Novak", "Roth"]
GIVEN = ["David & Rachel", "Sam & Leah", "Josh & Talia", "Aaron & Miriam", "Ben & Noa", "Dan & Sarah",
         "Grandma Ruth", "Uncle Mike", "Aunt Debbie", "Eli", "Maya", "Ethan", "Noah", "Ava", "Jacob", "Lily"]


def _guests(sides, groups, meals, gift_types, n, seed, kids_bias, gift_pool, tables):
    rnd = random.Random(seed)
    rows = []
    for i in range(n):
        name = f"{rnd.choice(GIVEN)} {rnd.choice(FIRST_NAMES)}"
        side = sides[i % len(sides)]
        group = rnd.choice(groups)
        invited = rnd.choice([1, 2, 2, 2, 3, 4])
        r = rnd.random()
        rsvp = "Attending" if r < .62 else "Declined" if r < .74 else "No reply yet" if r < .94 else "Not invited yet"
        att = invited if rsvp == "Attending" and rnd.random() > .15 else (max(1, invited - 1) if rsvp == "Attending" else None)
        kids = (rnd.choice([0, 0, 1, 2]) if kids_bias else rnd.choice([0, 0, 0, 1])) if att else None
        if kids and att and kids >= att:
            kids = att - 1 or None
        meal = rnd.choice(meals[:3]) if att else None
        table = rnd.randint(1, tables) if att and rnd.random() > .08 else None
        gift = rnd.choice(gift_pool) if rsvp in ("Attending", "Declined") and rnd.random() < .55 else None
        gtype = rnd.choice(gift_types[:3]) if gift else None
        thanks = ("Yes" if rnd.random() < .5 else "No") if gift else None
        rows.append((name, side, group, f"{rnd.randint(10, 999)} Maple St" if i % 3 else f"{name.split()[0].lower()}@example.com",
                     invited, rsvp, att, kids, meal, table, gift, gtype, thanks, None))
    return rows


# --------------------------------------------------------------------------- Bar / Bat Mitzvah
BM_CATEGORIES = [
    ("Venue & catering (party)", .42), ("Kiddush / luncheon after services", .08), ("DJ / band / MC & dancers", .10),
    ("Photo & video", .09), ("Decor, flowers & centerpieces", .06), ("Entertainment & activities", .04),
    ("Invitations, save-the-dates & postage", .02), ("Clothing (whole family)", .04),
    ("Tutor / Hebrew school / synagogue fees", .05), ("Tallit, kippot & Judaica", .02),
    ("Favors / swag / sign-in board", .02), ("Out-of-town guests (hotel block, welcome bags)", .02),
    ("Tzedakah / mitzvah project", .02), ("Contingency (unexpected)", .02),
]
BM_PHASES = ["12–18 months", "9–12 months", "6–9 months", "3–6 months", "1–3 months", "Final 2 weeks", "After"]
BM_TASKS = [
    (BM_PHASES[0], 78, "Get the date assigned by the synagogue (Torah portion / parashah)"),
    (BM_PHASES[0], 74, "Decide the style: Shabbat service + kiddush, evening party, Sunday brunch, Israel trip, or small family event"),
    (BM_PHASES[0], 72, "Set the total budget and a first guest count"),
    (BM_PHASES[0], 70, "Visit venues and book the party venue (check guaranteed minimum)"),
    (BM_PHASES[0], 66, "Book the caterer (kosher supervision level if needed)"),
    (BM_PHASES[1], 52, "Start tutoring / Torah & haftarah portion preparation"),
    (BM_PHASES[1], 50, "Book DJ / band / MC (they book up early on popular weekends)"),
    (BM_PHASES[1], 48, "Book photographer / videographer"),
    (BM_PHASES[1], 46, "Choose a mitzvah project and start it"),
    (BM_PHASES[1], 44, "Reserve a hotel room block for out-of-town guests"),
    (BM_PHASES[2], 36, "Choose the theme, décor and florist"),
    (BM_PHASES[2], 34, "Send save-the-dates (especially for out-of-town family)"),
    (BM_PHASES[2], 30, "Buy or order a tallit (and tefillin if your community uses them)"),
    (BM_PHASES[2], 28, "Plan the kiddush / luncheon with the synagogue"),
    (BM_PHASES[3], 22, "Order invitations (allow time for printing and postage)"),
    (BM_PHASES[3], 20, "Decide aliyot and other honors; ask the people you've chosen"),
    (BM_PHASES[3], 18, "Shop for clothes for the bar/bat mitzvah and the family"),
    (BM_PHASES[3], 16, "Choose the candle-lighting ceremony honorees and songs"),
    (BM_PHASES[3], 14, "Order favors / swag and the sign-in board"),
    (BM_PHASES[4], 9, "Mail invitations (about 8 weeks before)"),
    (BM_PHASES[4], 8, "Write the d'var Torah (speech) with the tutor or rabbi"),
    (BM_PHASES[4], 6, "Plan the slideshow / montage and collect photos"),
    (BM_PHASES[4], 5, "Confirm menu, kids' meals and dietary needs with the caterer"),
    (BM_PHASES[4], 4, "RSVP deadline: chase missing replies"),
    (BM_PHASES[4], 3, "Rehearsal at the synagogue"),
    (BM_PHASES[5], 2, "Final head count to venue and caterer"),
    (BM_PHASES[5], 2, "Seating chart and place cards"),
    (BM_PHASES[5], 1, "Share the day-of schedule with all vendors"),
    (BM_PHASES[5], 1, "Prepare envelopes for vendor tips and final balances"),
    (BM_PHASES[5], 0, "Assign a family member to hold the gift box / cards"),
    (BM_PHASES[6], -1, "Log every gift on the Guests sheet"),
    (BM_PHASES[6], -2, "Pay final vendor balances"),
    (BM_PHASES[6], -4, "Thank-you notes (ideally written by the bar/bat mitzvah)"),
    (BM_PHASES[6], -6, "Deposit checks / decide how gift money is saved or donated"),
]
BM_HONORS = [
    ("Aliyah: first (Kohen)", "Blessings before and after a Torah reading (customs vary by synagogue)"),
    ("Aliyah: second (Levi)", "Blessings over the Torah"),
    ("Aliyah: parents", "Often given to the parents together"),
    ("Aliyah: grandparents", "Grandparents' aliyah"),
    ("Aliyah: other relatives / friends", "Additional aliyot as allowed"),
    ("Maftir", "Usually the bar/bat mitzvah"),
    ("Opening the ark (petichah)", "Opens and closes the ark"),
    ("Hagbah (lifting the Torah)", "Lifts the Torah after the reading"),
    ("Gelilah (dressing the Torah)", "Rolls and dresses the Torah"),
    ("Passing the Torah (l'dor vador)", "Grandparents → parents → bar/bat mitzvah"),
    ("Prayer for the country / for Israel", "English readings"),
    ("Motzi (blessing over challah)", "At the kiddush or party"),
    ("Candle 1", "Candle-lighting ceremony at the party (often 13 candles + 1 for good luck)"),
    ("Candle 2", ""), ("Candle 3", ""), ("Candle 4", ""), ("Candle 5", ""), ("Candle 6", ""), ("Candle 7", ""),
    ("Candle 8", ""), ("Candle 9", ""), ("Candle 10", ""), ("Candle 11", ""), ("Candle 12", ""),
    ("Candle 13", ""), ("Candle 14 (good luck)", "Often the bar/bat mitzvah's own friends or siblings"),
]
BM_DAYOF = [((8, 30), "Family arrives at synagogue; photos with the Torah", "Photographer"),
            ((9, 30), "Shabbat morning service begins", "Rabbi / cantor"),
            ((11, 0), "Torah reading, aliyot, haftarah, d'var Torah", "Bar/bat mitzvah"),
            ((12, 15), "Kiddush luncheon", "Caterer"),
            ((18, 30), "Party: cocktail hour & kids' activities", "Venue / MC"),
            ((19, 15), "Grand entrance & hora", "DJ / band"),
            ((19, 30), "Motzi and dinner served", "Caterer"),
            ((20, 15), "Candle-lighting ceremony", "MC / family"),
            ((20, 45), "Slideshow / montage", "DJ"),
            ((21, 0), "Dancing, games, dessert", "DJ / dancers"),
            ((23, 0), "Last dance; collect gift box", "Family")]

BAR_MITZVAH = dict(
    slug="bar-mitzvah-planner",
    title="Bar / Bat Mitzvah Planner",
    short="Bar/Bat Mitzvah",
    tool_path="tools/bar-mitzvah-budget/",
    intro="Budget, vendors and payments, guest list with RSVPs, gifts and thank-you notes, aliyot and candle-lighting "
          "honors, seating, a timed checklist and a day-of schedule, all in one spreadsheet. The Dashboard keeps score for you.",
    steps=["Open Settings: type the event name, date, total budget and the caterer's price per guest.",
           "Check the Budget sheet: adjust the suggested % split and type your planned amount for each category.",
           "Add vendors as you get quotes; enter the contract total once you book. Log each deposit on Payments.",
           "Build the guest list on Guests (one row per household). Update RSVPs, tables and gifts as they come in.",
           "Work through the Checklist: due dates are counted back from the event date automatically.",
           "Look at the Dashboard any time to see money, RSVPs, overdue payments and what's next."],
    notes=["The candle-lighting list has 14 rows (13 + 1 for good luck); delete the ones you don't need.",
           "Aliyot customs differ between Reform, Conservative and Orthodox synagogues. Ask your rabbi or b'nai mitzvah "
           "coordinator what applies to you."],
    sheets=[("Settings", "Event details and the drop-down lists."),
            ("Dashboard", "Days to go, budget, payments, RSVPs, gifts, thank-yous, checklist progress, charts."),
            ("Budget", "14 categories with a suggested split, planned vs committed vs paid."),
            ("Vendors", "Contacts, status, contract totals, paid and balance."),
            ("Payments", "Deposits and installments with due dates; overdue in red."),
            ("Guests", "Households, side, group, RSVP, attending, kids, meal, table, gift and thank-you."),
            ("Seating", "Tables and seats, filled automatically from the guest list."),
            ("Checklist", "34 tasks from 18 months out to the thank-you notes, with automatic due dates."),
            ("Honors & Candles", "Aliyot, ark opening, hagbah/gelilah, and the candle-lighting ceremony."),
            ("Day-of Schedule", "Run-of-show for the service, kiddush and party.")],
    categories=BM_CATEGORIES,
    sides=["Mom's family", "Dad's family", "Family friends", "Kid's friends", "Synagogue / community"],
    groups=["Immediate family", "Extended family", "School friends", "Camp / youth group", "Sports / clubs",
            "Parents' friends", "Work", "Neighbors", "Synagogue", "Tutor / clergy"],
    gift_types=["Check", "Cash", "Online (Zelle/Venmo)", "Gift card", "Present", "Israel Bond / donation"],
    meals=["Adult meal", "Kids' meal", "Vegetarian", "Vegan", "Gluten-free", "Nut allergy", "Kosher meal (sealed)"],
    tasks=BM_TASKS,
    honors=dict(sheet="Honors & Candles", title="Honors & candle-lighting",
                subtitle="Who gets which honor at the service, and who lights each candle at the party. Track who you've asked "
                         "and who confirmed. Customs vary: check with your synagogue.",
                rows=BM_HONORS, kpi="Honors confirmed"),
    dayof=BM_DAYOF,
    demo=dict(name="Noah's Bar Mitzvah", date=D(2027, 5, 15), venue="Temple Beth Shalom & The Grand Ballroom",
              cap=32000, pp=95, min=120, today=TODAY,
              planned={"Venue & catering (party)": 13500, "Kiddush / luncheon after services": 2400,
                       "DJ / band / MC & dancers": 3200, "Photo & video": 2900, "Decor, flowers & centerpieces": 1800,
                       "Entertainment & activities": 1200, "Invitations, save-the-dates & postage": 650,
                       "Clothing (whole family)": 1300, "Tutor / Hebrew school / synagogue fees": 1800,
                       "Tallit, kippot & Judaica": 450, "Favors / swag / sign-in board": 600,
                       "Out-of-town guests (hotel block, welcome bags)": 500, "Tzedakah / mitzvah project": 700,
                       "Contingency (unexpected)": 1000},
              vendors=[("Venue & catering (party)", "The Grand Ballroom", "Lisa M.", "Booked", 13800),
                       ("Kiddush / luncheon after services", "Shalom Catering", "Avi", "Booked", 2350),
                       ("DJ / band / MC & dancers", "Beat Street DJs", "Marcus", "Booked", 3400),
                       ("Photo & video", "Lens & Light Studio", "Dana", "Booked", 2800),
                       ("Decor, flowers & centerpieces", "Bloom Room", "Kate", "Quote received", None),
                       ("Tutor / Hebrew school / synagogue fees", "Cantor Adler (tutoring)", "Cantor Adler", "Booked", 1600),
                       ("Invitations, save-the-dates & postage", "Paper & Ink", "", "Booked", 620),
                       ("Entertainment & activities", "Photo booth co.", "", "Researching", None)],
              payments=[("The Grand Ballroom", "Deposit", D(2026, 6, 1), 3000, "Paid"),
                        ("The Grand Ballroom", "Second payment", D(2026, 12, 1), 4000, "Due"),
                        ("The Grand Ballroom", "Final balance", D(2027, 5, 8), 6800, "Due"),
                        ("Beat Street DJs", "Deposit", D(2026, 7, 10), 1000, "Paid"),
                        ("Beat Street DJs", "Balance", D(2027, 5, 15), 2400, "Due"),
                        ("Lens & Light Studio", "Retainer", D(2026, 8, 2), 900, "Paid"),
                        ("Lens & Light Studio", "Balance", D(2027, 5, 1), 1900, "Due"),
                        ("Cantor Adler (tutoring)", "Tutoring Sep–Dec", D(2026, 11, 10), 800, "Due"),
                        ("Cantor Adler (tutoring)", "Tutoring Jan–Apr", D(2027, 1, 10), 800, "Due"),
                        ("Shalom Catering", "Deposit", D(2027, 2, 1), 500, "Due"),
                        ("Paper & Ink", "Invitations", D(2027, 2, 20), 620, "Due")],
              guests=None, tables=[("Family", 12), ("Grandparents", 10), ("Mom's cousins", 10), ("Dad's cousins", 10),
                                   ("Kids A", 12), ("Kids B", 12), ("Kids C", 12), ("Parents' friends", 10),
                                   ("Synagogue", 10), ("Work friends", 10), ("Neighbors", 10), ("Camp friends", 12)],
              honors=[("Grandpa Joe", "Yes"), ("Uncle Mike", "Yes"), ("Mom & Dad", "Yes"), ("Grandma Ruth", "Yes"),
                      ("Aunt Debbie & cousins", "No"), ("Noah", "Yes"), ("Sam Katz", "No")]),
)
BAR_MITZVAH["demo"]["guests"] = _guests(BAR_MITZVAH["sides"], BAR_MITZVAH["groups"], BAR_MITZVAH["meals"],
                                        BAR_MITZVAH["gift_types"], 70, 7, True, [36, 54, 72, 100, 108, 180, 180, 250, 360], 12)

# --------------------------------------------------------------------------- Jewish wedding
W_CATEGORIES = [
    ("Venue & catering", .45), ("Photo & video", .11), ("Music: band / DJ (ceremony & reception)", .08),
    ("Flowers, chuppah & decor", .08), ("Attire, hair & makeup", .07), ("Rabbi / officiant & synagogue fees", .02),
    ("Ketubah (artist, calligraphy, frame)", .02), ("Rings", .04), ("Invitations, stationery & postage", .02),
    ("Rehearsal dinner / Shabbat aufruf kiddush", .03), ("Transportation & hotel block", .02),
    ("Favors, welcome bags & sheva brachot meals", .02), ("Tips & gratuities", .02), ("Contingency (unexpected)", .02),
]
W_PHASES = ["12+ months", "9–12 months", "6–9 months", "4–6 months", "2–3 months", "Final month", "After"]
W_TASKS = [
    (W_PHASES[0], 60, "Talk budget with both families; decide who contributes what"),
    (W_PHASES[0], 58, "Choose a rabbi / officiant and discuss the ceremony you want"),
    (W_PHASES[0], 56, "Pick a date: check with your rabbi for dates to avoid (Shabbat, festivals, Sefirat HaOmer, the Three Weeks per your custom)"),
    (W_PHASES[0], 54, "Draft the guest list and a target guest count"),
    (W_PHASES[0], 52, "Book the venue (ceremony + reception) and caterer; check kosher supervision if needed"),
    (W_PHASES[1], 46, "Book photographer / videographer"),
    (W_PHASES[1], 44, "Book band / DJ (ask about hora and chair-lifting experience)"),
    (W_PHASES[1], 42, "Book florist and decide on the chuppah (freestanding or hand-held by four friends)"),
    (W_PHASES[1], 40, "Send save-the-dates"),
    (W_PHASES[1], 38, "Reserve a hotel room block"),
    (W_PHASES[2], 34, "Commission or choose the ketubah (artist lead times can be long)"),
    (W_PHASES[2], 32, "Agree the ketubah text with your rabbi (traditional, egalitarian, interfaith)"),
    (W_PHASES[2], 30, "Wedding dress, suits, tallit/kittel if part of your custom"),
    (W_PHASES[2], 28, "Choose honorees: ketubah witnesses, chuppah holders, sheva brachot readers"),
    (W_PHASES[2], 26, "Pre-marital classes / meetings with the rabbi (if applicable)"),
    (W_PHASES[3], 22, "Buy wedding rings (traditionally a plain band for the ceremony)"),
    (W_PHASES[3], 20, "Order invitations; include ceremony start time (and tisch/bedeken if guests should come early)"),
    (W_PHASES[3], 18, "Plan the aufruf / Shabbat kallah and the rehearsal dinner"),
    (W_PHASES[3], 16, "Book hair & makeup; schedule trials"),
    (W_PHASES[3], 14, "Plan the sheva brachot meals in the week after the wedding (if observing)"),
    (W_PHASES[4], 10, "Mail invitations (6–8 weeks before)"),
    (W_PHASES[4], 9, "Apply for the civil marriage license (check your state's rules and validity window)"),
    (W_PHASES[4], 8, "Schedule mikveh visit (if part of your practice)"),
    (W_PHASES[4], 6, "Finalize menu and tasting; confirm kosher meals for guests who need them"),
    (W_PHASES[4], 5, "Plan the order of the ceremony with your rabbi (processional, circling, blessings)"),
    (W_PHASES[4], 4, "RSVP deadline: follow up on missing replies"),
    (W_PHASES[5], 3, "Final head count to the caterer"),
    (W_PHASES[5], 2, "Seating chart and escort cards"),
    (W_PHASES[5], 2, "Prepare the glass to break, kiddush cup(s), ketubah pen and table for signing"),
    (W_PHASES[5], 1, "Send the day-of schedule to every vendor and the honorees"),
    (W_PHASES[5], 1, "Envelopes for tips and final balances; assign someone to hand them out"),
    (W_PHASES[5], 0, "Plan yichud room (food and drink for the couple after the ceremony)"),
    (W_PHASES[6], -1, "Collect gifts and cards; log them on the Guests sheet"),
    (W_PHASES[6], -2, "Pay final balances"),
    (W_PHASES[6], -4, "Frame the ketubah"),
    (W_PHASES[6], -8, "Thank-you notes; name change paperwork if applicable"),
]
W_HONORS = [
    ("Officiating rabbi / cantor", "Leads the ceremony"),
    ("Ketubah witness 1", "Signs the ketubah. Many rabbis require witnesses who are not related to the couple; ask yours"),
    ("Ketubah witness 2", "Same as above"),
    ("Kiddushin witness(es)", "Witness the ring ceremony (often the same witnesses)"),
    ("Ketubah reader", "Reads the ketubah aloud under the chuppah"),
    ("Chuppah holder 1", "Only if your chuppah is hand-held"),
    ("Chuppah holder 2", ""), ("Chuppah holder 3", ""), ("Chuppah holder 4", ""),
    ("Sheva brachah 1", "Seven blessings, said under the chuppah and at the meal"),
    ("Sheva brachah 2", ""), ("Sheva brachah 3", ""), ("Sheva brachah 4", ""), ("Sheva brachah 5", ""),
    ("Sheva brachah 6", ""), ("Sheva brachah 7 (often the officiant)", ""),
    ("Escorts / unterfirers (partner 1)", "Walk the couple to the chuppah (often parents)"),
    ("Escorts / unterfirers (partner 2)", ""),
    ("Tisch speaker(s)", "Short words of Torah at the tisch before the ceremony"),
    ("Motzi (blessing over challah)", "At the start of the meal"),
    ("Birkat hamazon leader", "Grace after meals; sheva brachot repeated after it"),
    ("Toasts", "Parents, best friends, siblings"),
]
W_DAYOF = [((14, 0), "Photos (first look if you're doing one)", "Photographer"),
           ((15, 30), "Kabbalat panim: tisch & reception for the couple", "Rabbi, close family"),
           ((16, 0), "Ketubah signing with witnesses and rabbi", "Witnesses, rabbi"),
           ((16, 20), "Bedeken (veiling)", "Couple, parents"),
           ((16, 30), "Processional and chuppah ceremony", "Rabbi, honorees, musicians"),
           ((17, 0), "Breaking the glass · Mazel tov!", "Everyone"),
           ((17, 5), "Yichud (a few minutes alone)", "Couple"),
           ((17, 15), "Cocktail hour", "Caterer"),
           ((18, 15), "Grand entrance, hora and chair lifting", "Band / DJ"),
           ((18, 45), "Motzi, dinner, toasts", "Caterer, MC"),
           ((20, 30), "Dancing, mitzvah tanz / shtick", "Band / DJ, friends"),
           ((22, 0), "Birkat hamazon and sheva brachot", "Honorees"),
           ((22, 30), "Send-off", "Everyone")]

WEDDING = dict(
    slug="jewish-wedding-planner",
    title="Jewish Wedding Planner",
    short="Wedding",
    tool_path="guides/jewish-wedding-checklist/",
    intro="Budget, vendors and payments, guest list with RSVPs and gifts, ketubah and chuppah honors (witnesses, sheva "
          "brachot, chuppah holders), seating, a 36-task Jewish wedding checklist and a day-of timeline from tisch to send-off.",
    steps=["Open Settings: type both names, the date, the total budget and the caterer's price per guest.",
           "Adjust the suggested split on the Budget sheet and enter planned amounts.",
           "Add vendors as you get quotes; record deposits and installments on Payments.",
           "Build the guest list (one row per household) and update RSVPs, tables and gifts.",
           "Fill in Ceremony Honors as you ask people: witnesses, chuppah holders, sheva brachot readers.",
           "Use the Checklist and Dashboard every week; share the Day-of Schedule with vendors near the date."],
    notes=["Ceremony details (who may serve as a witness, ketubah text, dates to avoid) vary by movement and community. "
           "Your rabbi has the final word.",
           "Civil marriage license rules differ by state and county. Check your local clerk's office."],
    sheets=[("Settings", "Couple, date, budget, price per guest and drop-down lists."),
            ("Dashboard", "Days to go, budget, payments, RSVPs, gifts, honors, checklist progress, charts."),
            ("Budget", "14 categories including ketubah, chuppah and officiant; planned vs committed vs paid."),
            ("Vendors", "Contacts, status, contract totals, paid and balance."),
            ("Payments", "Deposits and installments with due dates; overdue in red."),
            ("Guests", "Households, side, group, RSVP, attending, meal, table, gift and thank-you."),
            ("Seating", "Tables and seats, filled automatically from the guest list."),
            ("Checklist", "36 Jewish-wedding tasks with automatic due dates."),
            ("Ceremony Honors", "Witnesses, ketubah reader, chuppah holders, sheva brachot, escorts, tisch."),
            ("Day-of Schedule", "Tisch, ketubah signing, bedeken, chuppah, yichud, hora, sheva brachot.")],
    categories=W_CATEGORIES,
    sides=["Partner 1's family", "Partner 2's family", "Partner 1's friends", "Partner 2's friends", "Shared friends"],
    groups=["Immediate family", "Extended family", "College friends", "School friends", "Work", "Synagogue / community",
            "Parents' friends", "Neighbors", "Plus-ones"],
    gift_types=["Check", "Registry gift", "Online (Zelle/Venmo)", "Cash", "Honeymoon fund", "Donation in our honor"],
    meals=["Meat", "Fish", "Vegetarian", "Vegan", "Gluten-free", "Kids' meal", "Glatt kosher (sealed)"],
    tasks=W_TASKS,
    honors=dict(sheet="Ceremony Honors", title="Ceremony honors (kibbudim)",
                subtitle="Who signs, reads, holds and blesses. Track who you've asked and who confirmed. Requirements "
                         "(especially for witnesses) vary: check with your rabbi.",
                rows=W_HONORS, kpi="Honors confirmed"),
    dayof=W_DAYOF,
    demo=dict(name="Rachel & Daniel's Wedding", date=D(2027, 6, 13), venue="Riverside Gardens", cap=48000, pp=135,
              min=150, today=TODAY,
              planned={"Venue & catering": 22000, "Photo & video": 5200, "Music: band / DJ (ceremony & reception)": 4200,
                       "Flowers, chuppah & decor": 3800, "Attire, hair & makeup": 3300,
                       "Rabbi / officiant & synagogue fees": 900, "Ketubah (artist, calligraphy, frame)": 850,
                       "Rings": 1800, "Invitations, stationery & postage": 900,
                       "Rehearsal dinner / Shabbat aufruf kiddush": 1500, "Transportation & hotel block": 800,
                       "Favors, welcome bags & sheva brachot meals": 900, "Tips & gratuities": 950,
                       "Contingency (unexpected)": 900},
              vendors=[("Venue & catering", "Riverside Gardens", "Jenna", "Booked", 23500),
                       ("Photo & video", "Golden Hour Photo", "Eli", "Booked", 4900),
                       ("Music: band / DJ (ceremony & reception)", "Simcha Sound Band", "Yoni", "Booked", 4600),
                       ("Flowers, chuppah & decor", "Petal & Chuppah", "Mara", "Quote received", None),
                       ("Ketubah (artist, calligraphy, frame)", "Jerusalem Ketubah Studio", "", "Booked", 780),
                       ("Rabbi / officiant & synagogue fees", "Rabbi Stern", "Rabbi Stern", "Booked", 900),
                       ("Attire, hair & makeup", "Bridal Atelier", "", "Booked", 2400)],
              payments=[("Riverside Gardens", "Deposit", D(2026, 5, 20), 5000, "Paid"),
                        ("Riverside Gardens", "Second payment", D(2026, 11, 20), 8000, "Due"),
                        ("Riverside Gardens", "Final balance", D(2027, 6, 1), 10500, "Due"),
                        ("Golden Hour Photo", "Retainer", D(2026, 6, 15), 1500, "Paid"),
                        ("Golden Hour Photo", "Balance", D(2027, 5, 30), 3400, "Due"),
                        ("Simcha Sound Band", "Deposit", D(2026, 7, 1), 1500, "Paid"),
                        ("Simcha Sound Band", "Balance", D(2027, 6, 13), 3100, "Due"),
                        ("Jerusalem Ketubah Studio", "Full payment", D(2026, 10, 5), 780, "Paid"),
                        ("Rabbi Stern", "Honorarium", D(2027, 6, 13), 900, "Due"),
                        ("Bridal Atelier", "Dress deposit", D(2026, 10, 1), 1200, "Paid"),
                        ("Bridal Atelier", "Balance", D(2027, 4, 1), 1200, "Due")],
              guests=None, tables=[("Head table", 12)] + [(f"Table {i}", 10) for i in range(2, 17)],
              honors=[("Rabbi Stern", "Yes"), ("Josh Katz", "Yes"), ("Ben Weiss", "Yes"), ("Same as ketubah", "Yes"),
                      ("Aunt Miriam", "No"), ("Sam", "Yes"), ("Leah", "Yes"), ("Noa", "No"), ("Ethan", "Yes")]),
)
WEDDING["demo"]["guests"] = _guests(WEDDING["sides"], WEDDING["groups"], WEDDING["meals"], WEDDING["gift_types"], 90, 21,
                                    False, [100, 150, 180, 200, 250, 360, 500], 16)
