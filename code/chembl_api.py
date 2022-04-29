import time
from chembl_webresource_client.new_client import new_client
import uniprot
import requests, sys
import pandas as pd
import pprint


def main():
    drug_dict = {}
    molecule = new_client.molecule
    approved_drugs = molecule.filter(max_phase=4, first_approval__gte=2012).order_by('first_approval')
    molecule_chembl_id_list = []

    for count, i in enumerate(approved_drugs):

        molecule_chembl_id_list.append(i["molecule_chembl_id"])
        if i["first_approval"] != None:
            drug_dict[i["pref_name"]] = [i["first_approval"], i["molecule_chembl_id"]]
        else:
            drug_dict[i["pref_name"]] = [0, "molecule_chembl_id"]

    drug_year_df = pd.DataFrame.from_records(drug_dict)
    drug_year_df = drug_year_df.T
    drug_year_df.reset_index(inplace=True)
    drug_year_df.rename(columns={"index": "pref_name", 0: "first_approval", 1: "molecule_chembl_id"}, inplace=True)
    print(drug_year_df)

    activ = new_client.activity
    res_a = activ.filter(molecule_chembl_id__in=molecule_chembl_id_list).only(
        ["molecule_chembl_id", "target_chembl_id"])
    target_chembl_id_list = []
    activity_dict = {}
    for counter, i in enumerate(res_a):
        target_chembl_id_list.append(i["target_chembl_id"])
        activity_dict[i["molecule_chembl_id"]] = [i["target_chembl_id"]]
    target_chembl_id_list = list(set(target_chembl_id_list))

    drug_action_df = pd.DataFrame(activity_dict)
    drug_action_df = drug_action_df.T
    drug_action_df.reset_index(inplace=True)
    drug_action_df.rename(columns={"index": "molecule_chembl_id", 0: "target_chembl_id"}, inplace=True)
    print(drug_action_df)

    target = new_client.target
    res_t = target.filter(target_chembl_id__in=target_chembl_id_list).only(["target_chembl_id", "target_components"])

    drug_target_df = pd.DataFrame.from_records(res_t)
    pprint.pprint(drug_target_df)



    target_dict = {}
    url_base = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession="
    for i in res_t:
        acc = i["target_components"][0]["accession"]
        url = url_base + acc
        r = requests.get(url, headers= {"Accept" : "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        print(r.text)
        target_dict[i["target_chembl_id"]] = r.text


if __name__ == "__main__":

    main()
