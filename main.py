from date_functions import str2date, normalize_date, date2str
import argparse
import sys
import ui

def main():
    parser = argparse.ArgumentParser(description='Normalize date')
    parser.add_argument('date', nargs='?', help='date to normalize')
    parser.add_argument('-i', '--iformat', default="%Y.%m.%d %H:%M:%S", help='input date format, default=%%Y.%%m.%%d %%H:%%M:%%S')
    parser.add_argument('-o', '--oformat', help='output date format, default=IFORAMT')
    parser.add_argument('--ui', action='store_true', help='run UI instead of command line')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        try:
            app = ui.DateNormalizeTool()
        except Exception as e:
            print('An error occurred while trying to create the GUI:')
            print(e)
            return
        app.run()
        return
    
    args.oformat = args.oformat if args.oformat else args.iformat
    
    if args.ui:
        try:
            app = ui.DateNormalizeTool()
        except Exception as e:
            print('An error occurred while trying to create the GUI:')
            print(e)
            return
        app.create_widgets()
        app.set_date(*str2date(args.date, date_format=args.iformat)) if args.date else ...
        app.mainloop()
        return
    
    try:
        date = normalize_date(*str2date(args.date, date_format=args.iformat))
        print(date2str(*date, date_format=args.oformat))
    except Exception as e:
        print('An error occurred:')
        print(e)


if __name__ == '__main__':
    main()
