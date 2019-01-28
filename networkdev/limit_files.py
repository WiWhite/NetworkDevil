import os
import datetime



backupsdir = os.path.join(os.path.dirname(
                         os.path.dirname(os.path.abspath(__file__))), 'BACKUPS')

def scandel(scandir):

    for dirpath, dirnames, filenames in os.walk(scandir):
       for file in filenames:
          curpath = os.path.join(dirpath, file)
          file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
          diff_age = datetime.datetime.now() - file_modified
          max_age = datetime.timedelta(days=6)

          if diff_age > max_age:
              os.remove(curpath)

def main():
    scandel(backupsdir)

if __name__ == '__main__':
    main()
