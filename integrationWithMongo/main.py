import pymongo as pyM
import datetime
import pprint
import pymongo

client = pyM.MongoClient("")#inserir string de conexão

db = client.test
collection = db.test_collection

print(db.test_collection)

#definição de info para compor arquivo
post = {

    "nome":"Jack",
    "cpf": "123456789",
    "endereço":"rua asdfafdsadfs",
    "tipo_conta": "corrente",
    "agencia": 1001,
    "numero": 10651601,
    "saldo": 50.50,    
    "date": datetime.datetime.now()

}

auxiliar = 0

if auxiliar == 0:
    # preparando para submeter as infos
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)

    print(db.posts.find_one())

    pprint.pprint(db.posts.find_one())

    #bulk inserts

    new_posts = [{

                    "nome":"James",
                    "cpf": "8988498489",
                    "endereço":"rua sadfas651as6d",
                    "tipo_conta": "conjunta",
                    "agencia": 1001,
                    "numero": 6516516,
                    "saldo": 900.50,    
                    "date": datetime.datetime.now()
                },         
                {
                    "nome":"Rodrigo",
                    "cpf": "666666666",
                    "endereço":"rua eeeeeeeeeeeee",
                    "tipo_conta": "salario",
                    "agencia": 1001,
                    "numero": 999999,
                    "saldo": 20000.50,    
                    "date": datetime.datetime.now()
                }]

    result = posts.insert_many(new_posts)
    print(result.inserted_ids)

    print("Recuperação final")
    pprint.pprint(db.posts.find_one({"nome":"Jack"}))

    #pprint.pprint(post.find())

    print("\nDocumentos presentes na coleção post")
    for post in posts.find():
        pprint.pprint(post)




elif auxiliar== 1:

    db = client.test
    posts = db.posts

    for post in posts.find():
        pprint.pprint(post)

    print(posts.count_documents({}))

    print(posts.count_documents({"nome":"James"}))
    print(posts.count_documents({"numero":6516516}))

    pprint.pprint(posts.find_one({"numero":6516516}))

    print("Recuperando info da coleção post ede maneira ordenada")
    for post in posts.find({}).sort("date"):
        pprint.pprint(post)
        print("\n")

    result = db.profiles.create_index([('nome', pymongo.ASCENDING)], unique = True)

    print(sorted(list(db.profiles.index_information())))


    user_profile_user= [

        {'user_id': 211, 'name':'James'},
        {'user_id':212, 'name':'Rodrigo'}   

    ]

    result = db.profile_user.insert_many(user_profile_user)


    collections = db.list_collection_names()

    print("Coleções armazenadas no mongoDB")
    for collection in collections:
        print(collection)

elif auxiliar==2:
        #Apagar
        db = client.test
        posts = db.posts 
        db['posts'].drop()

        db['profiles'].drop()

        print(posts.delete_one({"nome":"Jack"}))

        client.drop_database('test')
        print(db.list_collection_names())