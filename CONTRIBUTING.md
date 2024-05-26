# CONTRIBUTING.md

## guidelines

feel free to do whatever you want, as long as it's not illegal/racist, even if it's just a joke. submit ALL the pull requests you want!!!!!

## how you should contribute to the project

you should have knowledge of python.

1. if you're not a collaborator, start by forking the repo
2. clone your repo onto your local machine
3. you should install python3 if you don't have it already (please install the latest version for best safety)
4. now you can make whatever changes you want to main.py!!!!
5. commit and push then open a pull request
6. you should know how to do this why did you read this

## how slang works

unless you think you can figure it out yourself (try it go ahead) you might wanna read this

so, slang i dont think has a lexer...

slang works by reading each line and checking if a line starts with a function name. if not, it raises an error saying there's no function. slang is based all around functions. defining variables is functions!!!!

if it finds something, it takes out the function name (simple replace statement) and splits the args with a space as the splitter, keeping everything in quotes as one arg

then it goes through the function's annotations and converts each argument to what it's supposed to be.

then, it runs the function with the arguments.

this horrible interpreter is a result of me taking the easiest route to implement on every fucking turn. it's simple though.

## how do i add new functions?

to add new functions, check out the `functions` list. it's a list of tuples with 2-3 items containing the function name, the function, and an optional description of it.

what you're supposed to do here is define a normal python function, with annotated arguments, then add a tuple to `functions`.

btw, for anything that involves numbers, you should probably use a float for its annotation unless you NEED whole numbers.

here's an example of how a slang function looks like:

```python
def exp(x: float, y: float):
    return x ** y
```

and an example of the tuple you'd add to `functions`:

```python
("exp", exp, "Calculates x to the power of y.")
```

and an example of how you'd use that function now:

```sponge
var fun out exp 2 64
print $out
```

`test.sponge` is for ALL the testing fuckery you want do WHATEVER you want with it!!!!!! PLEASE test in `test.sponge` and never ever remove your tests, this is so we can build up a relic for the future generations

## conclusion

slang is a very great and stable language you should totally contribute to!

just don't be like @ocaminty (you know what you did @ocaminty)
