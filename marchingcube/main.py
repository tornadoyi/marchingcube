import os
from marchingcube.app import Application


os.environ['DATASET_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()