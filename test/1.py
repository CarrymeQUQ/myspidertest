def main():
    # s = input("请输入s字符串:")
    # t = input("请输入t字符串:")
    s = "This is C programming text"
    t = "This is a text for C programming"

    # 判断字符串是否为空
    if s.strip() == "" or t.strip() == "":
        return "NULL"

    # 通过分隔符(默认以空格为分隔符)对字符串进行切片生成列表
    list_s = s.split()
    list_t = t.split()

    # 判断列表是否满足有第二公共单词
    if len(list_s) < 2 or len(list_t) < 2:
        return "NULl"

    # 新建一个列表存储公共单词
    res = []
    # 遍历并进行比较
    for a in list_s:
        for b in list_t:
            if a == b:
                # 放到数组中
                res.append(a)

    # 判断是否有2个公共单词以上
    if len(res) > 1:
        print(res[0])
    else:
        return "NULL"


if __name__ == "__main__":
    main()
