CFLAGS=-Wall -O3
LIBS=-lm

.PHONY: all test

all: c4bot

test: c4bot
	bash -c 'pushd ..; ./runner.py ./smeagol ./c4bot/c4bot; popd'

c4bot: c4bot.c
	$(CC) $(CFLAGS) c4bot.c $(LIBS) -o c4bot