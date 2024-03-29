March 2024 - I dislike Go
==============================

This page is a work in progress blog post about all the things I hate about Go.

Things to know


Complaints


* Reference types

  * Maps, channels and slices are reference types, so you can assign nil to either of them

    * Although slices are reference types, you may still need to pass them as a pointer if you are changing their length: https://stackoverflow.com/questions/31170368/go-reference-types-as-arguments

* Maps

  * Go maps don't support iteration in insertion order https://stackoverflow.com/questions/9619479/go-what-determines-the-iteration-order-for-map-keys
  * Go maps must have keys that are `comparable <https://go.dev/ref/spec#Comparison_operators>`_ (https://go.dev/blog/maps)

    * Problem with this is that for something to be comparable, it must implement ==, !=, and optionally stuff like <, >. Most of the time, these will be automatically implemented for you, but you can never override/overload the default behavior

      * Weirdly enough, interface types are comparable by default: https://stackoverflow.com/questions/47224422/how-can-interfaces-be-comparable-and-at-the-same-time-functions-not
      * Slices, maps, and functions are not comparable

* Iteration

  * The ``range`` keyword allows you to iterate over: entries of a map, elements of a slice or array, characters of a string, a channel

    * The behavior of the range keyword is different for each type.
    * There is no way to create a custom iterator that can utilize the ``range`` keyword.

* Slices

  * I don't understand this too much to criticize it, but this:

    * https://news.ycombinator.com/item?id=39477821
    * https://go.dev/blog/generic-slice-functions

* JSON

  * If you unmarshal JSON into an ``interface{}``, all objects will be of the type ``map[string]interface{}``. Because a map is being used, the order of the keys is lost.
  * Custom JSON unmarshaling is difficult. If you want to do some sort of complex unmarshaling of an object into a type, you will likely have to write your own JSON parser

    * The Unmarshaler interface just has a method that takes an array of bytes, so you get to use that bytes array however you see fit. This usually means leaving the parsing up to you without much help from the standard libraries. https://pkg.go.dev/encoding/json#Unmarshal

      * You can use the Decoder if you want to: https://pkg.go.dev/encoding/json#Decoder It will simplify your parsing quite a bit, but you're still dealing with the tokens, rather than the JSON constructs at a higher level.

        * However, the `Decode()` function does not have a way to "try" to parse something, as it consumes the reader with no way to get it back. If you try to buffer the reader and initialize a new decoder, it won't work because the decoder tries to make sure the JSON is valid, which means you can't start using a new decoder halfway through valid JSON.
        * If you were to read a token using decoder `a`, then call `a.Buffered()`, that new buffered reader would give you data from right after the token you just read, including commas!
        * It's hard to compare Tokens. It's not well documented. Remember to convert `'['` to a `json.Delim`, otherwise the comparison won't work.

    * If you need to do some sort of subtype thing, you'll likely just be able to unmarshal the JSON into a ``map[string]interface{}`` and then call the unmarshaler for the subtype after reading something like the ``type`` property.

* Lack of enums

  * https://www.zarl.dev/articles/enums

* Generics

  * Generics were added in Go 1.18, which means that lots and lots of Go code don't use generics!

    * The two most popular data structure libraries don't have great support for generics

      * https://github.com/emirpasic/gods supports generics, but does not have a stable release yet
      * https://github.com/Workiva/go-datastructures

* Interfaces

  * Interfaces in Go are simple. Implementing them is even easier. You don't have to explicitly say that you are implementing an interface.

    * This has the advantage of being able to define interfaces that adhere to existing structs

      * This gives me the vibe of a "scripting" language like Python. It feels like you can duck type your way there, but you still get good type safety

    * Con: You don't get much compile time help to help you understand if an unused implementation adheres to an interface. You also don't get the advantages that something like an ``@Override`` annotation or keyword gets you.

      * This is only a con in the developer experience. You aren't losing any type safety here, I just don't like how it feels personally.

* Instanceof

  * Many languages support instanceof. In Go you have a couple of options, but none of them give the ease of use that something like instanceof does.
  * The options Go gives you to do this don't make it easy to check if something is an instanceof an interface. It's fairly simple to check concrete type, though.

* Identity and equality (Pro)

  * All types in Go don't have identity. This is a good thing. It means when you compare two types for being equal, they'll be equal based on their contents, rather than location in memory (like in a language such as Java)

* Testing

  * ``testdata`` directory is special and not well documented: https://github.com/golang/go/issues/14715

