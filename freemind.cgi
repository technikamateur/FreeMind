import cgi

print("Content-Type: text/html")
print("")

arguments = cgi.FieldStorage()
for i in arguments.keys():
  print arguments[i].value
