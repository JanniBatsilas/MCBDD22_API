
from chembl_webresource_client.new_client import new_client
import requests, sys
import pandas as pd
import pprint
import collections
from statistics import median
import json


def main():

    testmode = 0

    if testmode != 1:
        # TASK 1: Get all the drugs and their YFA
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

        print("Number of Drugs: ", len(molecule_chembl_id_list))

        drug_year_df = pd.DataFrame.from_records(drug_dict)
        drug_year_df = drug_year_df.T
        drug_year_df.reset_index(inplace=True)
        drug_year_df.rename(columns={"index": "pref_name", 0: "first_approval", 1: "molecule_chembl_id"}, inplace=True)
        print(drug_year_df)

        # TASK 1: Get all activities for all the drugs found in step 1
        activ = new_client.activity
        res_a = activ.filter(molecule_chembl_id__in=molecule_chembl_id_list).only(["molecule_chembl_id", "target_chembl_id"])
        target_chembl_id_list = []
        activity_dict = {}
        for counter, i in enumerate(res_a):
            target_chembl_id_list.append(i["target_chembl_id"])
            activity_dict[counter] = [i["molecule_chembl_id"], i["target_chembl_id"]]

        target_chembl_id_list = list(set(target_chembl_id_list))
        drug_action_df = pd.DataFrame(activity_dict)
        drug_action_df = drug_action_df.T
        drug_action_df.rename(columns={0: "molecule_chembl_id", 1: "target_chembl_id"}, inplace=True)
        frequency = collections.Counter(drug_action_df["molecule_chembl_id"].tolist())
        print("Median targets associated with each compound: ", median(list(frequency.values())))

        # TASK 3: Get most frequent keyword
        target = new_client.target
        res_t = target.filter(target_chembl_id__in=target_chembl_id_list).only(["target_chembl_id", "target_components"])
        drug_target_df = pd.DataFrame.from_records(res_t)
        pprint.pprint(drug_target_df)

    target_dict = {}
    url_base = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession="
    keywords_list = []

    if testmode !=1:

        counter = 0
        for i in res_t:
            try:
                acc = i["target_components"][0]["accession"]
                url = url_base + acc
                r = requests.get(url, headers= {"Accept" : "application/json"})
                lst = json.loads(r.text)
                keywords = lst[0]["keywords"]
                for dict in keywords:
                    keywords_list.append(dict["value"])
            except Exception:
                print(Exception.args)

        print("Most used keyword: " , max(set(keywords_list), key=keywords_list.count))

    else:

        acc = "O76074"
        url = url_base + acc
        r = requests.get(url, headers={"Accept": "application/json"})
        lst = json.loads(r.text)
        keywords = lst[0]["keywords"]
        for dict in keywords:
            keywords_list.append(dict["value"])
        print(keywords_list)



if __name__ == "__main__":

    main()
