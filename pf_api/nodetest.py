from Naked.toolshed.shell import execute_js

# mode = 'eventsearch'
mode = 'lineupsearch'
query = 'frenchcore'
# num = 20
num = 311374
args = mode + ' "' + query + '" ' + str(num)
# args = mode + ' "' + query + '"'

success = execute_js('event.js', args)

if success:
  print success
else:
  print 'jammer joh'
