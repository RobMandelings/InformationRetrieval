import flask_restful


class SearchResource(flask_restful.Resource):

    def get(self, state_encoding: str):
        """
        Handles get requests for IR queries made by the user
        """
        # result = parse.unquote(state_encoding)
        return {'msg': state_encoding}
        pass
