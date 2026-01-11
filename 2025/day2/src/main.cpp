#include <cmath>
#include <fstream>
#include <iostream>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

int solve_1(std::string &filename) {
  std::ifstream in{filename};
  std::string line{};
  unsigned long long sum = 0;
  while (std::getline(in, line, ',')) {
    int idx = line.find('-');
    std::string lower = line.substr(0, idx);
    std::string upper = line.substr(idx + 1, line.length());
    unsigned long long lower_i = std::stoull(lower);
    unsigned long long upper_i = std::stoull(upper);
    std::cout << lower << "-" << upper << std::endl;
    std::cout << lower_i << "-" << upper_i << std::endl;
    for (unsigned long long i = lower_i; i <= upper_i; ++i) {
      std::string i_str = std::to_string(i);
      //      if (i_str.length() % 2 != 0) {
      //        continue;
      //      }
      int idx = i_str.length() / 2;
      if (i_str.compare(0, idx, i_str, idx, idx + 1) == 0) {
        std::cout << i << " is invalid" << std::endl;
        sum += i;
      }
    }
  }
  std::cout << "result is : " << sum << std::endl;
  return sum;
}

int main() {
  std::string file_name =
      "/Users/edlym96/Documents/Projects/adventofcode/2025/day2/input1.txt";
  std::string test_file_name =
      "/Users/edlym96/Documents/Projects/adventofcode/2025/day2/test.txt";
  return solve_1(file_name);
  // return solve_1(test_file_name);
}
