import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""# PyMarc > Finc - Demo Notebook""")
    return


@app.cell
def _():
    import marimo as mo
    import pymarc
    return mo, pymarc


@app.cell
def _(pymarc):
    # Erstelle ein neues Record-Objekt
    record = pymarc.Record()

    # Füge Felder hinzu
    # Leader
    record.leader = '00000nam a22000000a 4500'

    # Kontrollfelder
    record.add_field(
        pymarc.Field('008', data='200427s2020    gw a    b    001 0 ger')
    )

    # Datenfelder
    # Titel Information
    record.add_field(
        pymarc.Field(
            tag='245',
            indicators=['1', '0'],
            subfields=[
                pymarc.Subfield(code='a', value='Ein Beispielbuch :'),
                pymarc.Subfield(code='b', value='mit Untertitel /'),
                pymarc.Subfield(code='c', value='von Max Mustermann')
            ]
        )
    )

    # Autor
    record.add_field(
        pymarc.Field(
            tag='100',
            indicators=['1', ' '],
            subfields=[
                pymarc.Subfield(code='a', value='Mustermann, Max'),
                pymarc.Subfield(code='d', value='1980-')
            ]
        )
    )

    # ISBN
    record.add_field(
        pymarc.Field(
            tag='020',
            indicators=[' ', ' '],
            subfields=[
                pymarc.Subfield(code='a', value='9783123456789')
            ]
        )
    )
    return (record,)


@app.cell
def _(mo, record):
    # Zeige das Record-Objekt in formatierter Form an
    mo.md("## Marc21 Record")
    mo.md("```")
    mo.md(str(record))
    mo.md("```")
        
    # Zeige die Felder strukturiert an
    mo.md("## Feldübersicht")
       
    # Leader
    mo.md(f"### Leader\n```\n{record.leader}\n```")
        
    # Kontrollfelder
    mo.md("### Kontrollfelder")
    for field in record.get_fields():
        if field.is_control_field():
            mo.md(f"- {field.tag}: `{field.data}`")
        
    # Datenfelder
    mo.md("### Datenfelder")
    for field in record.get_fields():
        if not field.is_control_field():
            indicators = f"[{field.indicators[0]},{field.indicators[1]}]"
            mo.md(f"#### {field.tag} {indicators}")
            for subfield in field:
                mo.md(f"- ${subfield.code}: {subfield.value}")

    return field, indicators, subfield


if __name__ == "__main__":
    app.run()
