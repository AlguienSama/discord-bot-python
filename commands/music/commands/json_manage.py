import json

queueFile = './utils/ddbb/queue.json'


def get_songs():
    return json.load(open(queueFile))


def get_queue(guild):
    return get_songs()[f'{guild}']


def set_songs(queue):
    with open(queueFile, 'w') as outFile:
        json.dump(queue, outFile)


def add_song(guild, user, name, url):
    queue = get_songs()
    song = {'name': name, 'url': url, 'user': user}
    
    try:
        queue[f'{guild}'].append(song)
    except:
        queue[f'{guild}'] = [song]
    
    set_songs(queue)
    return queue[f'{guild}']


def del_songs(guild, index=1, index2=1):
    print('DEL SONGS')
    songs = get_songs()
    if index == index2:
        print(songs[f'{guild}'].pop(index-1))
    else:
        del songs[f'{guild}'][index-1:index2-1]
    set_songs(songs)
    return songs[f'{guild}']

