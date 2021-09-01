import base2
base2.setAppURL("http://127.0.0.1:5000/")
base2.setInfuraId('78f5577f2b5a4bda8419b718c57b8718')

print(base2.appURL)
print(base2.infuraProvider)
base2.addUsers(["neeraj"])