from logger import log
from ete3 import Tree
from ete3 import TreeStyle


class My_Tree:
    '''
    Объект генерирующий дерево в файл и в GUI
    1. Принимает файл сгенерированный Link_Parser
    2. Читает строки из файла(п. 1) это генератор
    3. Генерирует дерево
     3.1 Если первого элемента ссылки нет в дереве то добавляет его
     3.2 Если ссылка состоит более чем из одного элемента то остальные элементы прикрепляются как дети предыдущей и
         проверяем не является ли элемент веткой
    4. Взуализирует дерево в GUI
    '''

    def __init__(self):
        self.tree = Tree(format=1)

    def __str__(self):
        return self.tree.get_ascii(show_internal=True)  # Подписываеи ветки

    def read_links(self, file_links):
        with open(file_links, 'r') as f:
            try:
                links = f.read().splitlines()

                for link in links:
                    link = link.split('/')
                    link.pop(0)
                    if link[-1] == '':
                        link.pop(-1)
                    yield link
            except Exception as e:
                log.error(e)

    def make_tree(self, file_links):
        log.info('START GENERATE TREE')
        split_links = self.read_links(file_links)
        for selection_ln in split_links:
            if selection_ln:

                if selection_ln[0] not in self.tree:

                    self.tree.add_child(name=selection_ln[0])

                    if len(selection_ln) > 1:

                        self.node_build(selection_ln)

                elif selection_ln[0] in self.tree and len(selection_ln) > 0:

                    self.node_build(selection_ln)

            else:
                continue

    def node_build(self, link):
        for ln in link[1:]:
            if ln not in self.tree:
                val_child = link.index(ln)-1
                node = self.tree&link[val_child]
                node.add_child(name=ln)

    def draw_tree(self):
        style = TreeStyle()
        style.show_leaf_name = True
        style.show_branch_length = True
        style.show_branch_support = True
        self.tree.show(tree_style=style)
        self.tree.render('tree.png', w=183, units="mm", tree_style=style)



