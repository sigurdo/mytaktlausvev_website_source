


# Arguments:
# - fromPage - int
# - toPage - int
# Returns:
# - inputFormat - string on the format "fromPage-toPage" or "fromPage" if they are equal
def convertPagesToInputFormat(fromPage: int, toPage: int):
    if fromPage == toPage:
        return str(fromPage)
    else:
        return f"{fromPage}-{toPage}"

# Arguments:
# - inputFormat - string on the format "fromPage-toPage" or "fromPage" if they are equal
# Returns:
# - fromPage - int
# - toPage - int
def convertInputFormatToPages(inputFormat: str):
    pages = inputFormat.split("-")
    for i, page in enumerate(pages):
        pages[i] = int(page.strip(" "))
    if len(pages) == 1:
        return pages[0], pages[0]
    return pages[0], pages[1]

