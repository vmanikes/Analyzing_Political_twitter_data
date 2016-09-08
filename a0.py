from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.
    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.
    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    ###TODO
    pass
    lines = [line.rstrip('\n') for line in open(filename)]
    return lines


def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)
    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup
    In this example, I test retrieving two users: twitterapi and twitter.
    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    pass
    request = robust_request(twitter,'users/lookup',{'screen_name':screen_names})
    #request = twitter.request('users/lookup',{'screen_name':screen_names})
    users = [r for r in request]
    user_info = []
    i = 0
    while i < len(users):
    #for i in range(0,4):
        user_info.append(users[i])
        i = i + 1
    return user_info

def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.
    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.
    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    pass

    request = robust_request(twitter, 'friends/ids', {'screen_name': screen_name})
    #request = twitter.request('friends/ids',{'screen_name':screen_name})#
    id = [i for i in request]
    return sorted(id)

def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.
    Store the result in each user's dict using a new key called 'friends'.
    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing
    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    pass
    i = 0
    while i < len(users):
    #for i in range(0,4):
        u = users[i]
        friend_list = get_friends(twitter,u['screen_name'])
        users[i]['friends'] = friend_list
        i = i + 1

def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    pass
    for i in range(0,4):
        u = users[i]
        print(u['screen_name'], end = "")
        print(' %d' % len(users[i]['friends']))

def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter
    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    pass

    count = Counter()
    kc = []
    k = 0
    while k < len(users):
    #for i in range(0,4):
        kc.append(users[k]['friends'])
        k = k + 1
    for i in kc:

        for j in i:

            count[j]+=1
    return count



def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.
    Args:
        users...The list of user dicts.
    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.
    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    pass
    us = []
    i = 0
    while i < len(users):
        us.append(users[i]['friends'])
        i = i + 1

    user_set = []

    for k in range(0,len(us)):
        for l in range(k+1,len(us)):

            user_set.append(set(us[k]).intersection(set(us[l])))

    n = 0
    overlap = []
    for k in range(0, len(us)):
        for l in range(k + 1, len(us)):
            overlap.append((users[k]['screen_name'],users[l]['screen_name'],len(user_set[n])))
            n= n+1

    return sorted(overlap,key = lambda x: x[2],reverse = True)

def followed_by_hillary_and_donald(users, twitter):

    hilary = users[2]['friends']
    donald = users[3]['friends']

    HD = set(hilary) & set(donald)
    DH = list(HD)

    request = robust_request(twitter, 'users/lookup', {'user_id': DH[0]})

    hiddern_user = [r for r in request]
    return hiddern_user[0]['screen_name']


def create_graph(users, friend_counts):

    graph = nx.Graph()
    #Adding Candidate as a node
    for i in range(0,len(users)):
        graph.add_node(users[i]['screen_name'])

        for key in users[i]['friends']:
            if friend_counts[key] > 1:
                graph.add_node(key)

    for i in range(0,len(users)):
        for key in users[i]['friends']:
            if friend_counts[key] > 1:
                graph.add_edge(users[i]['screen_name'],key)

    return graph


def draw_network(graph, users, filename):
    labels = {users[0]['screen_name']:users[0]['screen_name'],users[1]['screen_name']:users[1]['screen_name'],users[2]['screen_name']:users[2]['screen_name'],users[3]['screen_name']:users[3]['screen_name']}
    plt.figure(figsize=(15 ,15))
    nx.draw_networkx(graph,labels=labels,width = 0.1, node_size = 100)
    plt.axis("off")
    plt.savefig(filename)


def main():
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()
