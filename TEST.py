""" 내용에서 숫자만 추출하는 방법
import re
temp = '<span class="style-scope ytd-grid-video-renderer">스트리밍 시간: 3주 전</span>'
number = re.findall("\d+", temp)
print(number[0])
"""
# 텐서플로우 정상 동작 테스트
# Successfully opened dynamic library cudart64_110.dll 나오면 정상
# import tensorflow as tf

from collections import Counter


def sort_by_frequency(n):
    # n을 카운터
    most_n = Counter(n)
    
    most_n_list = sorted((count, -num) for num, count in most_n.items())
    result = []

    for count, num in most_n_list:
        for i in range(count):
            result.append(-num)

    return result


print(sort_by_frequency([3, 8, 8, 3, 2, 8, 1, 2, 4, 56]))