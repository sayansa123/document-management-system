def retrieve_individual(i):
    return{
        'file_id':i['file_id'],
        'description':i['description'],
        'tags':i['tags'],
        'uploaded_at':i['uploaded_at']
    }

def retrieve_individual2(i, tag):
    if tag in i['tags']:
        return{
            'file_id':i['file_id'],
            'description':i['description'],
            'tags':i['tags'],
            'uploaded_at':i['uploaded_at']
        }
