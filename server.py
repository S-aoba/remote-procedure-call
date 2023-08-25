import socket
import os
import math
import json

class Callable:
    #ラムダにする
    def sum_numbers(numbers):
      total = 0
      for num_str in numbers:
          try:
              num = float(num_str)
              total += num
          except ValueError:
              # 数字に変換できない場合は無視します
              pass
      return total

    def floor(args):
        print('floor')
        def func(args):
            return math.floor(float(args[0]))
        return func(args)

    def nroot(args):
      print('nroot')

      if len(args) != 2:
          raise ValueError("引数の数は2つである必要があります")

      x_str, n_str = args[0], args[1]

      try:
          x = float(x_str)
          n = float(n_str)
      except ValueError:
          raise ValueError("xとnは数値である必要があります")

      if n == 0:
          raise ValueError("nは0にすることはできません")
      if x < 0 and n % 2 == 0:
          raise ValueError("負の数の偶数乗根は実数ではありません")

      result = x ** (1/n)
      return result

    def reverse(args):
        print('reverse')
        reversed_list = args[::-1]  # 逆順に並べ替え
        return reversed_list

    def validAnagram(args):
        print('validAnagram')

        s1 = args[0].lower().replace(" ", "").replace("'","")
        s2 = args[1].lower().replace(" ", "").replace("'","")
        print(s2)

        if len(s1) != len(s2): return False

        cache = []
        for i in range(26):
            cache.append(0)

        for i in range(len(s1)):
            cache[ord(s1[i]) - 97] += 1
            cache[ord(s2[i]) - 97] -= 1

        # 最大値0、最小値0の時のみ、アナグラムになります
        return max(cache) == 0 and min(cache) == 0

    def sortArr(args):
        print('sort')
        cleaned_args = [s.replace("'", "") for s in args]
        print(cleaned_args)
        # 文字列をソート
        sorted_strings = sorted(cleaned_args)

        return sorted_strings

# ソケット生成クラス
class Socket:

    def createSocket():

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = "/tmp/json_rpc_socket.sock"

        # ファイルが既に存在しないことを確認する
        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass

        # ソケットをアドレスに紐付ける
        print("Starting up on {}".format(server_address))
        sock.bind(server_address)

        # 接続
        sock.listen(1)

        # # サーバが常に接続を待ち受けるためのループ
        while True:
            connection, _ = sock.accept()
            try:

                while True:
                    data = connection.recv(1024)
                    # リクエストをdictに変換
                    dict = json.loads(data)
                    answer = Handler.handle_request(dict)
                    # print(dict)

                    # print("answer: ", answer)
                    # レスポンスの送信
                    if data:
                        connection.sendall(json.dumps(answer).encode())

                    else:
                        print("no data from")
                        break

            finally:
                # 接続のクリーンアップ
                print("Closing current connection")
                connection.close()
                break

class Handler:
    def handle_request(dict):
        method = dict['method']
        params = dict['params'].split(' ')

        table = {
            'sum': Callable.sum_numbers,
            'floor': Callable.floor,
            'nroot': Callable.nroot,
            'reverse': Callable.reverse,
            'validAnagram': Callable.validAnagram,
            'sort': Callable.sortArr,
        }
        if table[method]:
            result = table[method](params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        else:
            return {
                'result': None,
                'error': 'Unknown method',
                'id': dict['id']
            }


def main():
    Socket.createSocket()
    return 0


if __name__ == '__main__':
    main()
