Some of us think that the example of put function professor gave us is a little bit weird so I implement by only giving it an input parameter "value", which also works, if you want to add a value to the server just put(value), the detail is in the code you can check it if you want. 

At the end of the code in cache_client.py, I test some operation, which is put all users, get one user by key, delete one user by key and then try to get the deleted key which will show "The key does not exist".

Please open four servers 0 - 3 and then run client to test it out, if you want to add any operation just add print(operation(...)) (operation = put,get or delete). 

Thank you!
