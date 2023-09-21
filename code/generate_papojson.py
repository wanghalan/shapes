from pqdm.processes import pqdm
import json
import itertools
import copy
import multiprocessing
import os


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


with open("../data/testing/va_combined.topojson", "r") as f:
    j = json.load(f)


def process_geos(geo):
    geoid = geo["properties"]["geoid"]
    # pbar.set_description("Generating papojson for {geoid}".format(geoid=geoid))
    flat_arcs = set([abs(v) for v in flatten(geo["arcs"])])
    j_clone = copy.deepcopy(j)
    j_clone["objects"]["va_combined"]["geometries"] = [
        geo
    ]  # just the one we are looking at

    bbox = [float("-inf"), float("inf"), float("-inf"), float("inf")]
    for i in range(len(j_clone["arcs"])):
        if not i in flat_arcs:
            j_clone["arcs"][i] = []  # empty unecessary arcs
        else:  # update bounding box
            if len(j_clone["arcs"][i]) <= 0:
                continue
            bbox[0] = min(j_clone["arcs"][i], key=lambda x: x[0])[0]
            bbox[1] = min(j_clone["arcs"][i], key=lambda x: x[1])[1]
            bbox[2] = max(j_clone["arcs"][i], key=lambda x: x[0])[0]
            bbox[3] = max(j_clone["arcs"][i], key=lambda x: x[1])[1]
    j_clone["bbox"] = bbox

    export_filepath = "../data/testing/{geoid}.papojson".format(geoid=geoid)
    with open(export_filepath, "w") as f:
        json.dump(j_clone, f)
    return os.path.isfile(export_filepath)


if __name__ == "__main__":
    geos = j["objects"]["va_combined"]["geometries"]
    print(len(geos))
    assert isinstance(geos, list)
    result = pqdm(geos, process_geos, n_jobs=multiprocessing.cpu_count())
    print(result)
