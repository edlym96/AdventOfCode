#include <cstdlib>
#include <fstream>
#include <iostream>
#include <ostream>
#include <string>

int solve_2(std::string &file) {
  std::ifstream in{file};
  int location = 50;
  int count = 0;

  std::string line{};
  while (std::getline(in, line)) {
    // input is expected to look like 'R10' or 'L5' indication direction and
    // number of steps
    int direction = line[0] == 'R' ? 1 : -1;
    int val = std::stoi(line.substr(1));
    int local_count = 0;
    local_count += val / 100;
    val %= 100;
    int new_location = (location + (val * direction));
    if (location != 0 and (new_location <= 0 or new_location > 99)) {
      local_count += 1;
    }
    new_location = new_location % 100;
    new_location += new_location < 0 ? 100 : 0;
    location = new_location;
    count += local_count;
    std::cout << "after " << line << " "
              << "location pre modulo: " << new_location << " "
              << "location: " << location << std::endl;
    std::cout << "incrementing by " << local_count << std::endl;
  }
  std::cout << count << std::endl;
  return count;
}

int main() {
  std::string file_name =
      "/Users/edlym96/Documents/Projects/adventofcode/2025/day1/input1.txt";
  solve_2(file_name);
  return 0;
}
