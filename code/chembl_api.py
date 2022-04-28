import time
from chembl_webresource_client.new_client import new_client

def main():
    reduced_dict = {}
    molecule = new_client.molecule
    approved_drugs = molecule.filter(max_phase=4, first_approval__gte=2012).order_by('first_approval')
    molecule_chembl_id_list = []

    for count, i in enumerate(approved_drugs):

        molecule_chembl_id_list.append(i["molecule_chembl_id"])

        if i["first_approval"] != None:
            reduced_dict[i["pref_name"]] = [i["first_approval"], i["molecule_chembl_id"]]
        else:
            reduced_dict[i["pref_name"]] = [0, "molecule_chembl_id"]

    activ = new_client.activity
    res_a = activ.filter(molecule_chembl_id__in=molecule_chembl_id_list).only(["molecule_chembl_id", "target_chembl_id"])
    target_chembl_id_list = []

    for counter, i in enumerate(res_a):
        target_chembl_id_list.append(i["target_chembl_id"])

    target_chembl_id_list = list(set(target_chembl_id_list))
    print(target_chembl_id_list)
    print(len(target_chembl_id_list))

    target = new_client.target
    res_t = target.filter(target_chembl_id__in=target_chembl_id_list).only()




if __name__ == "__main__":
    main()
