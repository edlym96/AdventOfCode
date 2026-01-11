#!/usr/bin/env python3
import argparse
import math
import enum
from pathlib import Path
from collections import namedtuple, deque
from heapq import heappop, heappush

FILEPATH = str(Path(__file__).parent / 'input.txt')

class SignalType(enum.Enum):
    LOW = 0
    HIGH = 1

class State(enum.Enum):
    OFF = 0
    ON = 1

class Module:
    def __init__(self, label, destinations):
        self.label = label
        self.destinations = destinations

    def process_signal(self, source, signal_type: SignalType):
        raise NotImplemented
    
    def reset_state(self):
        raise NotImplemented

class Broadcaster(Module):
    
    def process_signal(self, source, signal_type: SignalType):
        return [(self.label, destination, signal_type) for destination in self.destinations]

    def reset_state(self):
        pass
    
class FlipFlop(Module):

    def __init__(self, label, destinations):
        super().__init__(label, destinations)
        self.state = State.OFF
    
    def process_signal(self, source, signal_type: SignalType):
        if signal_type == SignalType.HIGH:
            return []
        self.state = State.ON if self.state == State.OFF else State.OFF
        return [(self.label, destination, SignalType.HIGH if self.state == State.ON else SignalType.LOW) for destination in self.destinations]
    
    def reset_state(self):
        self.state = State.OFF

class Conjunction(Module):

    def __init__(self, label, destinations):
        super().__init__(label, destinations)
        self.memory = {}
    
    def process_signal(self, source, signal_type: SignalType):
        self.memory[source] = signal_type
        if all(mem == SignalType.HIGH for mem in self.memory.values()):
            output = SignalType.LOW
        else:
            output = SignalType.HIGH
        return [(self.label, destination, output) for destination in self.destinations]

    def update_sources(self, sources):
        self.memory = {s:SignalType.LOW for s in sources}

    def reset_state(self):
        self.memory = {s: SignalType.LOW for s in self.memory.keys()}

def load_txt(filepath) -> list[list[str]]:
    modules = {}
    conjunction_modules = {}
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            src, destinations = line.strip().rstrip().split(' -> ')
            destinations = destinations.split(', ')
            src_type = src[0]
            src_module = src[1:]
            if src == 'broadcaster':
                modules[src] = Broadcaster(src, destinations)
            elif src_type == '%':
                modules[src_module] = FlipFlop(src_module, destinations)
            elif src_type == '&':
                modules[src_module] = Conjunction(src_module, destinations)
                conjunction_modules[src_module] = []
    
    for source, module in modules.items():
        for destination in module.destinations:
            if destination in conjunction_modules:
                conjunction_modules[destination].append(source)

    for label, sources in conjunction_modules.items():
        modules[label].update_sources(sources)
    return modules

def one_button_press(modules):
    low_count = 0
    high_count = 0
    queue = deque([('button', 'broadcaster', SignalType.LOW)])
    while len(queue):
        src, dst, signal_type = queue.popleft()
        if signal_type == SignalType.LOW:
            low_count += 1
        else:
            high_count += 1
        if dst not in modules:
            continue
        next_signals = modules[dst].process_signal(src, signal_type)
        for sig in next_signals:
            queue.append(sig)
    return low_count, high_count

def button_press_part2(modules) -> bool:
    low_counts = {}
    # 'rx' has only one input, 'zp'
    sources = set(modules['zp'].memory.keys())
    cycles = 0
    while len(low_counts) < len(sources):
        cycles += 1
        queue = deque([('button', 'broadcaster', SignalType.LOW)])
        rx_low_pulses = 0
        while len(queue):
            src, dst, signal_type = queue.popleft()
            # The first low signal sent to any of the conjunction sources means there's a cycle - send a high to 'zp' if all inputs to 'zp' are high, then signal ot 'rx' is low
            if dst in sources:
                if signal_type == SignalType.LOW:
                    if dst not in low_counts:
                        print(dst, cycles)
                        low_counts[dst] = cycles
            if dst == 'rx' and signal_type == SignalType.LOW:
                rx_low_pulses += 1
            if dst not in modules:
                continue
            next_signals = modules[dst].process_signal(src, signal_type)
            for sig in next_signals:
                queue.append(sig)
    
    return math.lcm(*low_counts.values())

def solve_part1(modules) -> int:
    low_count = 0
    high_count = 0
    for _ in range(1000):
        new_low, new_high = one_button_press(modules)
        low_count += new_low
        high_count += new_high

    return low_count * high_count

def solve_part2(modules) -> int:
    return button_press_part2(modules)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    modules = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(modules)}")
    # part 2
    modules = load_txt(pargs.filepath)
    print(f"Result for part 2: {solve_part2(modules)}")
