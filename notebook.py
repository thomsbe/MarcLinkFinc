import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pymarc

    mo.md(r"""# PyMarc > Finc - Demo Notebook""")

    record = pymarc.Record()
    record.leader = "00000cam a2200000 a 4500"
    record.add_field("001", "1234567890")
    record.add_field("005", "20231027120000.0")
    record.add_field("008", "231027s2023    gw a     b    000 0 ger  ")
    record.add_field("020", "  $a9783120012345")
    record.add_field("040", "  $aDE-101 $bger $cDE-101")
    record.add_field("041", "0 $ager")
    record.add_field("100", "1 $aMustermann, Max $d1970-$4aut")
    record.add_field("245", "10$aEin tolles Buch $bEin Roman $cMax Mustermann")
    record.add_field("250", "  $a2. Auflage")
    record.add_field("264", " 1$aStuttgart $bKlett $c2023")
    record.add_field("300", "  $a300 Seiten $bill.")
    record.add_field("336", "  $atext $btxt $2rdacontent")
    record.add_field("337", "  $aunvermittelt $bn $2rdamedia")
    record.add_field("338", "  $aband $bnc $2rdacarrier")
    record.add_field("520", "  $aEin spannender Roman über ...")
    record.add_field("650", " 0$aRoman $xBelletristik")
    record.add_field("700", "1 $aMusterfrau, Maria $eMitwirkende")
    record.add_field("856", "40$uhttp://www.example.com/ebook.pdf $zOnline-Ausgabe")


    def display_record(record: pymarc.Record) -> mo.Html:
        """Displays a pymarc record in a structured HTML table."""
        html = "<table>"
        html += "<tr><th>Feld</th><th>Inhalt</th></tr>"
        
        for field in record:
            subfields_str = " ".join([f"${sf.code}{sf.value}" for sf in field.subfield])
            html += f"<tr><td>{field.tag}</td><td>{subfields_str}</td></tr>"
        
        html += "</table>"
        return mo.Html(html)

    display_record(record)
    return display_record, mo, pymarc, record


if __name__ == "__main__":
    app.run()
