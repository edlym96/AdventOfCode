#include <fstream>
#include <iostream>
#include <ostream>
#include <string>

int solve_1(std::string &file) {
  std::ifstream in{file};
  int location = 50;
  int count = 0;

  std::string line{};
  while (std::getline(in, line)) {
    // input is expected to look like 'R10' or 'L5' indication direction and
    // number of steps
    int direction = line[0] == 'R' ? 1 : -1;
    int val = std::stoi(line.substr(1));
    int new_location = (location + (val * direction));
    // int to_add = new_location < 0 ? 1 : 0;
    location = new_location % 100;
    std::cout << location << std::endl;
    count += location == 0 ? 1 : 0;
    // location += to_add;
  }
  std::cout << count << std::endl;
  return count;
}

int main() {
  std::string file_name =
      "/Users/edlym96/Documents/Projects/adventofcode/2025/day1/input1.txt";
  solve_1(file_name);
  return 0;
}
