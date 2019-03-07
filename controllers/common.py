from controllers.base import Base


class Common(Base):

    def __init__(self):
        super().__init__()

    # 资产类型列表
    def assets_type_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        data = [
            {
                "id": "1",
                "name": "数字货币"
            },
            # {
            #     "id": "2",
            #     "name": "股票"
            # },
            # {
            #     "id": "3",
            #     "name": "商品期货"
            # }
        ]
        return self.ret_json(self.ok, self.msg, data)

    # 交易所列表列表
    def exchange_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        data = [
            {
                "id": "1",
                "name": "OKEX"
            },
            {
                "id": "2",
                "name": "BITMEX"
            }
        ]
        return self.ret_json(self.ok, self.msg, data)

    # blue-test
    def blue_test(self):
        data = [
            {
                "id": "1",
                "name": "数字货币"
            },
        ]
        return self.ret_json(self.ok, self.msg, data)
