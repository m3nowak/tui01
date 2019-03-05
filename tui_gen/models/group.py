from tui_gen.models.period import Period


class Group(object):
    def __init__(self, name, period_list):
        self.name = name
        self.period_list = period_list

    @staticmethod
    def list_factory(name, list_raw):
        return Group(name, [Period.dict_factory(period_dict) for period_dict in list_raw])
