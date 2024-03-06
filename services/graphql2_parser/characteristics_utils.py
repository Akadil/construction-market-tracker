def set_to_null(tender):
    """
        Set the characteristics of the tender to None
    """
    tender["level"] = None
    tender["tech_diff"] = None
    tender["type"] = None
    tender["goal"] = None
    for lot in tender["lots"]:
        lot["level"] = None
        lot["tech_diff"] = None
        lot["type"] = None
        lot["goal"] = None


def get_characteristics(lot):
    """
        Get the characteristics of the lot
    """
    fileName, filePath = utils.get_file_link(lot["files"], "appendix_5")
    if (fileName == None):
        return {"ok": False, "error": "File not found"}

    response = parseFile(filePath, fileName)
    if (response["status_code"] != 200):
        return {"ok": False, "error": response["message"]}
    
    return {"ok": True, "char": response["characteristics"]}