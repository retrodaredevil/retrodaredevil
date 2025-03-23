JVM Libraries
================

Here are some opinions on different JVM libraries.

DGS Framework (By Netflix)
----------------------------

https://netflix.github.io/dgs/

DGS is a great framework by netflix and even `has its own IntelliJ plugin <https://plugins.jetbrains.com/plugin/17852-dgs>`_.
The IDE integration is really cool.
It's a really great way to easily make a GraphQL endpoint with no boilerplate!

There's also `Data Loaders <https://netflix.github.io/dgs/data-loaders/>`_ which solve the (N + 1) problem if I ever run into performance issues for that type of problem.

DGS Codegen
^^^^^^^^^^^^

https://github.com/Netflix/dgs-codegen

Part of the DGS framework, DGS codegen generates code based on a GraphQL schema.
This can be used to make a type-safe client API, or to generate classes and interfaces for you to use for your GraphQL server code.
It has a `bunch of options for configuring the code generation <https://netflix.github.io/dgs/generating-code-from-schema/#configuring-code-generation>`_.
Some options you could use are as shown:

.. code-block:: kotlin

  tasks.generateJava {

      typeMapping.putAll(mapOf(
          "Long" to "java.lang.Long",
          "UUID" to "java.util.UUID",
      ))
      schemaPaths.add("${projectDir}/src/main/resources/schema")
      packageName = "me.retrodaredevil.graphqlecho.codegen"
      generateClient = false
      generateDataTypes = false
      generateInterfaces = true
      generateInterfaceSetters = false
  }

Main downside is that even if you set it to generate interfaces, it will still generate POJOs that implement that interface.
So if all you are wanting is type-safety, but want to implement the POJOs yourself, you'll end up with a bunch of POJOs in your classpath you don't use.
Additionally it will not generate interfaces or POJOs that have the ability to alter their returned values based on input arguments.
Input arguments are completely ignored!!
That makes the code generation itself almost completely worthless for GraphQL endpoints that start to add any bit of complexity.

Also, generated interfaces are prefixed with an "I" (which I dislike -- this is Java for goodness sake).
It makes sense because the POJOs are generated alongside them. I guess it beats suffixing each POJO class name with "Impl".

Maybe someone has found a way to overcome that problem, but I'm not going to spend more time on it.
