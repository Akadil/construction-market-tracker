from . import characteristics_utils as utils

def check_characteristics(tender: dict):
    utils.set_to_null(tender)

    for lot in tender["lots"]:
        # Get the characteristics of the lot
        traits = utils.get_characteristics(lot)
        if (traits.get("ok") == False):
            continue
        else:
            traits = traits["characteristics"]

        lot["level"] = traits["level"]
        lot["tech_diff"] = traits["tech_diff"]
        lot["type"] = traits["type"]
        lot["goal"] = traits["goal"]