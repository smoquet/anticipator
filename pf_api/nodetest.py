from Naked.toolshed.shell import execute_js

mode = 'eventsearch'
query = 'frenchcore'
num = 20
args = mode + ' "' + query + '" ' + str(num)

success = execute_js('event.js', args)

if success:
  print success
else:
  print 'jammer joh'
