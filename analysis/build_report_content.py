#!/usr/bin/env python3
"""Generate retained LaTeX and Markdown Analysis sources from the reviewed JSON."""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path
from report_concise import concise_cases, NFR

ROOT = Path(__file__).resolve().parent.parent
GROUPS = ["User/shared", "Buyer", "Seller", "Admin", "Payment Integration"]
ACTORS = [
    ["Guest", "Registers an ordinary human account and enrols MFA; cannot provision Admin or Merchant privileges."],
    ["Buyer", "Creates/cancels their eligible escrow, accepts its terms when funding, confirms delivery acceptance, and exercises participant tracking/refund/dispute rights."],
    ["Seller", "Accepts/rejects their proposed agreement, records full goods delivery or service completion, and exercises participant tracking/refund/dispute rights."],
    ["Admin", "Uses a pre-provisioned MFA account to resolve disputes, configure future-only evidence policy, view analytics/audit and reconcile or safely retry approved payouts; cannot declare payment success."],
    ["Merchant/Marketplace", "Uses a pre-provisioned OAuth client bound to one Seller; creates and queries only its own escrows and has no participant/Admin transaction authority."],
    ["Partner Bank", "External mock funding method, all Seller releases, and refunds for original Bank funding; provides authenticated, correlated results."],
    ["Payment Gateway", "External mock funding method and refunds for original Gateway funding; does not execute Seller releases in the MVP."],
]
INTERFACES = [
    ["B1.API: Merchant creation", "OAuth client; scoped operation reference; distinct existing Buyer/Seller; GOODS/SERVICES; positive whole-VND amount; deliverable and acceptance criteria.", "Verify the client's Seller binding and shared B1 rules. Return escrow/client references, policy version and AWAITING_SELLER. Identical repeats return the original; conflicting reference reuse is rejected."],
    ["U4.API: Merchant tracking", "OAuth client and an owned escrow/client reference.", "Return an authorised lifecycle/attempt snapshot with reconciliation uncertainty. Polling is read-only; exclude private evidence, other clients' records and Admin-only audit."],
    ["P1: Funding confirmation", "Authenticated Bank/Gateway result; provider, escrow, operation and attempt references; exact amount, VND and outcome.", "Matched full receipt establishes HELD once. Confirmed no-receipt failure permits Buyer retry/cancellation. Pending, unknown and invalid results never establish held funds."],
    ["P2/P3/A5: Payout and reconciliation", "Saved immutable decision/reservation; provider, escrow, operation and attempt references; full VND amount; locked destination/source; authenticated callback/query result.", "Bank releases to Seller; original provider refunds original source. Only verified success is terminal. Unknown is query-only; confirmed no-money failure permits a linked retry in the same direction."],
]

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def ascii_text(value):
    s = str(value)
    for a, b in {"—":" - ", "–":"-", "‘":"'", "’":"'", "“":'"', "”":'"',
                 "…":"...", "≤":"<=", "≥":">=", "→":" -> ", "×":" x ", "\u00a0":" "}.items():
        s = s.replace(a, b)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

def tx(value):
    special = {"\\":r"\textbackslash{}", "{":r"\{", "}":r"\}", "$":r"\$",
               "&":r"\&", "#":r"\#", "%":r"\%", "_":r"\_\allowbreak{}", "~":r"\textasciitilde{}",
               "^":r"\textasciicircum{}", "<":r"\textless{}", ">":r"\textgreater{}"}
    return "".join(special.get(c, c) for c in ascii_text(value))

def cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ")

def lab(kind, code):
    return "fig:" + kind + "-" + re.sub("[^a-z0-9]+", "-", code.lower()).strip("-")

def ref(kind, code):
    return r"Figure~\ref{" + lab(kind, code) + "}"

def mt(headers, rows):
    return "\n".join(["| " + " | ".join(map(cell, headers)) + " |",
                       "| " + " | ".join("---" for _ in headers) + " |"] +
                      ["| " + " | ".join(map(cell, row)) + " |" for row in rows]) + "\n\n"

def lt(headers, rows, widths):
    cols = "".join(r">{\raggedright\arraybackslash}p{" + f"{w:.2f}" + r"\linewidth}" for w in widths)
    head = " & ".join(r"\textbf{" + tx(h) + "}" for h in headers) + r" \\"
    body = "\n\\addlinespace[4pt]\n".join(" & ".join(tx(x) for x in row) + r" \\" for row in rows)
    return ("{\\fontsize{10.5}{13}\\selectfont\\setlength{\\tabcolsep}{4pt}\n"
            "\\begin{longtable}{" + cols + "}\n\\toprule\n\\rowcolor{epsblue!10}" + head +
            "\n\\midrule\n\\endfirsthead\n\\toprule\n\\rowcolor{epsblue!10}" + head +
            "\n\\midrule\n\\endhead\n\\midrule\\multicolumn{" + str(len(headers)) +
            r"}{r}{\small Continued on next page}\\" +
            "\n\\endfoot\n\\bottomrule\n\\endlastfoot\n" + body + "\n\\end{longtable}\n}\n")

def items(values):
    return "\\begin{itemize}\n" + "\n".join(r"\item " + tx(v) for v in values) + "\n\\end{itemize}\n"

class Builder:
    def __init__(self, root, project):
        self.root, self.project, self.a = root, project, root / "analysis"
        self.ucs = concise_cases(read(self.a / "content_user_buyer.json")["use_cases"] + read(self.a / "content_seller_admin_payment.json"))
        self.c = read(self.a / "analysis_controls.json")
        self.ov = [d for d in read(self.a / "overview_manifest.json")["diagrams"] if d['id'] != 'UC_Overview']
        self.ad = {d["use_case"]: d for d in read(self.a / "activity_models.json")["diagrams"]}
        self.seq = read(self.a / "sequence_models.json")
        self.sd = {d["id"]: d for d in self.seq["diagrams"]}
        self.logical = {d["logical_id"]: d for d in self.seq["logical_diagrams"]}
        self.tex, self.md, self.figures, self.labels = [], [], [], []

    def heading(self, n, title):
        self.tex.append("\\" + {1:"chapter",2:"section",3:"subsection",4:"subsubsection"}[n] + "{" + tx(title) + "}\n")
        self.md.append("#" * n + " " + title + "\n\n")

    def p(self, value):
        self.tex.append(tx(value) + "\n\n")
        self.md.append(value + "\n\n")

    def table(self, headers, rows, widths):
        self.tex.append(lt(headers, rows, widths))
        self.md.append(mt(headers, rows))

    def field(self, title, value):
        self.tex.append(r"\paragraph{" + tx(title) + ".} " + tx(value) + "\n")
        self.md.append("**" + title + ":** " + value + "\n\n")

    def list_field(self, title, values):
        self.tex.append(r"\paragraph{" + tx(title) + r".}\mbox{}" + "\n" + items(values))
        self.md.append("**" + title + ":**\n\n" + "\n".join("- " + x for x in values) + "\n\n")

    def figure(self, kind, code, filename, caption, notes="", inline_first=False):
        pdf = Path(filename).with_suffix(".pdf").as_posix()
        png = (Path("analysis") / Path(filename).with_suffix(".png")).as_posix()
        self.figures.append(pdf)
        self.labels.append(lab(kind, code))
        if kind == "sequence" and code == "B3":
            self.tex.append(r"\clearpage\newgeometry{margin=15mm,headheight=15pt,headsep=8pt,footskip=16pt}\begin{figure}[p]\centering\includegraphics[width=510bp,height=700bp,keepaspectratio,clip]{" + pdf + r"}\caption{" + tx(caption) + r"}\label{" + lab(kind, code) + r"}\end{figure}\clearpage\restoregeometry" + "\n")
        else:
            command = r"\epsfirstfigure{" if inline_first else r"\epsfigure{"
            self.tex.append(command + pdf + "}{" + tx(caption) + "}{" + lab(kind, code) + "}\n")
        self.md.append("![" + caption + "](" + png + ")\n\n")
        if notes:
            self.md.append(notes + "\n\n")

    def overview(self):
        self.heading(1, "Analysis")
        self.heading(2, "General Use cases Diagram")
        self.p("EPS is an academic escrow simulation for goods and services. Each agreement has one Buyer, one distinct Seller and one full VND amount, funded through a Bank or Payment Gateway mock. The overview is divided into focused views for readability.")
        for position,d in enumerate(self.ov):
            self.figure("overview",d["id"],d["file"],d["title"].split(" - ",1)[-1],inline_first=position==0)
        actors=[
            ("Guest","registers an ordinary account and logs in with MFA."),
            ("Buyer","creates and funds an escrow, accepts delivery and requests release."),
            ("Seller","accepts the agreement and records delivery or service completion. Both participants may request a refund or open a dispute."),
            ("Admin","resolves disputes, updates policy, views analytics/audit and reconciles pending transfers."),
            ("Merchant/Marketplace","creates and queries only its own escrows through a separately authenticated client."),
            ("Partner Bank","simulates funding, Seller release and refunds for Bank-funded escrows."),
            ("Payment Gateway","simulates funding and refunds to the original Gateway source.")]
        self.tex.append("\\begin{itemize}\n")
        for name,description in actors:
            self.tex.append(r"\item \textbf{"+tx(name)+"}: "+tx(description)+"\n")
            self.md.append("- **"+name+":** "+description+"\n")
        self.tex.append("\\end{itemize}\n")
        self.md.append("\n")
        self.p("Buyer and Seller are roles in each transaction. Release uses the Bank mock; refund returns through the original funding provider. Real money, partial payments, milestones and automatic release are outside this MVP.")

    def details(self):
        self.heading(2,"Use case Details")
        for group in GROUPS:
            name="User" if group=="User/shared" else group
            self.tex.append(r"\par\begingroup\ifdim\dimexpr\pagegoal-\pagetotal\relax<180pt\relax\newpage\fi\endgroup"+"\n")
            self.heading(3,name + "'s Use cases Details")
            for u in [u for u in self.ucs if u["group"]==group]:
                title=u["id"]+": "+u["name"]
                self.tex.append(r"\par\begingroup\ifdim\dimexpr\pagegoal-\pagetotal\relax<120pt\relax\newpage\fi\endgroup\medskip\noindent\textbf{"+tx(title)+"}\n")
                self.md.append("**"+title+"**\n\n")
                cols=r"|>{\raggedright\arraybackslash}p{0.22\linewidth}|>{\raggedright\arraybackslash}p{0.07\linewidth}|>{\raggedright\arraybackslash}p{0.17\linewidth}|>{\raggedright\arraybackslash}p{0.44\linewidth}|"
                span=r"p{\dimexpr0.68\linewidth+4\tabcolsep+2\arrayrulewidth\relax}|"
                parts=[r"{\fontsize{10.5}{13}\selectfont\setlength{\tabcolsep}{4pt}",
                       r"\begin{longtable}{"+cols+"}",r"\hline\endfirsthead",
                       r"\multicolumn{4}{|l|}{\textit{"+tx(u['id'])+r" (continued)}}\\\hline\endhead",
                       r"\endfoot\endlastfoot",
                       r"\textbf{Use Case Code} & "+tx(u["id"])+r" & \textbf{Use Case Name} & "+tx(u["name"])+r" \\\hline"]
                self.md.append(mt(["Field","Description"],[["Use Case Code",u["id"]],["Use Case Name",u["name"]]]))
                for label,value in [("Actor","; ".join(u["actors"])),("Usage",u["usage"]),("Activation Event",u["activation"]),("Preconditions"," ".join(u["preconditions"]))]:
                    parts.append(r"\textbf{"+label+r"} & \multicolumn{3}{"+span+"}{"+tx(value)+r"} \\\hline")
                    self.md.append("**"+label+":** "+value+"\n\n")
                parts.append(r"\textbf{Main Event Flow} & \textbf{Index} & \textbf{Done by} & \textbf{Action} \\\hline")
                flow=[dict(f) for f in u["flow"]]
                for variant in u.get("api_variants",[]):
                    flow.append({"index":"API","by":variant["actor"],"action":variant["id"]+": "+variant["summary"]})
                for f in flow:
                    parts.append(" & "+tx(f["index"])+" & "+tx(f["by"])+" & "+tx(f["action"])+r" \\\hline")
                self.md.append("**Main Event Flow**\n\n"+mt(["Index","Done by","Action"],[[f["index"],f["by"],f["action"]] for f in flow]))
                post=" ".join(u["postconditions"])
                parts.append(r"\textbf{Postconditions} & \multicolumn{3}{"+span+"}{"+tx(post)+r"} \\\hline")
                parts.append(r"\end{longtable}}")
                self.tex.append("\n".join(parts)+"\n")
                self.md.append("**Postconditions:** "+post+"\n\n")

    def activities(self):
        self.heading(2,"Activity Diagram")
        for group in GROUPS:
            name="User" if group=="User/shared" else group
            self.heading(3,name + "'s Use cases")
            for position,u in enumerate(u for u in self.ucs if u["group"]==group):
                d=self.ad[u["id"]]
                self.figure("activity",u["id"],d["filename"],u["id"]+": "+u["name"],inline_first=position==0)

    def sequences(self):
        self.heading(2,"Sequence Diagram")
        self.p("Sequence diagrams show actor, boundary, control and entity interactions. Large flows continue in the referenced modules; B1.API and U4.API use the same business rules as their user-interface variants.")
        rendered=[]
        for group in GROUPS:
            name="User" if group=="User/shared" else group
            self.heading(3,name + "'s Use cases")
            first_view=True
            for u in (u for u in self.ucs if u["group"]==group):
                for code in [u["id"]]+[v["id"] for v in u.get("api_variants",[])]:
                    for sid in [code]+[part["id"] for part in self.logical[code].get("parts",[])]:
                        d=self.sd[sid]
                        caption=code+": "+u["name"]
                        if sid!=code:
                            caption+=" (continued: "+sid+")"
                        self.figure("sequence",sid,d["filename"],caption,inline_first=first_view)
                        first_view=False
                        rendered.append(sid)
        assert len(rendered)==len(set(rendered))==len(self.sd)

    def nfr(self):
        self.heading(2,"Non-functional Requirements")
        self.p("The system must also meet the following non-functional requirements.")
        for name,values in NFR.items():
            self.tex.append(r"\medskip\noindent\textbf{"+tx(name)+":}\n"+items(values))
            self.md.append("**"+name+":**\n\n"+"\n".join("- "+value for value in values)+"\n\n")

    def traceability(self):
        out=["# EPS - Traceability and Acceptance\n\n",
             "This support document defines coverage and future acceptance scenarios. It is not an executed test report. It remains outside Chapter 3, preserving Sections 3.1-3.5.\n\n",
             "## Functional coverage\n\n"]
        rows=[]
        for r in self.c["requirements"]:
            rules=[b["id"] for b in self.c["rules"] if r["id"] in b["requirements"]]
            ad=list(dict.fromkeys(u.replace(".API","") for u in r["useCases"]))
            rows.append([r["id"],r["title"],", ".join(r["useCases"]),", ".join("AD-"+u for u in ad),", ".join("SD-"+u for u in r["useCases"]),", ".join(rules)])
        out.append(mt(["Requirement","Capability","Use cases","Activities","Logical sequences","Business rules"],rows))
        out.append("B1.API/U4.API share B1/U4 activity contracts and have dedicated Merchant sequence views. Continuations belong to the same logical sequence and do not increase the use-case count.\n\n## Acceptance criteria by requirement\n\n")
        for r in self.c["requirements"]:
            out.append("### " + r["id"] + " - " + r["title"] + "\n\n")
            out.extend("- "+v+"\n" for v in r["acceptanceCriteria"])
            out.append("\n")
        out.append("## Diagram inventory\n\n")
        rows=[]
        for code,d in self.logical.items():
            parent=code.replace(".API","")
            rows.append([code,self.ad[parent]["filename"],d["default_main"],", ".join(p["id"] for p in d.get("parts",[])) or "None"])
        out.append(mt(["Code","Activity source","Main sequence source","Continuation IDs"],rows))
        out.append("## Basic acceptance matrix\n\nThe 16 paths cover GOODS/SERVICES x BANK/GATEWAY x BUYER_RELEASE/CONSENSUAL_REFUND/ADMIN_RELEASE/ADMIN_REFUND. Every path uses the full amount and synthetic data, and ends only on a verified mock provider success.\n\n")
        basic=[s for s in self.c["acceptanceScenarios"] if s["kind"]=="basic_matrix"]
        out.append(mt(["ID","Transaction type","Funding","Outcome","Final state"],[[s["id"],s["transactionType"],s["fundingMethod"],s["outcome"],"RELEASED" if s["outcome"].endswith("RELEASE") else "REFUNDED"] for s in basic]))
        for s in basic:
            out.append("### " + s["id"] + " - " + s["transactionType"] + " / " + s["fundingMethod"] + " / " + s["outcome"] + "\n\nPreconditions: " + s["preconditions"] + "\n\n")
            out.extend(str(i)+". "+v+"\n" for i,v in enumerate(s["steps"],1))
            out.append("\nExpected results:\n\n")
            out.extend("- "+v+"\n" for v in s["expected"])
            out.append("\nUse-case coverage: " + ", ".join(s["useCases"]) + ".\n\n")
        out.append("## Focused exception and concurrency scenarios\n\n")
        for s in [s for s in self.c["acceptanceScenarios"] if s["kind"]!="basic_matrix"]:
            out.append("### "+s["id"]+" - "+s["title"]+"\n\nSetup/action: "+s["setupAndAction"]+"\n\nExpected: "+s["expected"]+"\n\nRules: "+", ".join(s["rules"])+".\n\n")
        out.append("## Non-functional acceptance\n\n")
        for g in self.c["nfr"]:
            out.append("### "+g["group"]+"\n\n"+mt(["ID","Requirement","Acceptance criterion","Verification"],[[r["id"],r["requirement"],r["acceptance"],r["verification"]] for r in g["requirements"]]))
        out.append("## Completion criteria\n\n"
                   "- FR01-FR12 have use-case, rule and diagram coverage; the same 22 codes and five groups are retained.\n"
                   "- Bank-only release and original-source refund hold for both funding methods.\n"
                   "- PENDING proposals freeze new delivery and ordinary release; a dispute invalidates the pending proposal.\n"
                   "- At most one dispute, one accepted payout direction and one final money outcome exist per escrow.\n"
                   "- Unknown is query-only; failed funding returns to Buyer control; failed payout keeps its reservation and permits only confirmed-failure same-direction retry.\n"
                   "- All 16 basic paths and 24 focused scenarios have explicit expected results and remain unexecuted until an implementation exists.\n"
                   "- Performance targets and legal statements are not presented as measured or certified findings.\n")
        return "".join(out)

    def alignment(self):
        out=["# Ghi chú đồng bộ Introduction / Planning với Analysis\n\n",
             "Ghi riêng các điểm cần nhóm rà soát khi hợp nhất report; không sửa PDF Introduction và Planning đã cung cấp. Analysis tuân theo MVP đã chốt. Đây không phải kết quả kiểm thử hay kết luận tuân thủ pháp lý.\n\n"]
        for n in self.c["planningAlignmentNotes"]:
            out.append("## "+n["id"]+" — "+n["topic"]+"\n\n"+n["note"]+"\n\n")
        out.append("## Mặc định nghiệp vụ đã khóa\n\n"
                   "- Tiền giả lập, VND nguyên, một buyer/một seller khác nhau; hàng hóa hoặc dịch vụ; payout toàn phần một lần.\n"
                   "- Seller chấp thuận trước funding; buyer xác nhận điều khoản khi nạp tiền. Merchant là OAuth client được cấp sẵn, gắn với seller, chỉ tạo/tra cứu giao dịch của client.\n"
                   "- Đề nghị PENDING chặn ghi nhận bàn giao mới và giải ngân thường. Từ chối/rút khôi phục thao tác hợp lệ mà không đảo ngược bàn giao đã lưu.\n"
                   "- Chỉ một dispute; mở dispute vô hiệu hóa đề nghị chờ. Admin ghi lý do và chốt một hướng payout, sau đó chờ provider xác nhận.\n"
                   "- Timeout/UNKNOWN chỉ đối soát cùng attempt. Funding thất bại có xác nhận không thu tiền trả về AWAITING_FUNDING để buyer retry/hủy. Payout thất bại giữ trạng thái pending và chỉ retry cùng hướng sau xác nhận không chuyển tiền.\n\n")
        out.append(f"## Sơ đồ và tệp nguồn\n\nCó {len(self.ov)} view use-case, {len(self.ad)} activity và {len(self.sd)} view sequence cho {len(self.logical)} luồng logic (22 use case chính và hai biến thể API). Continuation không làm tăng số use case.\n\n")
        out.append("- Giữ main.tex và sections/analysis.tex trong EPS_Report_LaTeX cùng toàn bộ nguồn .drawio và ảnh xuất.\n"
                   "- PDF được biên dịch và kiểm tra trình bày riêng. PNG phục vụ xem nhanh; PDF vector phục vụ LaTeX.\n"
                   "- EPS_Analysis.md là bản nội dung đồng hành. Traceability_and_Acceptance.md giữ truy vết/nghiệm thu bên ngoài chương 3, không tạo mục 3.6.\n")
        return "".join(out)

    def write(self):
        ids=[u["id"] for u in self.ucs]
        assert len(ids)==len(set(ids))==22
        assert len(self.ad)==22 and len(self.logical)==24
        for code in ids:
            assert code in self.ad and code in self.logical
        assert [g["group"] for g in self.c["nfr"]]==["Performance","Operational","Security","Cultural and Political"]
        self.overview(); self.details(); self.activities(); self.sequences(); self.nfr()
        t="% Generated by analysis/build_report_content.py; edit reviewed JSON and regenerate.\n"+"".join(self.tex)
        m="<!-- Companion to the retained LaTeX source. -->\n\n"+"".join(self.md)
        expected=len(self.ov)+len(self.ad)+len(self.sd)
        assert len(self.figures)==len(set(self.figures))==len(set(self.labels))==expected
        assert all(ord(c)<128 for c in t), "Unicode in TeX"
        for f in ["Use Case Code","Use Case Name","Actor","Usage","Activation Event","Preconditions","Main Event Flow","Postconditions"]:
            assert t.count("\\textbf{"+f+"}")==22, f
        assert not re.search(r"\\(?:subsection|subsubsection)\{", t.split("\\section{Use case Details}")[0])
        assert "\\subsection" not in t.split("\\section{Non-functional Requirements}")[1]
        assert all(r in self.labels for r in re.findall(r"\\ref\{([^}]+)\}",t))
        sections=re.findall(r"\\section\{([^}]+)\}",t)
        assert len(sections)==5
        dest=self.project/"sections"
        dest.mkdir(parents=True,exist_ok=True)
        (self.a/"Report_Structure_Validation.json").write_text(json.dumps({"report_figure_count":expected,"use_case_count":22,"fields_per_use_case":8,"sections":sections,"numbered_group_sections":["Use case Details","Activity Diagram","Sequence Diagram"],"source_chapters_unchanged":True,"report_style":"Sample outline with concise Analysis wording","figures":self.figures},indent=2),encoding="utf-8")
        start=t.index(r"\section{Sequence Diagram}")
        end=t.index(r"\section{Non-functional Requirements}",start)
        sequence=t[start:end]
        (dest/"sequence.tex").write_text(sequence,encoding="utf-8")
        t=t[:start]+r"\input{sections/sequence.tex}"+"\n"+t[end:]
        (dest/"analysis.tex").write_text(t,encoding="utf-8")
        (self.root/"EPS_Analysis.md").write_text(m,encoding="utf-8")
        (self.a/"Traceability_and_Acceptance.md").write_text(self.traceability(),encoding="utf-8")
        (self.a/"Planning_Alignment_Notes.md").write_text(self.alignment(),encoding="utf-8")
        print(json.dumps({"use_cases":22,"fields_per_use_case":8,"overview_views":len(self.ov),
                          "activities":len(self.ad),"logical_sequences":len(self.logical),
                          "sequence_views":len(self.sd),"figure_references":expected,"unique_labels":len(set(self.labels)),
                          "nfr_groups":4,"markdown_word_count":len(re.findall(r"\b[\w'-]+\b",re.sub(r"!\[[^]]*\]\([^)]*\)","",m))),
                          "latex_ascii_only":True,"sections":sections,
                          "missing_project_pdf_assets":[f for f in self.figures if not (self.project/f).exists()],
                          "status":"Sources generated and structurally checked; compilation and visual QA are separate."},indent=2))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=ROOT)
    parser.add_argument("--project",type=Path)
    args=parser.parse_args()
    root=args.root.resolve()
    Builder(root,args.project.resolve() if args.project else root/"EPS_Report_LaTeX").write()

if __name__=="__main__":
    main()

