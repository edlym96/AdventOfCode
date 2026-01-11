#include <cmath>
#include <fstream>
#include <iostream>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

bool is_repeating(std::string &in) {
  int idx = in.length() / 2;
  for (int count = 1; count <= idx; ++count) {
    int left = 0;
    int right = count;
    bool flag = true;
    if (in.length() % count != 0) {
      continue;
    }
    while (right < in.length()) {
      if (in.compare(left, count, in, right, count) != 0) {
        flag = false;
        break;
      }
      left += count;
      right += count;
    }
    if (flag) {
      return true;
    }
  }
  return false;
}

int solve_2(std::string &filename) {
  std::ifstream in{filename};
  std::string line{};
  unsigned long long sum = 0;
  while (std::getline(in, line, ',')) {
    int idx = line.find('-');
    std::string lower = line.substr(0, idx);
    std::string upper = line.substr(idx + 1, line.length());
    unsigned long long lower_i = std::stoull(lower);
    unsigned long long upper_i = std::stoull(upper);
    std::cout << lower_i << "-" << upper_i << std::endl;
    for (unsigned long long i = lower_i; i <= upper_i; ++i) {
      std::string i_str = std::to_string(i);
      if (is_repeating(i_str)) {
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
  return solve_2(file_name);
  // return solve_2(test_file_name);
}
