from Naked.toolshed.shell import execute_js

mode = 'eventsearch'
query = 'prspct xl'
num = 7
args = mode + ' "' + query + '" ' + str(num)

success = execute_js('event.js', args)

if success:
  print success
else:
  print 'jammer joh'
