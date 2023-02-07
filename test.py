import sys

args = sys.argv
if len(args) != 2:
    print('invalid number of system arguments.')
    sys.exit(1)

if args[1] == 'scroll_view':
    from tests import scroll_view

if args[1] == 'all':
    from tests import scroll_view

