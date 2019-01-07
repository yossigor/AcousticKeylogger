import itertools,functools

guesses = [
[("p",12),("i",5),("o",8),("l",7)],
[("a",20),("q",10),("e",7),("s",4)],
[("a",12),("q",8),("s",7),("d",6)],
[("a",13),("s",9),("e",5),("d",6)],
[("a",13),("e",11),("s",6),("w",4)],
[("o",17),("i",9),("k",6),("j",4)],
[("r",13),("t",7),("e",6),("f",5)],
[("d",15),("s",6),("f",4),("e",4)],
]



smart_dict = list(map(lambda tuple:list(tuple) ,list(itertools.product(*guesses))))
smart_dict = list(map(lambda list:(list,functools.reduce(lambda a,b: a+b[1], list, 0)) ,smart_dict))
smart_dict.sort(key = lambda guess: guess[1])
smart_dict.reverse()
for guess in smart_dict:
    print(''.join((list(map(lambda tuple: tuple[0],guess[0])))))
