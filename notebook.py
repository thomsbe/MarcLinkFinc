import marimo

__generated_with = "0.10.19"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pymarc import MARCReader

    titles = []

    with open("samples/output.mrc", "rb") as marc_file:
        reader = MARCReader(marc_file)

        for record in reader:
            title = record.title
            mo.output.append(f'Titel: {title}')
    return MARCReader, marc_file, mo, reader, record, title, titles


if __name__ == "__main__":
    app.run()
