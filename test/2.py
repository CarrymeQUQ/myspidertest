def main():
    N = int(input("请输入整数N(N <= 10000):"))
    # N = 16
    # 能够拆分成连续整数相加的数　一定满足等差数列的求和公式　 (min+max)*(max-min+1)/2=N

    # 设置一个布尔值　用来判断输入的整数是否能分解为连续整数的和
    flag = False
    # 从1开始循环遍历
    for x in range(1, N):
        min = x
        for y in range(min, N):
            max = y
            # 如果满足条件就返回最小值和最大值
            if (min + max) * (max - min + 1) / 2 == N:
                # print(min,max)
                flag = True
                # 定义一个列表用来生成连续数
                res_list = []
                for z in range(min, max + 1):
                    res_list.append(str(z))
                # print(res_list)
                # 每个数字之间有一个空格
                print(" ".join(res_list))

    if not flag:
        print("NONE")


if __name__ == "__main__":
    main()
