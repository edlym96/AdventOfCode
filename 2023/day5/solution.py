import argparse
from collections import namedtuple
import bisect
from pathlib import Path

RangeRecord = namedtuple('RangeRecord', ('start', 'range'))
# Each mapping record is a named tuple which maps the source + range -> translation
MappingRecord = namedtuple('MappingRecord', ('source', 'range', 'translation'))

FILEPATH = str(Path(__file__).parent / 'input.txt')

class TranslationMapping():
    def __init__(self, mappings):
        self._mappings = {}
        for name, mapping in mappings.items():
            self._mappings[name] = sorted(mapping, key=lambda x: x.source)
    
    def map_seed(self, seed):
        val = seed
        for name, mapping in self._mappings.items():
            idx = bisect.bisect_right(mapping, val, key=lambda x: x.source)-1
            if idx < 0 or idx >= len(mapping):
                continue
            record = mapping[idx]
            high = record.source + record.range
            if record.source <= val < high:
                val += record.translation
        return val
    
    def map_seed_range(self, seed_rec:RangeRecord):
        # Two "queues"
        curr= [seed_rec]
        nxt = []
        for mapping in self._mappings.values():
            while len(curr):
                _rec = curr.pop(0)
                curr_start, curr_range = _rec.start, _rec.range
                start_idx = bisect.bisect_right(mapping, curr_start, key=lambda x: x.source)-1
                end_idx = bisect.bisect_right(mapping, curr_start + curr_range, key=lambda x: x.source)-1
                # Check the first overlap for cases where first idx xoes not overlap with given start
                if curr_start > (mapping[start_idx].source + mapping[start_idx].range):
                    start_idx += 1
                    nxt.append(RangeRecord(curr_start, curr_range - record.range))
                start_idx = max(0, start_idx)
                end_idx = min(len(mapping)-1, end_idx)
                for idx in range(start_idx, end_idx + 1):
                    # the first part of the overlap
                    record = mapping[idx]
                    if curr_start > record.source:
                        nxt.append(RangeRecord(curr_start + record.translation, min(record.source + record.range - curr_start, curr_range)))
                    else:
                        nxt.append(RangeRecord(record.source + record.translation, min(curr_start + curr_range - record.source, record.range)))
                    
                    # Second part of overlap
                    if curr_start + curr_range > record.source + record.range and idx < len(mapping)-1 and mapping[idx+1].source > record.source + record.range + 1:
                        if curr_start + curr_range >= mapping[idx+1].source:
                            outstanding_range = mapping[idx+1].source - (record.source + record.range) - 1
                        else:
                            outstanding_range = (curr_start + curr_range) - (record.source + record.range) - 1
                        nxt.append(RangeRecord(record.source + record.range + 1, outstanding_range))
            # Refresh queue states
            curr = nxt
            nxt = []
        return curr

def parse_seeds_part1(seed_line):
    return [int(s) for s in seed_line.split(' ')[1:]]

def parse_seeds_part2(seed_line):
    seeds = seed_line.split(' ')[1:]
    recs = []
    # seeeds must be even number
    for i in range(len(seeds) // 2):
        start = int(seeds[i*2])
        rng = int(seeds[i*2+1])
        recs.append(RangeRecord(start, rng))
    return recs

def load_txt(filepath):
    with open(filepath, mode='r') as file:
        
        # parse seeds
        seed_line = file.readline()
        seeds = parse_seeds_part1(seed_line)

        # parse maps
        file.readline()
        mappings = {}
        # There are known to be 7 maps, this can be changed to check file.eof for N maps
        for i in range(7):
            mappings.update(parse_mapping(file))

        # part 1
        return seeds, mappings

def load_txt_part2(filepath):
    with open(filepath, mode='r') as file:
        
        # parse seeds
        seed_line = file.readline()
        seed_recs = parse_seeds_part2(seed_line)

        # parse maps
        file.readline()
        mappings = {}
        # There are known to be 7 maps, this can be changed to check file EOF for N maps
        for i in range(7):
            mappings.update(parse_mapping(file))

        # part 2
        return seed_recs, mappings

def parse_mapping(fstream):
    rec_list = []
    line = fstream.readline()
    name = line.split(' ')[0]

    line = fstream.readline()
    while line.rstrip():
        dst, src, rng = line.split(' ')
        dst, src, rng = int(dst), int(src), int(rng)
        rec = MappingRecord(src, rng, dst-src)
        rec_list.append(rec)
        line = fstream.readline()
    
    return {name: rec_list}



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    seeds, mappings = load_txt(pargs.filepath)
    translation_mapping = TranslationMapping(mappings)
    locations = [translation_mapping.map_seed(seed) for seed in seeds]
    print(f"Min location for part 1: {min(locations)}")

    # part 2
    seeds, mappings = load_txt_part2(pargs.filepath)
    translation_mapping = TranslationMapping(mappings)
    locations = []
    for seed_rec in seeds:
        location_ranges = translation_mapping.map_seed_range(seed_rec)
        bound_locations = [r[0] for r in location_ranges]
        locations.extend(bound_locations)

    print(f"Min location for part 2: {min(locations)}")
