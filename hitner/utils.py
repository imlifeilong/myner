import os
import jieba

from pyltp import NamedEntityRecognizer, Segmentor, \
    Postagger, CustomizedSegmentor, \
    Parser, SementicRoleLabeller, SentenceSplitter


class HLT(object):
    def __init__(self, model_path):
        self.model_path = model_path
        self.cws_model_file = os.path.join(self.model_path, 'cws.model')
        self.pos_model_file = os.path.join(self.model_path, 'pos.model')
        self.ner_model_file = os.path.join(self.model_path, 'ner.model')
        self.par_model_file = os.path.join(self.model_path, 'parser.model')
        self.srl_model_file = os.path.join(self.model_path, 'pisrl_win.model')

    def seg(self, txt):
        # 分词
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(self.cws_model_file)  # 加载模型
        words = segmentor.segment(txt)  # 分词
        words_list = list(words)  # words_list列表保存着分词的结果
        segmentor.release()  # 释放模型
        return words_list

    def pos(self, txt):
        # 词性标注
        postagger = Postagger()  # 初始化实例
        postagger.load(self.pos_model_file)  # 加载模型
        postags = postagger.postag(txt)  # 词性标注
        postags_list = list(postags)  # postags_list保存着词性标注的结果
        postagger.release()  # 释放模型

        return postags_list

    def net(self, word, post):
        # 命名实体识别
        recognizer = NamedEntityRecognizer()  # 初始化实例
        recognizer.load(self.ner_model_file)  # 加载模型
        netags = recognizer.recognize(word, post)  # 命名实体识别
        netags_list = list(netags)  # netags_list保存着命名实体识别的结果
        recognizer.release()  # 释放模型

        return netags_list

    # def par(self, word, post):
    #     parser = Parser()  # 初始化实例
    #     parser.load(self.par_model_file)  # 加载模型
    #     arcs = parser.parse(word, post)  # 句法分析
    #
    #     rely_id = [arc.head for arc in arcs]
    #     relation = [arc.relation for arc in arcs]
    #     heads = ['ROOT' if id == 0 else word[id - 1] for id in rely_id]
    #     # print([(word[arc.head - 1], arc.relation, word[i]) for i, arc in enumerate(arcs)])
    #     # # print(heads)
    #     for i in range(len(word)):
    #         print(relation[i] + '(' + word[i] + ', ' + heads[i] + ')')
    #     parser.release()  # 释放模型
    #
    #     return arcs

    # def srl(self, word, post, arcs):
    #     labeller = SementicRoleLabeller()  # 初始化实例
    #     labeller.load(self.srl_model_file)  # 加载模型
    #     # arcs 使用依存句法分析的结果
    #     roles = labeller.label(word, post, arcs)  # 语义角色标注
    #     for role in roles:
    #         tmp = ["%s:[%d %d] %s" % (arg.name, arg.range.start, arg.range.end,
    #                                   ''.join(word[arg.range.start:arg.range.end])) for arg in role.arguments]
    #
    #         # print(word[role.index], role.index, "".join(tmp))
    #     labeller.release()  # 释放模型

    def start(self, txt):
        w_list, p_list, n_list = [], [], []
        words_list = self.seg(txt)
        # words_list = self.cus_seg(txt)
        postags_list = self.pos(words_list)
        netags_list = self.net(words_list, postags_list)

        w_len = len(words_list)
        for i in range(w_len):
            # print(words_list[i], postags_list[i], netags_list[i])
            if netags_list[i] != 'O':
                # 分词结果
                w_list.append(words_list[i])
                # 词性标注结果
                p_list.append(postags_list[i])
                # 命名实体识别结果
                n_list.append(netags_list[i])

        a1 = len(w_list)
        # 提取机构名
        i = 0
        orignizations = []
        while i < a1:
            if n_list[i] == 'S-Ni':
                orignizations.append(w_list[i])
            elif n_list[i] == 'B-Ni':
                temp_s = ''
                temp_s += w_list[i]
                j = i + 1
                while j < a1 and (n_list[j] == 'I-Ni' or n_list[j] == 'E-Ni'):
                    temp_s += w_list[j]
                    j += 1
                orignizations.append(temp_s)
            i += 1
        # 删除重重出现的机构名
        return orignizations


if __name__ == '__main__':
    model_path = './model/ltp_data_v3.4.0'
    txt = '''招标人：    定边县教育和体育局    招标代理机构：    陕西新世纪工程管理咨询有限公司\n地址：    定边县东正街41号县政府大院    地址：    榆林市开发区沙河口市场世纪嘉兴 酒店五楼\n联系人：    陈世军    联系人：    郭秀梅\n电话：    0912-4215408    电话：    0912-2256048\n邮编：        邮编：    \n开户银行：        开户银行：    中国银行股份有限公司榆林肤施路支行\n账号：        账号：    103605790456'''
    htl = HLT(model_path)
    res = htl.start(txt)
    print(res)
