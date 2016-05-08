#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys  # 修改默认编码
import os   # 添加系统路径

from src.main import EEBook
from src.tools.debug import Debug
from src.constants import __version__
from src.utils import log
from src.tools.match import Match
from src.login import Login
from src.constants import url_info

reload(sys)
base_path = unicode(os.path.abspath('.').decode(sys.stdout.encoding))

# print base_path
# sys.path.append(base_path + '/src/lib')

# Python早期版本可以直接用sys.setdefaultencoding('utf-8')，新版本需要先reload一下
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(100000)  # 为BS解析知乎上的长答案增加递归深度限制

short_options = 'Vhgu:r:i:l:'
long_options = ['version', 'help', 'url', 'gui', 'info', 'login']


help_info = 'Usage: ee-book [OPTION]... [URL]... \n\n'

help_info += '''Starup options:
-V | --version                  Print version and exit
-h | --help                     Print help and exit
-i | --info                     Print information of URLs
-l | --login <URL>              Login via command line
\n
'''

help_info += '''Run options:
-g | --gui                      Graphical user interface. under developing.
-u | --url <URL>                URL to download, if not setted, read from ReadList.txt(default)
-r | --file <file-path>         Read from the given file. Notice: only one kind could be accepted in one file
'''


if __name__ == '__main__':
    def version():
        log.info_log('version %s' % __version__)

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as err:
        log.error_log(u"try ee-book --help for more options")
        sys.exit(2)
    for option, args in opts:
        if option in ('-V', '--version'):
            version()
            sys.exit()
        elif option in ('-h', '--help'):
            version()
            print(help_info)
            sys.exit()
        elif option in ('-g', '--gui'):
            # graphviz = GraphvizOutput(output_file='filter_gui.png')
            # with PyCallGraph(output=graphviz, config=config):
            from PyQt4.QtGui import QApplication
            from PyQt4.QtGui import QIcon
            from src.gui.ui import MainWindow
            from src.resources import qrc_resources
            app = QApplication(sys.argv)
            app.setWindowIcon(QIcon(":/icon.png"))
            app.setApplicationName('EE-Book')
            window = MainWindow()
            window.show()
            sys.exit(app.exec_())
        elif option in ('-l', '--login'):
            url = args
            recipe_kind = Match.get_recipe_kind(url)
            if recipe_kind != 'zhihu':
                print("Unsupport type! Only zhihu are supported now")
                print("Please try again.")
                sys.exit()
            zhihu = EEBook(recipe_kind=recipe_kind)    # Init path, e.g. config, only zhihu are supported now
            login = Login(recipe_kind=recipe_kind)
            login.start()
            sys.exit()
        elif option in ('-u', '--url'):
            url = args
            recipe_kind = Match.get_recipe_kind(url)
            if recipe_kind == 'Unsupport type':
                print("Unsupport type!")
                print("Please try again.")
                sys.exit()
            game = EEBook(recipe_kind=recipe_kind, url=url)
            game.begin()
            sys.exit()
        elif option in ('-i', '--info'):
            url = args
            url_kind = Match.get_url_kind(url)
            if url_kind == 'Unknow type':
                print('Unsupport website or url type. \nPlease check url.')
            else:
                info = url_info[url_kind]
                print(info)
            sys.exit()
        elif option in('-r', '--file'):
            file_name = args
            log.print_log(u'read from %s' % file_name)
            with open(file_name, 'r') as read_list:
                line = read_list[0]
                recipe_kind = Match.get_recipe_kind(line)
                if recipe_kind == 'Unsupport type':
                    print('Unsupport website or url type. \nPlease check url.')
                    sys.exit()
            print(u"website type:" + str(recipe_kind))
            game = EEBook(recipe_kind=recipe_kind, url=None, read_list=file_name)
            game.begin()
            sys.exit()

    from PyQt4.QtGui import QApplication
    from PyQt4.QtGui import QIcon
    from src.gui.ui import MainWindow
    from src.resources import qrc_resources
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon.png"))
    app.setApplicationName('EE-Book')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



