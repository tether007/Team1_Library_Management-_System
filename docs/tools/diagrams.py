"""Draws every diagram used in the project guide PDF as a PNG in docs/images.

Run:  python docs/tools/diagrams.py
Style follows the app: black outlines, flat offset shadows, white and light-yellow fills.
Coordinates: 1 unit = 0.1 inch.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text
from matplotlib.patches import Polygon, Rectangle

OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(exist_ok=True)

WHITE, YELLOW, GREEN, RED, PAPER, BLUE = "#ffffff", "#fff6c2", "#d9f2d9", "#f8d7d7", "#f4f4f0", "#dbe8f7"
MONO = "DejaVu Sans Mono"


SCALE = 0.55      # physical size of one drawing unit in inches * 10 (smaller = text looks larger on the page)
FONT = 1.12       # extra font growth applied to every label so text stays readable when the PDF shrinks the image


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w / 10 * SCALE, h / 10 * SCALE), dpi=220)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def save(fig, name):
    for t in fig.findobj(matplotlib.text.Text):
        t.set_fontsize(t.get_fontsize() * FONT)
    fig.savefig(OUT / name, facecolor="white")
    plt.close(fig)
    print("wrote", name)


def box(ax, cx, cy, w, h, text, fc=WHITE, size=8, bold=False, shadow=True, mono=False, ls="-"):
    x, y = cx - w / 2, cy - h / 2
    if shadow:
        ax.add_patch(Rectangle((x + 0.7, y - 0.7), w, h, fc="black", ec="black", lw=0, zorder=1))
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="black", lw=1.3, ls=ls, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, zorder=3,
            fontweight="bold" if bold else "normal", family=MONO if mono else "DejaVu Sans", linespacing=1.3)
    return dict(l=x, r=x + w, t=y + h, b=y, cx=cx, cy=cy)


def arrow(ax, p1, p2, label=None, ls="-", size=7, lpos=0.5, loff=(0, 0), style="-|>"):
    ax.annotate("", xy=p2, xytext=p1, zorder=4,
                arrowprops=dict(arrowstyle=style, lw=1.2, color="black", ls=ls, shrinkA=0, shrinkB=0))
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + loff[0]
        my = p1[1] + (p2[1] - p1[1]) * lpos + loff[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=size, zorder=5,
                bbox=dict(fc="white", ec="none", pad=1.2))


def route(ax, pts, label=None, label_at=0, size=7):
    """Polyline with an arrow head on the last segment. label_at = index of the segment to label."""
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="black", lw=1.2, zorder=4)
    arrow(ax, pts[-2], pts[-1])
    if label:
        a, b = pts[label_at], pts[label_at + 1]
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 2, label, ha="center", fontsize=size,
                bbox=dict(fc="white", ec="none", pad=1), zorder=6)


def poly(ax, pts, fc=WHITE):
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec="black", lw=1.3, zorder=2))


def diamond(ax, cx, cy, w, h, text, size=7):
    poly(ax, [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], YELLOW)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, zorder=3, linespacing=1.2)
    return dict(l=cx - w / 2, r=cx + w / 2, t=cy + h / 2, b=cy - h / 2, cx=cx, cy=cy)


def terminal(ax, cx, cy, text, filled=True):
    ax.add_patch(plt.Circle((cx, cy), 1.6 if filled else 2.0, fc="black" if filled else "white", ec="black", lw=1.3, zorder=3))
    if not filled:
        ax.add_patch(plt.Circle((cx, cy), 1.0, fc="black", ec="black", zorder=4))
    ax.text(cx + 3.2, cy, text, va="center", fontsize=7)
    return dict(l=cx - 2, r=cx + 2, t=cy + 2, b=cy - 2, cx=cx, cy=cy)


def class_box(ax, x, ytop, w, name, fields=(), methods=(), stereo=None, fc=WHITE):
    lh = 1.9
    head = 4.6 if stereo else 3.2
    h = head + max(len(fields), 1) * lh + 1.2 + (max(len(methods), 1) * lh + 1.2 if methods else 0)
    y = ytop - h
    ax.add_patch(Rectangle((x + 0.7, y - 0.7), w, h, fc="black", lw=0, zorder=1))
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="black", lw=1.3, zorder=2))
    ax.add_patch(Rectangle((x, ytop - head), w, head, fc=YELLOW, ec="black", lw=1.3, zorder=2))
    if stereo:
        ax.text(x + w / 2, ytop - 1.4, f"<<{stereo}>>", ha="center", va="center", fontsize=6.5, style="italic", zorder=3)
        ax.text(x + w / 2, ytop - 3.3, name, ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=3)
    else:
        ax.text(x + w / 2, ytop - head / 2, name, ha="center", va="center", fontsize=8.5, fontweight="bold", zorder=3)
    cy = ytop - head - 1.4
    for f in fields or [" "]:
        ax.text(x + 1.2, cy, f, ha="left", va="center", fontsize=6.8, family=MONO, zorder=3)
        cy -= lh
    if methods:
        ax.plot([x, x + w], [cy + lh / 2 + 0.2] * 2, color="black", lw=1.0, zorder=3)
        cy -= 0.4
        for m in methods:
            ax.text(x + 1.2, cy, m, ha="left", va="center", fontsize=6.8, family=MONO, zorder=3)
            cy -= lh
    return dict(l=x, r=x + w, t=ytop, b=y, cx=x + w / 2, cy=y + h / 2)


# ---------------------------------------------------------------- 1. architecture
def architecture():
    fig, ax = canvas(170, 100)
    ax.text(85, 96, "System architecture (how the pieces run together)", ha="center", fontsize=11, fontweight="bold")

    ax.add_patch(Rectangle((3, 28), 52, 60, fc=PAPER, ec="black", lw=1.3, ls="--", zorder=0))
    ax.text(29, 85, "Browser  (http://localhost:5173)", ha="center", fontsize=8, fontweight="bold")
    box(ax, 29, 74, 44, 8, "React 19 components\n(pages, forms, tables)", size=7.5)
    box(ax, 29, 61, 44, 8, "Redux Toolkit store\n(auth, books, members, nav, notice)", size=7.5)
    box(ax, 29, 48, 44, 8, "axios client + interceptors\n(adds Basic header, handles 401)", size=7.5)
    box(ax, 17, 34, 20, 7, "sessionStorage\n(login token)", fc=YELLOW, size=6.5)
    box(ax, 42, 34, 22, 7, "localStorage\n(cached lists)", fc=YELLOW, size=6.5)
    arrow(ax, (29, 70), (29, 65))
    arrow(ax, (29, 57), (29, 52))

    box(ax, 72, 48, 16, 12, "Vite dev\nserver\nproxy\n/api -> :8080", fc=BLUE, size=6.8)
    arrow(ax, (51, 48), (64, 48), "HTTP + JSON", size=6.5, loff=(0, 3))
    route(ax, [(72, 54), (72, 76), (88, 76)], "forwarded", label_at=1)

    ax.add_patch(Rectangle((84, 8), 82, 80, fc=PAPER, ec="black", lw=1.3, ls="--", zorder=0))
    ax.text(125, 85, "Spring Boot 4  (http://localhost:8080, Java 21)", ha="center", fontsize=8, fontweight="bold")
    box(ax, 120, 76, 62, 7, "Spring Security filter chain:\nHTTP Basic -> UserDetailsService -> BCrypt -> role rules", fc=YELLOW, size=6.6)
    box(ax, 120, 64, 62, 7, "Controllers (@RestController)\nmap URL + JSON to Java methods", size=6.8)
    svc = box(ax, 120, 52, 62, 7, "Services (@Service)\nbusiness rules, @Transactional, @Cacheable", size=6.8)
    box(ax, 120, 40, 62, 7, "Repositories\n(Spring Data JPA interfaces)", size=6.8)
    box(ax, 120, 26, 62, 8, "H2 in-memory database\ntables: books, members, app_users\nrecreated and seeded at every start", fc=GREEN, size=6.6)
    cache = box(ax, 158, 52, 14, 12, "Spring\ncache\n'books'", fc=BLUE, size=6.5)
    arrow(ax, (svc["r"], 52), (cache["l"], 52), style="<|-|>")
    box(ax, 100, 14, 30, 6, "GlobalExceptionHandler\n(errors -> JSON)", size=6.5)
    box(ax, 140, 14, 30, 6, "DataSeeder\n(demo data at startup)", size=6.5)
    arrow(ax, (120, 72.5), (120, 67.5))
    arrow(ax, (120, 60.5), (120, 55.5))
    arrow(ax, (120, 48.5), (120, 43.5))
    arrow(ax, (120, 36.5), (120, 30))
    ax.text(125, 3, "Everything on the right is in memory: stop the server and the data is gone.", ha="center", fontsize=7, style="italic")
    save(fig, "architecture.png")


# ---------------------------------------------------------------- 2. domain class diagram
def class_domain():
    fig, ax = canvas(150, 92)
    ax.text(75, 88, "Class diagram: domain model (package model)", ha="center", fontsize=11, fontweight="bold")
    person = class_box(ax, 55, 82, 40, "Person", ["- Long id", "- String name"], ["+ getId()", "+ getName()"], stereo="abstract, @MappedSuperclass")
    member = class_box(ax, 8, 52, 46, "Member", ["- MemberType type"], ["+ getType()", "+ getBorrowLimit()"], stereo="@Entity  table members")
    appuser = class_box(ax, 98, 52, 48, "AppUser", ["- String username", "- String passwordHash", "- Role role"], ["+ getUsername()", "+ getRole()"], stereo="@Entity  table app_users")
    book = class_box(ax, 8, 24, 52, "Book", ["- Long id", "- String title", "- String author", "- String isbn (unique)", "- Member borrower"],
                     ["+ issueTo(Member)", "+ markReturned()", "+ isAvailable()"], stereo="@Entity  table books")
    mtype = class_box(ax, 78, 28, 30, "MemberType", ["STUDENT(3)", "FACULTY(5)"], ["+ getBorrowLimit()"], stereo="enum", fc=BLUE)
    role = class_box(ax, 114, 28, 32, "Role", ["ADMIN", "LIBRARIAN", "MEMBER"], None, stereo="enum", fc=BLUE)
    # inheritance (hollow triangle drawn as arrow)
    arrow(ax, (member["cx"], member["t"]), (62, person["b"] - 0.2), "extends", size=7)
    arrow(ax, (appuser["cx"], appuser["t"]), (88, person["b"] - 0.2), "extends", size=7)
    arrow(ax, (member["cx"], book["t"]), (member["cx"], member["b"]), "borrower  0..1", size=7, loff=(11, 0))
    arrow(ax, (member["r"], member["cy"] - 6), (mtype["l"], mtype["t"] - 3), "type", size=7)
    arrow(ax, (appuser["cx"] + 8, appuser["b"]), (role["cx"], role["t"]), "role", size=7)
    ax.text(112, 8, "Many books can point to one member;\na book is available when its borrower is empty.", ha="center", fontsize=7, style="italic")
    save(fig, "class_domain.png")


# ---------------------------------------------------------------- 3. layers class diagram
def class_layers():
    fig, ax = canvas(170, 100)
    ax.text(85, 96, "Class diagram: layers and dependencies (constructor injection)", ha="center", fontsize=11, fontweight="bold")
    cols = [10, 62, 114]
    ax.text(30, 91, "Controllers", ha="center", fontsize=8.5, fontweight="bold")
    ax.text(82, 91, "Services", ha="center", fontsize=8.5, fontweight="bold")
    ax.text(134, 91, "Repositories", ha="center", fontsize=8.5, fontweight="bold")
    c_auth = box(ax, 30, 82, 40, 6, "AuthController\nGET /api/auth/me", size=6.8)
    c_book = box(ax, 30, 68, 40, 6, "BookController\n/api/books", size=6.8)
    c_mem = box(ax, 30, 54, 40, 6, "MemberController\n/api/members", size=6.8)
    c_bor = box(ax, 30, 40, 40, 6, "BorrowController\n/api/borrow/*", size=6.8)
    s_book = box(ax, 82, 68, 40, 8, "BookService\nsearch() @Cacheable\nadd() @CacheEvict", size=6.8)
    s_mem = box(ax, 82, 54, 40, 6, "MemberService\nlist(), add()", size=6.8)
    s_bor = box(ax, 82, 40, 40, 8, "BorrowService\nissue(), giveBack()\n@CacheEvict", size=6.8)
    s_usr = box(ax, 82, 82, 40, 6, "DatabaseUserDetailsService\nloadUserByUsername()", size=6.5)
    r_book = box(ax, 134, 54, 40, 8, "BookRepository\nfindBy...Containing...\ncountByBorrowerId()", fc=GREEN, size=6.5)
    r_mem = box(ax, 134, 38, 40, 6, "MemberRepository", fc=GREEN, size=6.8)
    r_usr = box(ax, 134, 82, 40, 6, "AppUserRepository\nfindByUsername()", fc=GREEN, size=6.5)
    arrow(ax, (c_book["r"], 68), (s_book["l"], 68))
    arrow(ax, (c_mem["r"], 54), (s_mem["l"], 54))
    arrow(ax, (c_bor["r"], 40), (s_bor["l"], 40))
    arrow(ax, (s_book["r"], 66), (r_book["l"], 57))
    arrow(ax, (s_mem["r"], 54), (r_book["l"], 54))
    arrow(ax, (s_bor["r"], 42), (r_book["l"], 52))
    arrow(ax, (s_bor["r"], 38), (r_mem["l"], 39))
    arrow(ax, (s_mem["r"], 52), (r_mem["l"], 40))
    arrow(ax, (s_usr["r"], 82), (r_usr["l"], 82))
    ax.text(30, 28, "AuthController has no service:\nSpring Security has already\nverified the credentials\nbefore the method runs.", ha="center", va="top", fontsize=6.5, style="italic")
    box(ax, 134, 20, 58, 14, "Spring creates every box above once\n(a bean) and passes it into the\nconstructor of the class that needs it.\nNo class calls new on a service.", fc=YELLOW, size=6.6)
    box(ax, 82, 20, 52, 14, "Also injected:\nSecurityConfig -> SecurityErrorHandler\nDataSeeder -> 3 repositories\n+ PasswordEncoder", size=6.3)
    save(fig, "class_layers.png")


# ---------------------------------------------------------------- 4. exceptions
def class_exceptions():
    fig, ax = canvas(170, 82)
    ax.text(85, 78, "Class diagram: exceptions and the handler", ha="center", fontsize=11, fontweight="bold")
    rte = box(ax, 85, 68, 40, 6, "RuntimeException (Java)", size=7.5)
    lib = class_box(ax, 62, 62, 46, "LibraryException", ["- HttpStatus status"], ["+ getStatus()"], stereo="abstract")
    arrow(ax, (85, lib["t"]), (85, rte["b"] - 0.2))
    names = [("BookNotFound\nException", "404", RED), ("MemberNotFound\nException", "404", RED),
             ("BookNotAvailable\nException", "409", YELLOW), ("BorrowLimit\nExceededException", "409", YELLOW),
             ("BookNotIssued\nException", "409", YELLOW), ("DuplicateIsbn\nException", "409", YELLOW)]
    xs = [16 + i * 27 for i in range(6)]
    for x, (n, code, fc) in zip(xs, names):
        b = box(ax, x, 22, 24, 9, f"{n}\nHTTP {code}", fc=fc, size=6.5)
        arrow(ax, (x, b["t"]), (85, lib["b"] - 0.2))
    box(ax, 85, 7, 130, 11, "GlobalExceptionHandler (@RestControllerAdvice) catches LibraryException\nand returns { \"message\": ... } with the exception's own status.\n"
        "It also maps validation errors, unreadable JSON and bad sort fields to 400.", fc=GREEN, size=6.6)
    save(fig, "class_exceptions.png")


# ---------------------------------------------------------------- 5. sequence: issue a book
def seq(ax, parts, xs, top, bottom):
    for p, x in zip(parts, xs):
        box(ax, x, top, 21, 6, p, fc=YELLOW, size=6.8, bold=True)
        ax.plot([x, x], [top - 3, bottom], color="black", lw=0.9, ls="--", zorder=0)


def sequence_issue():
    fig, ax = canvas(190, 120)
    ax.text(95, 116, "Sequence diagram: issuing a book  (POST /api/borrow/issue)", ha="center", fontsize=11, fontweight="bold")
    parts = ["BorrowPage\n(React)", "axios +\nRedux thunk", "Security\nfilter chain", "BorrowController", "BorrowService", "Repositories\n(JPA)", "Spring cache"]
    xs = [14, 40, 66, 92, 118, 146, 174]
    seq(ax, parts, xs, 108, 19)
    msgs = [
        (0, 1, 100, "1. click 'Issue book'  -> dispatch(issueBook)"),
        (1, 2, 93, "2. POST /api/borrow/issue + Basic header"),
        (2, 2, 86, "3. verify password (BCrypt), check role"),
        (2, 3, 80, "4. allowed: ADMIN / LIBRARIAN"),
        (3, 4, 73, "5. issue(IssueRequest)  after @Valid"),
        (4, 5, 66, "6. findById(book), findById(member)"),
        (4, 5, 60, "7. countByBorrowerId(member)"),
        (4, 4, 54, "8. rules: available? under limit?"),
        (4, 5, 48, "9. book.issueTo(member) -> UPDATE on commit"),
        (4, 6, 42, "10. @CacheEvict clears 'books'"),
        (4, 3, 36, "11. BookResponse"),
        (3, 1, 30, "12. 200 + JSON {available:false,...}"),
        (1, 0, 23, "13. Redux replaces the book -> row shows 'Issued'"),
    ]
    for a, b, y, label in msgs:
        if a == b:
            ax.annotate("", xy=(xs[a] + 1, y - 2), xytext=(xs[a] + 1, y), arrowprops=dict(arrowstyle="-|>", lw=1.1))
            ax.text(xs[a] + 4, y - 1, label, fontsize=6.5, va="center")
        else:
            arrow(ax, (xs[a], y), (xs[b], y), style="-|>")
            ax.text((xs[a] + xs[b]) / 2, y + 1.8, label, fontsize=6.5, ha="center",
                    bbox=dict(fc="white", ec="none", pad=0.8), zorder=6)
    box(ax, 95, 9, 150, 9, "If a rule fails (step 8), a LibraryException is thrown, the transaction\nrolls back, GlobalExceptionHandler returns 409 { \"message\": ... }\nand the UI shows the message in the red banner.", fc=RED, size=6.5)
    save(fig, "sequence_issue.png")


# ---------------------------------------------------------------- 6. activity flows
def flow_signin():
    fig, ax = canvas(150, 112)
    ax.text(75, 108, "Activity diagram: sign in", ha="center", fontsize=11, fontweight="bold")
    terminal(ax, 40, 100, "Start")
    a = box(ax, 40, 90, 50, 7, "Open the app", size=7.5)
    d0 = diamond(ax, 40, 78, 44, 11, "Session already\nin sessionStorage?")
    b = box(ax, 40, 62, 50, 7, "Show login page, user types\nusername and password", size=7)
    c = box(ax, 40, 50, 50, 7, "GET /api/auth/me\nwith Basic header", size=7)
    d1 = diamond(ax, 40, 37, 44, 11, "Credentials match\nthe database?")
    e = box(ax, 40, 22, 50, 7, "Backend returns {username, role}\nfront end saves session", size=7)
    f = box(ax, 40, 11, 50, 6, "Show tabs allowed for the role", size=7)
    err = box(ax, 112, 37, 44, 9, "401: show red banner\n'Invalid username or password.'", fc=RED, size=7)
    arrow(ax, (40, 98.4), (40, a["t"]))
    arrow(ax, (40, a["b"]), (40, d0["t"]))
    arrow(ax, (40, d0["b"]), (40, b["t"]), "No", loff=(3, 0))
    # session already present: skip the form, go straight to showing the tabs
    route(ax, [(d0["r"], 78), (135, 78), (135, 11), (f["r"], 11)], "Yes", label_at=0)
    arrow(ax, (40, b["b"]), (40, c["t"]))
    arrow(ax, (40, c["b"]), (40, d1["t"]))
    arrow(ax, (40, d1["b"]), (40, e["t"]), "Yes", loff=(3, 0))
    arrow(ax, (d1["r"], 37), (err["l"], 37), "No")
    # wrong credentials: back to the login form
    route(ax, [(err["cx"], err["t"]), (err["cx"], 62), (b["r"], 62)])
    arrow(ax, (40, e["b"]), (40, f["t"]))
    terminal(ax, 40, 3, "End", filled=False)
    arrow(ax, (40, f["b"]), (40, 5))
    save(fig, "flow_signin.png")


def flow_issue():
    fig, ax = canvas(150, 128)
    ax.text(75, 124, "Activity diagram: issue a book", ha="center", fontsize=11, fontweight="bold")
    terminal(ax, 40, 116, "Start")
    box(ax, 40, 106, 56, 7, "Librarian picks a book and a member,\nclicks 'Issue book'", size=7)
    d1 = diamond(ax, 40, 92, 44, 11, "Logged in as ADMIN\nor LIBRARIAN?")
    d2 = diamond(ax, 40, 76, 44, 11, "Book and member\nexist?")
    d3 = diamond(ax, 40, 60, 44, 11, "Book available?")
    d4 = diamond(ax, 40, 44, 50, 11, "Member holds fewer than the\nlimit (student 3, faculty 5)?")
    ok = box(ax, 40, 28, 56, 7, "book.issueTo(member), clear cache\nreturn 200 with the updated book", fc=GREEN, size=7)
    ui = box(ax, 40, 16, 56, 6, "UI shows the book as 'Issued'", size=7)
    terminal(ax, 40, 6, "End", filled=False)
    arrow(ax, (40, 114.4), (40, 109.5))
    arrow(ax, (40, 102.5), (40, d1["t"]))
    arrow(ax, (40, d1["b"]), (40, d2["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, d2["b"]), (40, d3["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, d3["b"]), (40, d4["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, d4["b"]), (40, ok["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, ok["b"]), (40, ui["t"]))
    arrow(ax, (40, ui["b"]), (40, 8))
    errs = [(92, "403 Forbidden / 401", d1), (76, "404 'Book not found.' or\n'Invalid member.'", d2),
            (60, "409 '\"title\" is not available.'", d3), (44, "409 'name has reached the\nborrow limit of N.'", d4)]
    for y, t, d in errs:
        e = box(ax, 120, y, 50, 8, t, fc=RED, size=6.8)
        arrow(ax, (d["r"], y), (e["l"], y), "No")
    ax.text(120, 30, "Any failure: nothing is changed\n(transaction rolls back) and the\nmessage is shown in the banner.", ha="center", fontsize=7, style="italic")
    save(fig, "flow_issue.png")


def flow_return():
    fig, ax = canvas(150, 92)
    ax.text(75, 88, "Activity diagram: return a book", ha="center", fontsize=11, fontweight="bold")
    terminal(ax, 40, 80, "Start")
    box(ax, 40, 70, 56, 7, "Librarian clicks 'Return' on an issued book", size=7)
    d1 = diamond(ax, 40, 56, 44, 11, "ADMIN or LIBRARIAN?")
    d2 = diamond(ax, 40, 41, 44, 11, "Book exists?")
    d3 = diamond(ax, 40, 26, 44, 11, "Book currently issued?")
    ok = box(ax, 40, 12, 56, 7, "book.markReturned(), clear cache\nreturn 200", fc=GREEN, size=7)
    terminal(ax, 40, 2, "End", filled=False)
    arrow(ax, (40, 78.4), (40, 73.5))
    arrow(ax, (40, 66.5), (40, d1["t"]))
    arrow(ax, (40, d1["b"]), (40, d2["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, d2["b"]), (40, d3["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, d3["b"]), (40, ok["t"]), "Yes", loff=(3, 0))
    arrow(ax, (40, ok["b"]), (40, 4))
    for y, t, d in [(56, "401 / 403", d1), (41, "404 'Book not found.'", d2), (26, "409 '\"title\" was not issued.'", d3)]:
        e = box(ax, 115, y, 46, 7, t, fc=RED, size=6.8)
        arrow(ax, (d["r"], y), (e["l"], y), "No")
    save(fig, "flow_return.png")


def flow_list_books():
    fig, ax = canvas(160, 118)
    ax.text(80, 114, "Activity diagram: list books (paging, sorting, two caches)", ha="center", fontsize=11, fontweight="bold")
    terminal(ax, 40, 106, "Start")
    box(ax, 40, 96, 60, 7, "Open Books tab / search / sort / change page", size=7)
    d0 = diamond(ax, 40, 82, 48, 11, "Cached list in\nlocalStorage?")
    cache = box(ax, 116, 82, 50, 7, "Show cached rows at once", fc=BLUE, size=7)
    req = box(ax, 40, 66, 60, 7, "GET /api/books?query&page&size&sort", size=7)
    d1 = diamond(ax, 40, 52, 52, 11, "Spring cache has this\nquery+page+size+sort?")
    db = box(ax, 40, 37, 60, 7, "Query H2 with LIMIT/OFFSET and ORDER BY\nstore the page in the Spring cache", size=7)
    resp = box(ax, 40, 24, 60, 7, "Return { content, page, size,\ntotalElements, totalPages }", fc=GREEN, size=7)
    ui = box(ax, 40, 12, 60, 6, "UI replaces rows, pager; saves to localStorage", size=7)
    terminal(ax, 40, 3, "End", filled=False)
    arrow(ax, (40, 104.4), (40, 99.5))
    arrow(ax, (40, 92.5), (40, d0["t"]))
    arrow(ax, (d0["r"], 82), (cache["l"], 82), "Yes")
    arrow(ax, (40, d0["b"]), (40, req["t"]), "No", loff=(3, 0))
    route(ax, [(116, 78.5), (116, 66), (70, 66)])
    arrow(ax, (40, req["b"]), (40, d1["t"]))
    arrow(ax, (40, d1["b"]), (40, db["t"]), "No", loff=(3, 0))
    route(ax, [(d1["r"], 52), (118, 52), (118, 24), (resp["r"], 24)], "Yes", label_at=0)
    arrow(ax, (40, db["b"]), (40, resp["t"]))
    arrow(ax, (40, resp["b"]), (40, ui["t"]))
    arrow(ax, (40, ui["b"]), (40, 5))
    save(fig, "flow_list_books.png")


# ---------------------------------------------------------------- 7. security flow
def security_flow():
    fig, ax = canvas(190, 78)
    ax.text(95, 74, "Spring Security: what happens to every /api request", ha="center", fontsize=11, fontweight="bold")
    steps = [
        ("1. BasicAuthentication\nFilter\nreads Authorization:\nBasic base64(user:pass)", 22),
        ("2. DaoAuthentication\nProvider asks\nDatabaseUserDetails\nService for the user", 66),
        ("3. Compare password\nwith the stored\nBCrypt hash\n(PasswordEncoder)", 110),
        ("4. Authorization rules\nin SecurityConfig\n(URL + role)", 154),
    ]
    boxes = []
    for t, x in steps:
        boxes.append(box(ax, x, 50, 36, 16, t, fc=YELLOW if x != 154 else GREEN, size=6.8))
    for a, b in zip(boxes, boxes[1:]):
        arrow(ax, (a["r"], 50), (b["l"], 50))
    e1 = box(ax, 66, 22, 56, 10, "Missing / wrong credentials\nSecurityErrorHandler -> 401 JSON\n(no WWW-Authenticate header)", fc=RED, size=6.8)
    e2 = box(ax, 154, 22, 56, 10, "Role not allowed\nSecurityErrorHandler -> 403 JSON", fc=RED, size=6.8)
    ok = box(ax, 120, 8, 100, 7, "Allowed: request reaches the controller. No session or cookie is created (STATELESS).", fc=GREEN, size=7)
    arrow(ax, (88, 42), (66, 27.5), "fails")
    arrow(ax, (154, 42), (154, 27.5), "denied")
    arrow(ax, (154, 22 - 5), (150, 11.7), None) if False else None
    save(fig, "security_flow.png")


# ---------------------------------------------------------------- 8. redux flow
def redux_flow():
    fig, ax = canvas(190, 96)
    ax.text(95, 92, "Frontend data flow (Redux Toolkit + axios)", ha="center", fontsize=11, fontweight="bold")
    comp = box(ax, 24, 70, 40, 10, "Component\n(BooksPage.jsx)\nuseSelector / useDispatch", size=7)
    thunk = box(ax, 76, 70, 40, 10, "Thunk (booksActions.js)\ncreateApiThunk('books/fetch')", size=7)
    api = box(ax, 128, 70, 40, 10, "libraryApi.js\nhttp.get('/books', {params})", size=7)
    http = box(ax, 170, 70, 32, 10, "httpClient.js\naxios + interceptors", fc=YELLOW, size=7)
    back = box(ax, 170, 48, 32, 8, "Spring Boot\n/api/books", fc=GREEN, size=7)
    slice_ = box(ax, 76, 40, 40, 10, "Slice (booksSlice.js)\nextraReducers: fetch.fulfilled\n-> { items, pageInfo }", size=7)
    store = box(ax, 24, 40, 40, 10, "Store (app/store.js)\nauth books members nav notice", size=7)
    notice = box(ax, 76, 16, 40, 10, "noticeSlice\nisRejected -> red banner\nfulfilled -> green banner", fc=RED if False else YELLOW, size=7)
    cache = box(ax, 24, 16, 40, 10, "localCache.js\nsubscribe -> localStorage", fc=BLUE, size=7)
    arrow(ax, (comp["r"], 70), (thunk["l"], 70), "dispatch", size=6.5, loff=(0, 3))
    arrow(ax, (thunk["r"], 70), (api["l"], 70), "call", size=6.5, loff=(0, 3))
    arrow(ax, (api["r"], 70), (http["l"], 70), "")
    arrow(ax, (170, 65), (170, 52), "HTTP", size=6.5, loff=(5, 0))
    arrow(ax, (back["l"], 46), (thunk["r"] - 6, 65), "JSON page", size=6.5, loff=(8, -5))
    arrow(ax, (thunk["cx"], thunk["b"]), (slice_["cx"], slice_["t"]), "fulfilled action", size=6.5, loff=(10, 0))
    arrow(ax, (slice_["l"], 40), (store["r"], 40), "new state")
    arrow(ax, (store["cx"], store["t"]), (comp["cx"], comp["b"]), "re-render", size=6.5, loff=(7, 0))
    arrow(ax, (slice_["cx"], slice_["b"]), (notice["cx"], notice["t"]), "rejected", size=6.5, loff=(7, 0))
    arrow(ax, (store["cx"], store["b"]), (cache["cx"], cache["t"]), "every change", size=6.5, loff=(8, 0))
    ax.text(150, 22, "Request middleware adds the Basic header.\nResponse middleware signs the user out on a 401.", fontsize=7, style="italic", ha="left")
    save(fig, "redux_flow.png")


# ---------------------------------------------------------------- 9. maven lifecycle
def maven_lifecycle():
    fig, ax = canvas(190, 62)
    ax.text(95, 58, "Maven build lifecycle (default phases used in this project)", ha="center", fontsize=11, fontweight="bold")
    phases = [("validate", "pom.xml is\ncorrect"), ("compile", "src/main/java\n-> target/classes"), ("test", "JUnit 5 runs\n(23 tests)"),
              ("package", "repackaged\nexecutable jar"), ("verify / install", "checks, copy to\n~/.m2 (optional)")]
    xs = [20, 58, 96, 134, 172]
    prev = None
    for (n, d), x in zip(phases, xs):
        b = box(ax, x, 36, 32, 14, f"{n}\n\n{d}", fc=YELLOW if n in ("compile", "test", "package") else WHITE, size=7)
        if prev:
            arrow(ax, (prev["r"], 36), (b["l"], 36))
        prev = b
    ax.text(95, 12, "`mvnw test` runs phases up to test.   `mvnw package` runs up to package.   `mvnw spring-boot:run` compiles and starts the app.\n"
            "Each phase runs all earlier phases first. The spring-boot-maven-plugin adds the 'repackage' step that makes the jar runnable.", ha="center", fontsize=7, style="italic")
    save(fig, "maven_lifecycle.png")


# ---------------------------------------------------------------- 10. RBAC matrix
def rbac_matrix():
    fig, ax = canvas(170, 82)
    ax.text(85, 78, "Role-based access control (what each login role may do)", ha="center", fontsize=11, fontweight="bold")
    rows = ["View / search books  GET /api/books", "Add a book  POST /api/books", "List members  GET /api/members",
            "Add a member  POST /api/members", "Issue / return  POST /api/borrow/*"]
    allow = {"ADMIN": [1, 1, 1, 1, 1], "LIBRARIAN": [1, 1, 1, 0, 1], "MEMBER": [1, 0, 0, 0, 0]}
    x0, y0, cw, rh = 8, 64, 24, 9
    ax.add_patch(Rectangle((x0, y0 - 5), 74, 7, fc=YELLOW, ec="black", lw=1.2))
    ax.text(x0 + 2, y0 - 1.5, "Action (endpoint)", fontsize=7.5, fontweight="bold", va="center")
    for j, role in enumerate(allow):
        ax.add_patch(Rectangle((x0 + 74 + j * cw, y0 - 5), cw, 7, fc=YELLOW, ec="black", lw=1.2))
        ax.text(x0 + 74 + j * cw + cw / 2, y0 - 1.5, role, fontsize=7.5, fontweight="bold", ha="center", va="center")
    for i, r in enumerate(rows):
        y = y0 - 5 - (i + 1) * rh
        ax.add_patch(Rectangle((x0, y), 74, rh, fc="white", ec="black", lw=1.0))
        ax.text(x0 + 2, y + rh / 2, r, fontsize=7.2, va="center")
        for j, role in enumerate(allow):
            ok = allow[role][i]
            ax.add_patch(Rectangle((x0 + 74 + j * cw, y), cw, rh, fc=GREEN if ok else RED, ec="black", lw=1.0))
            ax.text(x0 + 74 + j * cw + cw / 2, y + rh / 2, "allowed" if ok else "403", fontsize=7.2, ha="center", va="center")
    ax.text(85, 8, "Enforced twice: SecurityConfig on the server (the real protection) and permissions.js in the UI (hides what you cannot use).", ha="center", fontsize=7, style="italic")
    save(fig, "rbac_matrix.png")


def main():
    for fn in (architecture, class_domain, class_layers, class_exceptions, sequence_issue, flow_signin,
               flow_issue, flow_return, flow_list_books, security_flow, redux_flow, maven_lifecycle, rbac_matrix):
        fn()


if __name__ == "__main__":
    main()
