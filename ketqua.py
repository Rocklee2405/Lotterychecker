import requests
import bs4
import argparse


class ServerError(Exception):
    pass


def ketqua():
    resp = requests.get('http://ketqua.net')
    if resp.status_code >= 500:
        raise ServerError('Cannot connect to server!')
    tree = bs4.BeautifulSoup(resp.text, features="lxml")
    date = tree.find(attrs={'id': 'result_date'}).text
    prizes = {}
    parameters = [('Đặc biệt', 0, 1), ('Giải nhất', 1, 1), ('Giải nhì', 2, 2),
                  ('Giải ba', 3, 6), ('Giải tư', 4, 4), ('Giải năm', 5, 6),
                  ('Giải sáu', 6, 3), ('Giải bảy', 7, 4)]
    for prize, order, nums in parameters:
        prizes[prize] = [tree.find(
            attrs={'id': 'rs_{}_{}'.format(order, i)}).text
            for i in range(nums)]
    return prizes, date


def check_ketqua(*args):
    prizes, date = ketqua()
    list_prizes = [i[-2:] for j in prizes for i in prizes[j]]
    count = 0
    print(date)
    for num in args:
        if num in list_prizes:
            count += 1
            cnt = list_prizes.count(num)
            print('Bạn đã trúng lô x{1} với số {0}'.format(num, cnt))
    if count == 0:
        print('Rất tiếc bạn không trúng lô\nDanh sách giải:')
        for prize in prizes:
            print(prize, ':', prizes[prize])
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Check Vietnamese lottery number at ketqua.net')
    parser.add_argument('numbers', nargs='*', type=str)
    args = parser.parse_args()
    check_ketqua(*args.numbers)


if __name__ == "__main__":
    main()
